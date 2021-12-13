from flask import abort, request
from flask_restful import Resource
from marshmallow import Schema, fields, validates_schema, ValidationError
from sqlalchemy.exc import IntegrityError

from api.schemas import ProductSchema
from api.models import ProductsModel
from api.common.util import JsonEncoder


class Products(Resource):

    schema = ProductSchema()

    def post(self):
        data = request.get_json()
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        try:
            new_product = ProductsModel(**data).create()
        except IntegrityError:
            abort(409, {"errors": f"Product <{data['name']}> already exists."})
        except Exception:
            abort(500, {"errors": "Server error."})
        return new_product.get_dict(), 201


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
