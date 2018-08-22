from marshmallow import fields, Schema


class ScorePostSchema(Schema):
    class Meta:
        strict = True

    username = fields.Str(required=True)
    company = fields.Str(required=True)
    score = fields.Integer(required=True)


class ScorePutSchema(Schema):
    class Meta:
        strict = True

    username = fields.Str(required=True)
    score = fields.Integer(required=True)


class UserPostSchema(Schema):
    class Meta:
        strict = True

    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
