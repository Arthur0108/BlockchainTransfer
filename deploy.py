from web3 import Web3
import json
from solcx import compile_files, install_solc
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Установим нужную версию Solidity
install_solc("0.8.29")

# Скомпилируем контракт
print("Компиляция контракта Donation.sol...")
compiled_sol = compile_files(["contracts/Donation.sol"], solc_version="0.8.29")
contract_interface = compiled_sol['contracts/Donation.sol:Donation']
abi = contract_interface['abi']
bytecode = contract_interface['bin']
print("Контракт успешно скомпилирован")

# Сохраняем ABI в файл
with open("build/contracts_Donation_sol_Donation.abi", "w") as f:
    json.dump(abi, f)
print("ABI сохранён в build/contracts_Donation_sol_Donation.abi")

# Подключение к Sepolia через Infura
infura_url = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(infura_url))
print("Подключение к Sepolia:", w3.is_connected())
assert w3.is_connected(), "Не удалось подключиться к Sepolia"

# Аккаунт для развертывания (твой кошелёк MetaMask)
account = "0xBaAc487e59a9d3D98e2C932dBfB20f4d4672b2fоE"  # полный адрес моего кошелька MetaMask
private_key = os.getenv("PRIVATE_KEY")  # приватный ключ из MetaMask
print(f"Используемый аккаунт: {account}")

# Проверяем баланс аккаунта
balance = w3.eth.get_balance(account)
balance_eth = w3.from_wei(balance, "ether")
print(f"Баланс аккаунта: {balance_eth} ETH")
assert balance_eth > 0, "На аккаунте недостаточно средств для развёртывания"

# Создание контракта
Donation = w3.eth.contract(abi=abi, bytecode=bytecode)
print("Контракт подготовлен для развертывания")

# Подготовка транзакции
nonce = w3.eth.get_transaction_count(account)
print(f"Nonce аккаунта: {nonce}")
tx = Donation.constructor().build_transaction({
    "from": account,
    "nonce": nonce,
    "gas": 2000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": 11155111  # Chain ID для Sepolia
})

# Подпись транзакции
signed_tx = w3.eth.account.sign_transaction(tx, private_key)

# Отправка транзакции
try:
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Транзакция отправлена, ожидание подтверждения...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Транзакция успешна:", tx_hash.hex())

    # Адрес развернутого контракта
    contract_address = tx_receipt.contractAddress
    print(f"Контракт развернут по адресу: {contract_address}")

    # Сохранение адреса для дальнейшего использования
    with open("contract_address.txt", "w") as f:
        f.write(contract_address)
except Exception as e:
    print("Ошибка при развертывании:", str(e))