from flask import Flask
from flask_restful import Api
from sqlalchemy.ext.automap import automap_base

from api.resources import Products
from api.resources import ProductsSales
from api.resources import UserCredentials
from api.resources import UserOrders
from api.resources import Users
from api.resources import User
from api.models.shared import db
from api.common.util import JsonEncoder

Flask.json_encoder = JsonEncoder
app = Flask(__name__)
app.config.from_object("api.config.Config")

api = Api(app)
db.init_app(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:id>')
api.add_resource(UserCredentials, '/users/<string:id>/credentials')
api.add_resource(UserOrders, '/users/<string:id>/orders')

api.add_resource(Products, '/products')
api.add_resource(ProductsSales, '/products/sales')
