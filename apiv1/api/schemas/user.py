from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
