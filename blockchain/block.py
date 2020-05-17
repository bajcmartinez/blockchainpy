import hashlib
from api.schema.block import BlockSchema
from time import time


class Block:
    def __init__(self, index, transactions, nonce, previous_hash):
        """
        Constructs a new block

        :param index:
        :param transactions:
        :param previous_hash:
        """
        self.index = index
        self.timestamp = time()
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

        return BlockSchema().dumps(block_params)

    def hash_block(self):
        """
        Calculates the hash of the block

        :return:
        """
        sha = hashlib.sha256()
        sha.update(self.serialize(['hash']).encode('utf-8'))
        return sha.hexdigest()
