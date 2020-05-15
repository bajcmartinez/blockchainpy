from unittest import TestCase
from blockchain.block import Block


class TestBlock(TestCase):
    def test_block_hash(self):
        """
        Test hashing blocks
        """
        block = Block(1, [], 0, '0')

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual(block.hash, block.hash_block())
