import decimal
from api.common.auth import auth_required, generate_token
from api.models import (OrderContentsModel, OrdersModel, ProductsModel,
                        UsersModel)
from api.models.shared import db
from api.schemas import ProductsOrdersSchema, UserSchema
from api.schemas.product import ProductSchema
from flask import abort, jsonify, request
from flask_restful import Resource
from marshmallow import Schema, fields
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


class Users(Resource):

    schema = UserSchema()

    def post(self):
        data = request.get_json()
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        try:
            new_user = UsersModel(**data).create()
        except IntegrityError:
            abort(409, {"errors": f"Email <{data['email']}> already in use."})
        except Exception:
            abort(500, {"errors": "Server error."})
        return new_user.get_dict(), 201


class User(Resource):

    class UserRequestSchema(Schema):
        id = fields.Email(required=True)

    schema = UserRequestSchema()

    @auth_required
    def get(self, id):
        errors = self.schema.validate({"id": id})
        if errors:
            abort(400)
        result = db.session.query(UsersModel).filter(
            func.lower(UsersModel.email) == func.lower(id)
        ).first()
        return result.get_dict(), 200


class UserCredentials(Resource):

    class UserCredentialsRequestSchema(Schema):
        id = fields.Email(required=True)

    schema = UserCredentialsRequestSchema()

    def get(self, id):
        errors = self.schema.validate({"id": id})
        if errors:
            abort(400, {"errors": errors})
        result = db.session.query(UsersModel.email).filter(
            func.lower(UsersModel.email) == func.lower(id)
        ).first()
        if not result:
            abort(404, {"errors": 'User not found.'})
        token = generate_token(id)
        return {"token": token}, 200


class UserOrders(Resource):

    class UserOrdersRequestSchema(Schema):
        user_email = fields.Email(required=True)
        products = fields.List(fields.Nested(
            ProductsOrdersSchema), required=True)

    schema = UserOrdersRequestSchema()

    @auth_required
    def post(self, id: str):
        data = request.get_json()
        data["user_email"] = id.strip().lower()
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        # TODO:
        # - move database logic out of here!!
        total = decimal.Decimal(0)
        try:
            # Create order
            new_order = {
                "user_email": data["user_email"],
                "total": 0
            }
            db_order = OrdersModel(**new_order)
            db.session.add(db_order)
            db.session.flush()
            print("TX Orders->", db_order)

            # Create or get product from db
            for product in data["products"]:
                product["name"] = product["name"].strip().lower()
                db_product: ProductsModel = db.session.query(ProductsModel).filter(
                    ProductsModel.name == product["name"]).first()
                if db_product is None:
                    new_product = {
                        "name": product.get("name"),
                        "unitary_price": decimal.Decimal(product.get("unitary_price"))
                    }
                    errors = ProductSchema().validate(new_product)
                    if errors:
                        db.session.rollback()
                        abort(400, {
                            "errors": {
                                product["name"]: {
                                    k: v for (k, v) in errors.items()}
                            }
                        })
                    db_product = ProductsModel(**new_product)
                    db.session.add(db_product)
                    db.session.flush()
                    print("TX Products->", db_product)
                elif db_product and "unitary_price" in product and db_product.unitary_price != product["unitary_price"]:
                    abort(409, {
                        "errors": {
                            product["name"]: "Product already exists with different unitary price."
                        }
                    })
                product["unitary_price"] = db_product.unitary_price.__float__()
                # here we have a valid db_product
                # push product to order
                new_order_contents = {
                    "order_id": db_order.id,
                    "product_id": db_product.id,
                    "quantity": product["quantity"]
                }
                db_order_contents = OrderContentsModel(**new_order_contents)
                db.session.add(db_order_contents)
                total += db_product.unitary_price * db_order_contents.quantity
                db.session.flush()
                print("TX OrderContents->", db_order_contents)
            # save changes to db
            db_order.total = total
            # db.session.add(db_order)
            db.session.commit()
            data["order_id"] = db_order.id
            data["total"] = db_order.total.__float__()
        except IntegrityError as e:
            print({"error": e})
            db.session.rollback()
            abort(409)
        return data, 201
