from flask_restful import reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required

from flask import current_app as app
from flask_restx import Namespace, Resource

from app.helpers.common import authorize, status_code_responses, is_admin
from app.models.user import User

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
class Users(Resource):
    @authorize
    @api.doc(description='Get User by username')
    def get(self, username):
        user = User.find_user_by_username(username)
        if user:
            return user.json()

        return {
                "message": "User not found!"
        }, 404

    @authorize
    @fresh_jwt_required
    def delete(self, user_id):
        user = User.find_user_by_id(user_id)
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

        username = data["username"]

        if User.find_user_by_username(data["username"]):
            return {
                    "message": "User {} exists!".format(data["username"])
            }, 400

        user = User(username, hashlib.sha256(data["password"].encode("utf-8")).hexdigest(), data["name"], data["email"])

        try:            
            user.save_to_db()
            return {
                    "message": "User {} created!".format(username)
            }, 200
        except:
            return {
                    "message": "The user {} was not saved in the database.".format(username)
            }, 500

@api.route('/login')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        username = data["username"]
        password = data["password"]

        if not username:
            return {
                "message": "Missing username parameter"
            }, 400
        if not password:
            return {
                "message": "Missing password parameter"
            }, 400

        user = User.find_user_by_username(username)
        if user and user.password == hashlib.sha256(password.encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                    "message": "Successfully logged in as {}".format(username),
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
