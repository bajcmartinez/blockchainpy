from unittest import TestCase
from blockchain import Blockchain


class TestBlockchain(TestCase):
    def test_mine_empty_transaction_block(self):
        """
        Test mining an empty transaction block
        """
        blockchain = Blockchain()
        block = blockchain.mine()

        # Let's see if the block was added to the chain
        self.assertEqual(blockchain.last_block.hash, block.hash)

        # We need to check that the block contains only the reward transaction
        self.assertEqual(len(block.transactions), 1)

        reward_transaction = block.transactions[0]

        # We make sure the reward function has no sender, and gives away exactly 1 coin
        self.assertEqual(reward_transaction.sender, '0')
        self.assertEqual(reward_transaction.recipient, blockchain.node_id)
        self.assertEqual(reward_transaction.amount, 1)
