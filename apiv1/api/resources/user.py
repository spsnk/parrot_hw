from flask import abort, request
from flask_restful import Resource
from marshmallow import Schema, fields
from api.schemas import UserSchema, ProductSchema


class Users(Resource):

    schema = UserSchema()

    def post(self):
        data = request.get_json()
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        # TODO:
        # - database functions
        return data, 201


class UserCredentials(Resource):

    class UserCredentialsRequestSchema(Schema):
        id = fields.Email(required=True)

    schema = UserCredentialsRequestSchema()

    def get(self, id):
        errors = self.schema.validate({"id": id})
        if errors:
            abort(400, {"errors": errors})
        # TODO:
        # - database lookup and auth
        return '', 200


class UserOrders(Resource):

    class UserOrdersRequestSchema(Schema):
        user_id = fields.Email(required=True)
        products = fields.List(fields.Nested(ProductSchema), required=True)

    schema = UserOrdersRequestSchema()

    def post(self, id):
        data = request.get_json()
        data["user_id"] = id
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        # TODO:
        # - database lookup and auth
        return data, 201
