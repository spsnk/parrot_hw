from flask import abort, request, jsonify
from flask_restful import Resource
from marshmallow import Schema, fields
from api.schemas import UserSchema, ProductSchema
from api.models.user import Users as UsersModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from api.models.shared import db
from api.common.auth import auth_required, generate_token


class Users(Resource):

    schema = UserSchema()

    def post(self):
        data = request.get_json()
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        try:
            new_user = UsersModel(
                email=func.lower(data["email"]), name=data["name"])
            db.session.add(new_user)
            db.session.commit()
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
        user_id = fields.Email(required=True)
        products = fields.List(fields.Nested(ProductSchema), required=True)

    schema = UserOrdersRequestSchema()

    @auth_required
    def post(self, id):
        data = request.get_json()
        data["user_id"] = id
        errors = self.schema.validate(data)
        if errors:
            abort(400, {"errors": errors})
        # TODO:
        # - database lookup and auth
        return data, 201
