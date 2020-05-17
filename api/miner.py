from flask import Blueprint
from api.globals import blockchain, blockchain_encoder

miner_api = Blueprint('miner', __name__)


@miner_api.route('/mine', methods=['GET'])
def mine():
    """
    Mines a new block into the chain

    :return: result of the mining attempt and the new block
    """
    block = blockchain.mine('address')

    response = {
        'message': "New Block Mined",
        'block': block
    }
    return blockchain_encoder.encode(response), 200
