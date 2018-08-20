from marshmallow import fields, Schema, ValidationError
from example import log


class ScorePostSchema(Schema):
    class Meta:
        strict = True

    username = fields.Str(required=True)
    company = fields.String(required=True)
    score = fields.Integer(required=True)


class ScorePutSchema(Schema):
    class Meta:
        strict = True

    id = fields.Integer(required=True)
