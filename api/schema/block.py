from flask_marshmallow import Schema
from marshmallow.fields import Nested, Str, Number
from api.schema.transaction import TransactionSchema


class BlockSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["index", "timestamp", "transactions", "nonce", "previous_hash", "hash"]

    index = Number()
    nonce = Str()
    timestamp = Number()
    previous_hash = Str()
    hash = Str()
    transactions = Nested(TransactionSchema, many=True)
