from json import JSONEncoder
import blockchain


class BlockchainEncoder(JSONEncoder):
    def default(self, z):
        if isinstance(z, blockchain.block.Block) or isinstance(z, blockchain.transaction.Transaction):
            return z.serialize()
        else:
            return super().default(z)