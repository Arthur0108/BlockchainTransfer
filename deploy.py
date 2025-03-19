from web3 import Web3
import json
from solcx import compile_files

# Подключение к Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print("Подключение к Ganache:", w3.is_connected())
assert w3.is_connected(), "Не удалось подключиться к Ganache"

# Аккаунт для развертывания (первый из Ganache)
account = w3.eth.accounts[0]
print("Аккаунт для развертывания:", account)

# Чтение ABI и байт-кода
with open("build/contracts_Donation_sol_Donation.abi", "r") as file:
    abi = json.load(file)
with open("build/contracts_Donation_sol_Donation.bin", "r") as file:
    bytecode = file.read()

# Создание контракта
Donation = w3.eth.contract(abi=abi, bytecode=bytecode)
print("Контракт подготовлен для развертывания")

# Развертывание
try:
    tx_hash = Donation.constructor().transact({"from": account})
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