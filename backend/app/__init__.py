from flask import Flask, jsonify, request
import requests
import os
import random

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction


app = Flask(__name__)
blockchain = Blockchain()
sender_wallet = Wallet()
pubsub = PubSub(blockchain)

@app.route("/")
def route_default():
    return 'Hello world !'

@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())

    

@app.route("/blockchain/mine")
def route_blockchain_mine():
    data = "foo_data"

    blockchain.add_block(data)
    block = blockchain.chain[-1]

    pubsub.broadcast_block(block)

    return block.to_json()


@app.route("/wallet/transact", methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = Transaction(
        sender_wallet,
        transaction_data['recipient'],
        transaction_data['amount']
    )

    print(f"{transaction.to_json()}")
    return jsonify(transaction.to_json())


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)

    response = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    root_blockchain = Blockchain.from_json(response.json())

    try:
        blockchain.replace_chain(root_blockchain)
        print(f"Blockchain synchronized successfully\n")

    except Exception as e:
        print(f"Failed to synchronize blockchain !!!\n Error: {e}")



app.run(port=PORT)
