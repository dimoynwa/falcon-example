from marshmallow import fields, Schema, ValidationError


class ScorePostSchema(Schema):
    class Meta:
        strict = True

    username = fields.Str(required=True)
    company = fields.String(required=True)
    score = fields.Integer(required=True)


class ScorePutSchema(Schema):
    class Meta:
        strict = True

    username = fields.String(required=True)
    score = fields.Integer(required=True)
