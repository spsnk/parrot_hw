from flask import abort, request
from flask_restful import Resource
from marshmallow import Schema, fields, validates_schema, ValidationError

from api.schemas import ProductSchema


class Products(Resource):

    schema = ProductSchema()

    def post(self):
        data = request.get_json()
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        # TODO:
        # - database functions
        return data, 201


class ProductsSales(Resource):

    class ProductsSalesRequest(Schema):
        start = fields.Date()
        end = fields.Date()

        @validates_schema
        def validate_dates(self, data, **kwargs):
            start = data.get("start")
            end = data.get("end")
            if (start and end) and start > end:
                raise ValidationError(
                    "Start date must be earlier than end date.")

    schema = ProductsSalesRequest()

    def get(self):
        filters = request.args.to_dict()
        errors = self.schema.validate(filters)
        if errors:
            abort(400, {"errors": errors})
        data = {
            "products": [
                {
                    "name": "coke",
                    "total_quantity": 53,
                    "total_earnings": 1258.36
                }
            ]
        }
        return data, 200
