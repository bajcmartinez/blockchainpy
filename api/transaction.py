from flask import Blueprint, request
from http import HTTPStatus
from flasgger import swag_from
from api.globals import blockchain
from api.schema.transaction import TransactionSchema, TransactionCreatedSchema

transaction_api = Blueprint('transaction', __name__)


@transaction_api.route('/', methods=['POST'])
@swag_from({
    'parameters': [
        {
            "name": "transaction",
            "in": "body",
            "schema": {
                'type': 'object',
                'properties': {
                    'sender': {
                        'type': 'string'
                    },
                    'recipient': {
                        'type': 'string'
                    },
                    'amount': {
                        'type': 'number'
                    }
                }
            },
            "required": True,
        }
    ],
    'responses': {
        HTTPStatus.CREATED.value: {
            'description': 'The transaction was created and its pending to be included in a block.',
            'schema': TransactionSchema
        },
        HTTPStatus.BAD_REQUEST.value: {
            'description': 'Invalid transaction'
        }
    }
}, validation=True)
def new_transaction():
    """
    Generates a new transaction
    Consolidates the pending transactions into a new block, and adds the block to the blockchain
    ---
    """
    values = request.get_json()

    # Check that the required fields are in the body
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        response = {
            'message': 'Invalid transaction'
        }

        return TransactionCreatedSchema().dumps(response), 400

    # Create a new Transaction
    transaction, valid = blockchain.create_transaction(values['sender'], values['recipient'], values['amount'])

    if valid:
        response = {
            'message': "New transaction registered",
            'transaction': transaction
        }
        return TransactionCreatedSchema().dumps(response), 201

    response = {
        'message': 'Invalid transaction'
    }

    return TransactionCreatedSchema().dumps(response), 400