from http import HTTPStatus
from flask import Blueprint, abort
from flasgger import swag_from
from api.globals import blockchain
from api.schema.blockchain import BlockchainSchema
from api.schema.block import BlockSchema

blockchain_api = Blueprint('blockchain', __name__)


@blockchain_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'The blockchain as a list of blocks with all transactions.',
            'schema': BlockchainSchema
        }
    }
})
def get_chain():
    """
    Returns the full blockchain
    Returns blockchain as a list of blocks with all transactions.
    ---
    """
    chain = blockchain.full_chain
    response = {
        'blockchain': chain
    }

    return BlockchainSchema().dump(response), 200


@blockchain_api.route('/block/<block_hash>')
@swag_from({
    'parameters': [
        {
            "name": "block_hash",
            "in": "path",
            "type": "string",
            "required": True,
        }
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'The block with all its transactions.',
            'schema': BlockSchema
        },
        HTTPStatus.NOT_FOUND.value: {
            'description': 'Block not found.'
        }
    }
})
def get_block(block_hash):
    """
    Returns the full blockchain
    Returns blockchain as a list of blocks with all transactions.
    ---
    """
    blocks = [x for x in blockchain.full_chain if x.hash == block_hash]
    if len(blocks) > 0:
        return BlockSchema().dump(blocks[0]), 200

    abort(404)
