from uuid import uuid4
import hashlib
from blockchain.block import Block
from blockchain.transaction import Transaction


class Blockchain:

    def __init__(self):
        self.__current_transactions = []
        self.chain = []
        self.nodes = set()
        # Generate random number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')
        # Create genesis block
        self.create_genesis()

    def create_genesis(self):
        """
        Creates the Genesis block and passes it to the chain

        :return:
        """
        block = Block(0, self.__current_transactions, 0, '00')

        self.chain.append(block)
        return block

    def create_block(self, nonce, previous_hash):
        """
        Creates a new block and passes it to the chain

        :param nonce: <int> nonce for the new block
        :param previous_hash: <str> previous hash
        :return: <Block> newly created block
        """
        block = Block(self.last_block.index + 1, self.__current_transactions, nonce, previous_hash)

        # Reset the current list of transactions
        self.__current_transactions = []

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

        if transaction.validate():
            self.__current_transactions.append(transaction)

            return transaction, True

        return None, False

    def mine(self):
        """
        Mines a new block into the chain

        :return: result of the mining attempt and the new block
        """
        last_block = self.last_block

        # Let's start with the heavy duty, generating the proof of work
        nonce = self.generate_proof_of_work(last_block)

        # In the next step we will create a new transaction to reward the miner
        # In this particular case, the miner will receive coins that are just "created", so there is no sender
        self.create_transaction(
            sender="0",
            recipient=self.node_id,
            amount=1,
        )

        # Add the block to the new chain
        return self.create_block(nonce, last_block.hash)

    @staticmethod
    def validate_proof_of_work(last_nonce, last_hash, nonce):
        """
        Validates the nonce

        :param last_nonce: <int> Nonce of the last block
        :param nonce: <int> Current nonce to be validated
        :param last_hash: <str> Hash of the last block
        :return: <bool> True if correct, False if not.
        """
        sha = hashlib.sha256(f'{last_nonce}{last_hash}{nonce}'.encode())
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

    @property
    def last_transaction(self):
        return self.__current_transactions[-1]
