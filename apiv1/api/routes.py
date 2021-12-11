from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api.resources import Users

app = Flask(__name__)
app.config.from_object("api.config.Config")
db = SQLAlchemy(app)
api = Api(app)

api.add_resource(Users, '/users')
