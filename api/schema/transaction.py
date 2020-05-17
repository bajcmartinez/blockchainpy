from flask_marshmallow import Schema
from marshmallow.fields import Str, Number, Nested


class TransactionSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["sender", "recipient", "amount", "timestamp"]

    sender = Str()
    recipient = Str()
    amount = Number()
    timestamp = Number()


class TransactionCreatedSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["message", "transaction"]

    message = Str()
    transaction = Nested(TransactionSchema)