from unittest import TestCase
from blockchain import Blockchain
from blockchain.block import Block


class TestBlockchain(TestCase):
    def test_mine_empty_transaction_block(self):
        """
        Test mining an empty transaction block
        """
        miner_address = 'miner_address'

        blockchain = Blockchain()
        block = blockchain.mine(miner_address)

        # First we look that a new block could be mined
        self.assertIsNotNone(block)

        # Let's see if the block was added to the chain
        self.assertEqual(blockchain.last_block.hash, block.hash)

        # We need to check that the block contains only the reward transaction
        self.assertEqual(len(block.transactions), 1)

        reward_transaction = block.transactions[0]

        # We make sure the reward function has no sender, and gives away exactly 1 coin
        self.assertEqual(reward_transaction.sender, '0')
        self.assertEqual(reward_transaction.recipient, miner_address)
        self.assertEqual(reward_transaction.amount, 1)

    def test_mine_simple_transaction_block(self):
        """
        Test mining a simple transaction block
        """
        miner_address = 'miner_address'

        blockchain = Blockchain()
        blockchain.create_transaction('sender', 'recipient', 1)
        blockchain.create_transaction('sender2', 'recipient2', 1.5)
        self.assertEqual(len(blockchain.pending_transactions), 2)

        block = blockchain.mine(miner_address)

        # First we look that a new block could be mined
        self.assertIsNotNone(block)

        # Let's see if the block was added to the chain
        self.assertEqual(blockchain.last_block.hash, block.hash)

        # We need to check that the transaction list is empty
        self.assertEqual(0, len(blockchain.pending_transactions))

        # We need to check that the block contains all of the transactions
        self.assertEqual(3, len(block.transactions))

        reward_transaction = block.transactions[-1]

        # We make sure the reward function has no sender, and gives away exactly 1 coin
        self.assertEqual('0', reward_transaction.sender)
        self.assertEqual(miner_address, reward_transaction.recipient)
        self.assertEqual(1, reward_transaction.amount)

    def test_validate_empty_chain(self):
        """
        Test validating an empty chain
        """
        miner_address = 'miner_address'

        blockchain = Blockchain()
        block = blockchain.mine(miner_address)

        self.assertTrue(blockchain.validate_chain(blockchain.full_chain))

    def test_validate_chain_with_tempered_block_nonce(self):
        """
        Test validating a chain with a tempered block nonce
        """
        miner_address = 'miner_address'

        blockchain = Blockchain()
        last_block = blockchain.mine(miner_address)

        # First we look that a new block could be mined
        self.assertIsNotNone(last_block)

        chain = blockchain.full_chain

        # Hack a block
        chain.append(Block(1, [], 1, last_block.hash))

        self.assertFalse(blockchain.validate_chain(blockchain.full_chain))

    def test_replace_chain(self):
        """
        Test that the chain is replaced for a larger one

        :return:
        """
        import copy
        miner_address = 'miner_address'

        blockchain1 = Blockchain()
        blockchain1.mine(miner_address)

        blockchain2 = copy.deepcopy(blockchain1)
        blockchain2.mine(miner_address)

        # Now let's make sure that each blockchain has its own number of blocks
        self.assertEqual(2, len(blockchain1.full_chain))
        self.assertEqual(3, len(blockchain2.full_chain))

        # Then let's replace blockchain1 with blockchain2
        blockchain1.replace_chain(blockchain2.full_chain)

        self.assertEqual(3, len(blockchain1.full_chain))
        self.assertEqual(3, len(blockchain2.full_chain))
        self.assertEqual(blockchain1.last_block.hash, blockchain2.last_block.hash)

    def test_replace_chain_keep_original(self):
        """
        Test that the chain is not replaced for a smaller one

        :return:
        """
        import copy
        miner_address = 'miner_address'

        blockchain1 = Blockchain()
        blockchain1.mine(miner_address)

        blockchain2 = copy.deepcopy(blockchain1)
        blockchain1.mine(miner_address)

        # Now let's make sure that each blockchain has its own number of blocks
        self.assertEqual(3, len(blockchain1.full_chain))
        self.assertEqual(2, len(blockchain2.full_chain))

        # Then let's replace blockchain1 with blockchain2
        blockchain1.replace_chain(blockchain2.full_chain)

        self.assertEqual(3, len(blockchain1.full_chain))
        self.assertEqual(2, len(blockchain2.full_chain))


