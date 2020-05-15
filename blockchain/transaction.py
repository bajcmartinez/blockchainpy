import hashlib as hasher
from json import dumps
import time


class Transaction:
    def __init__(self, sender, recipient, amount):
        """
        Creates a new transaction

        :param sender: <str> sender account
        :param recipient: <str> recipient account
        :param amount: <float> amount to be transferred
        """
        self.sender = sender
        self.timestamp = time.time()
        self.recipient = recipient
        self.amount = amount

    def serialize(self):
        """
        Serializes a block into a string

        :return:
        """
        return dumps(self.__dict__)
