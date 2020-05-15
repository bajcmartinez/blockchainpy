from flask import Flask, request
from blockchain import Blockchain
from lib.encoder import BlockchainEncoder


def create_app(test_config=None):
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
        block = blockchain.mine()

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
        transaction, valid = blockchain.create_transaction(values['sender'], values['recipient'], values['amount'])

        if valid:
            response = {
                'message': "New transaction registered",
                'transaction': transaction
            }
            return blockchain_encoder.encode(response), 201

        response = {
            'message': 'Invalid transaction details'
        }

        return response, 400

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()
    app.run(host='0.0.0.0', port=port)
