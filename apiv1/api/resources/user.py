from flask_restful import Resource, reqparse, inputs
from flask import request


class Users(Resource):
    parser = None

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True, type=inputs.regex(
            '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'), help='Invalid e-mail address.')
        self.parser.add_argument(
            'name', required=True, type=str, help='Please provide a name.')

    def post(self):
        user = self.parser.parse_args()
        # TODO:
        # - database functions
        return user, 201
