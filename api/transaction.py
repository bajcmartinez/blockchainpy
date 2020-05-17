from flask import Blueprint, request
from api.globals import blockchain, blockchain_encoder

transaction_api = Blueprint('transaction', __name__)


@transaction_api.route('/', methods=['POST'])
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