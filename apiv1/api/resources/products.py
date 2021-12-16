from datetime import datetime

from api.models import OrderContentsModel, OrdersModel, ProductsModel
from api.models.shared import db
from api.schemas import ProductSchema
from flask import abort, request
from flask_restful import Resource
from flask_sqlalchemy import BaseQuery
from marshmallow import Schema, ValidationError, fields, validates_schema
from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError


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
        if filters.get("end") is None and filters.get("start"):
            filters["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # TODO
        # -- remove database logic from here
        query: BaseQuery = (
            db.session.query(
                ProductsModel.name,
                func.sum(OrderContentsModel.quantity).label("units"),
                func.sum(
                    OrderContentsModel.unitary_price *
                    OrderContentsModel.quantity
                ).label("revenue")
            ).join(ProductsModel)
            .join(OrdersModel)
            .group_by(ProductsModel.name)
            .order_by(desc("units"))
        )
        if filters.get("start") and filters.get("end"):
            query = query.filter(
                OrdersModel.date_created.between(
                    filters["start"], filters["end"]
                )
            )
        elif filters.get("end"):
            query = query.filter(
                OrdersModel.date_created < filters["end"]
            )
        result_set = query.all()
        product_list: list = list(map(lambda p: {
            "name": p[0],
            "units": p[1],
            "revenue": float(p[2])
        }, result_set))
        results = {
            "range": filters if filters else "all",
            "products": product_list
        }
        return results, 200
