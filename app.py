from flask import Flask, request, jsonify, send_from_directory,render_template
from web3 import Web3
import json

app = Flask(__name__)

# Подключение к Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected(), "Не удалось подключиться к Ganache"

# Загрузка контракта
with open("build/contracts_Donation_sol_Donation.abi", "r") as file:
    abi = json.load(file)
with open("contract_address.txt", "r") as file:
    contract_address = file.read().strip()

contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route("/donate", methods=["POST"])
def donate():
    data = request.json
    amount = data["amount"]  # В wei
    account = data["account"]  # Адрес отправителя

    tx_hash = contract.functions.donate().transact({
        "from": account,
        "value": w3.to_wei(amount, "ether")
    })
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"tx_hash": tx_hash.hex()})

@app.route("/total", methods=["GET"])
def get_total():
    total = contract.functions.totalDonations().call()
    return jsonify({"total": w3.from_wei(total, "ether")})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)