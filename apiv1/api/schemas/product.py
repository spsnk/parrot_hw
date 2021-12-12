from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    name = fields.Str(required=True)
    quantity = fields.Int(
        strict=True,
        required=True,
        validate=validate.Range(
            min=1, error="Quantity must be greater than 0.")
    )
    unitary_price = fields.Number(
        required=True,
        validate=validate.Range(
            min=0.01, error="Unitary price must be greater than 0.")
    )
