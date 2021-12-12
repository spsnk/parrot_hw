from flask import Flask
from flask_restful import Api

from api.resources import Products
from api.resources import ProductsSales
from api.resources import UserCredentials
from api.resources import UserOrders
from api.resources import Users

app = Flask(__name__)
app.config.from_object("api.config.Config")
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(UserCredentials, '/users/<string:id>/credentials')
api.add_resource(UserOrders, '/users/<string:id>/orders')

api.add_resource(Products, '/products')
api.add_resource(ProductsSales, '/products/sales')
