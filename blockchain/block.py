import hashlib
from json import dumps
from lib.encoder import BlockchainEncoder
import time


class Block:
    def __init__(self, index, transactions, nonce, previous_hash):
        """
        Constructs a new block

        :param index:
        :param transactions:
        :param previous_hash:
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def serialize(self, ignore=None):
        """
        Serializes a block into a string

        :return:
        """
        if ignore is None:
            ignore = []
        block_params = {x: self.__dict__[x] for x in self.__dict__ if x not in ignore}

        return dumps(block_params, cls=BlockchainEncoder)

    def hash_block(self):
        """
        Calculates the hash of the block

        :return:
        """
        sha = hashlib.sha256()
        sha.update(self.serialize(['hash']).encode('utf-8'))
        return sha.hexdigest()
