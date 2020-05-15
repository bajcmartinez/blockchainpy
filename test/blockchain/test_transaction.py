from unittest import TestCase
from blockchain import Blockchain


class TestTransaction(TestCase):
    def test_create_transaction(self):
        """
        Test creating a transaction
        """
        blockchain = Blockchain()
        _, valid = blockchain.create_transaction('sender', 'recipient', 1)

        transaction = blockchain.last_transaction

        # Let's now validate the transaction
        self.assertTrue(valid)
        self.assertEqual(transaction.sender, 'sender')
        self.assertEqual(transaction.recipient, 'recipient')
        self.assertEqual(transaction.amount, 1)

    def test_create_negative_transaction(self):
        """
        Test creating a transaction with a negative amount
        """
        blockchain = Blockchain()
        transaction, valid = blockchain.create_transaction('sender', 'recipient', -1)

        # Let's now validate the transaction
        self.assertIsNone(transaction)
        self.assertFalse(valid)
