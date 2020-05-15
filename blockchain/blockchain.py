from uuid import uuid4
import hashlib as hasher
from blockchain.block import Block
from blockchain.transaction import Transaction


class Blockchain:

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Generate random number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')
        # Create genesis block
        self.create_block(0, '00')

    def create_block(self, nonce, previous_hash):
        """
        Creates a new block and passes it to the chain

        :param nonce: <int> nonce for the new block
        :param previous_hash: <str> previous hash
        :return: <Block> newly created block
        """
        block = Block(len(self.chain) + 1, self.current_transactions, nonce, previous_hash)

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def create_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next block

        :param sender: <str> sender address
        :param recipient: <str> recipient address
        :param amount: <float> amount
        :return: <Transaction> generated transaction
        """
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)

        return transaction

    @staticmethod
    def validate_proof_of_work(last_nonce, last_hash, nonce):
        """
        Validates the nonce

        :param last_nonce: <int> Nonce of the last block
        :param nonce: <int> Current nonce to be validated
        :param last_hash: <str> Hash of the last block
        :return: <bool> True if correct, False if not.
        """
        sha = hasher.sha256(f'{last_nonce}{last_hash}{nonce}'.encode())
        return sha.hexdigest()[:4] == '0000'

    def generate_proof_of_work(self, block):
        """
        Very simple proof of work algorithm:

        - Find a number 'p' such that hash(pp') contains 4 leading zeroes
        - Where p is the previous proof, and p' is the new proof

        :param block: <Block> reference to the last block object
        :return: <int> generated nonce
        """
        last_nonce = block.nonce
        last_hash = block.hash

        nonce = 0
        while not self.validate_proof_of_work(last_nonce, last_hash, nonce):
            nonce += 1

        return nonce

    @property
    def last_block(self):
        return self.chain[-1]
