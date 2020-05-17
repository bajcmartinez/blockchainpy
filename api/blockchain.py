from flask import Blueprint
from api.globals import blockchain, blockchain_encoder

blockchain_api = Blueprint('blockchain', __name__)


@blockchain_api.route('/')
def get_chain():
    chain = blockchain.full_chain
    response = {
        'chain': chain,
        'length': len(chain)
    }
    return blockchain_encoder.encode(response), 200