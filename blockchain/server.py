from flask import Flask, request
from blockchain.blockchain import Blockchain
from blockchain.encoder import BlockchainEncoder

app = Flask(__name__)
blockchain = Blockchain()
blockchain_encoder = BlockchainEncoder()


@app.route('/chain')
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return blockchain_encoder.encode(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    """
    Mines a new block into the chain

    :return: result of the mining attempt and the new block
    """
    last_block = blockchain.last_block

    # Let's start with the heavy duty, generating the proof of work
    nonce = blockchain.generate_proof_of_work(last_block)

    # In the next step we will create a new transaction to reward the miner
    # In this particular case, the miner will receive coins that are just "created", so there is no sender
    blockchain.create_transaction(
        sender="0",
        recipient=blockchain.node_id,
        amount=1,
    )

    # Add the block to the new chain
    block = blockchain.create_block(nonce, last_block.hash)

    response = {
        'message': "New Block Mined",
        'block': block
    }
    return blockchain_encoder.encode(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the body
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Invalid transaction', 400

    # Create a new Transaction
    transaction = blockchain.create_transaction(values['sender'], values['recipient'], values['amount'])

    response = {
        'message': "New transaction registered",
        'transaction': transaction
    }
    return blockchain_encoder.encode(response), 201


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
