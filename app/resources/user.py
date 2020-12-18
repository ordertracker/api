from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required

from flask import current_app as app
from flask_restx import Namespace, Resource

from app.helpers.common import authorize, welfare, get_service_token, status_code_responses
from app.models.user import UserModel

import hashlib

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_user_parser.add_argument(
    "name",
    type=str,
    required=False,
    help="This field cannot be blank"
)
_user_parser.add_argument(
    "email",
    type=str,
    required=False,
    help="This field cannot be blank"
)

api = Namespace('users', path='/api', description='Users')

@api.route('/user/<username>')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class User(Resource):
    @authorize
    @api.doc(description='Get User by username')
    def get(self, username):
        user = UserModel.find_user_by_username(username)
        if user:
            return user.json()

        return {
                   "message": "User not found!"
               }, 404

    @authorize
    @fresh_jwt_required
    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            user.remove_from_db()
            return {
                       "message": "User deleted!"
                   }, 200

        return {
                   "message": "User not found!"
               }, 404

@api.route('/register')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_user_by_username(data["username"]):
            return {
                       "message": "User {} exists!".format(data["username"])
                   }, 400

        user = UserModel(data["username"], hashlib.sha256(data["password"].encode("utf-8")).hexdigest(), data["name"], data["email"])
        user.save_to_db()
        return {
            "message": "User {} created!".format(data["username"])
        }, 200

@api.route('/login')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class UserLogin(Resource):
    def post(self):

        data = _user_parser.parse_args()
        user = UserModel.find_user_by_username(data["username"])

        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {
                   "message": "Invalid credentials!"
        }, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {
                   "access_token": new_token
        }, 200