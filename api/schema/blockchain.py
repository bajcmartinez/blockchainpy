from flask_marshmallow import Schema
from marshmallow.fields import Nested
from api.schema.block import BlockSchema


class BlockchainSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["blockchain"]

    blockchain = Nested(BlockSchema, many=True)