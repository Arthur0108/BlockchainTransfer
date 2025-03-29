from flask import Flask, render_template, request, jsonify
from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

app = Flask(__name__)

# Подключение к Sepolia через Infura
infura_url = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(infura_url))

# Проверяем подключение
if not w3.is_connected():
    raise Exception("Не удалось подключиться к Sepolia")

# Читаем адрес контракта из файла
with open("contract_address.txt", "r") as f:
    contract_address = f.read().strip()

# Читаем ABI из скомпилированного контракта
with open("build/contracts_Donation_sol_Donation.abi", "r") as f:
    abi = json.load(f)

# Создаём объект контракта
contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    try:
        amount = int(request.form['amount'])
        # Здесь мы не отправляем транзакцию, а возвращаем данные для MetaMask
        return jsonify({
            'success': True,
            'contract_address': contract_address,
            'amount': amount
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_donations', methods=['GET'])
def get_donations():
    try:
        total = contract.functions.totalDonations().call()  # Используем totalDonations
        return jsonify({'success': True, 'total': total})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_abi', methods=['GET'])
def get_abi():
    try:
        with open("build/contracts_Donation_sol_Donation.abi", "r") as f:
            abi = json.load(f)
        return jsonify(abi)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)