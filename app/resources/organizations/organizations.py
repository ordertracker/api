from flask_restful import reqparse
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from flask import current_app as app

from app.helpers.common import status_code_responses, is_admin
from app.models.organizations import Organizations

_organization_parser = reqparse.RequestParser()
_organization_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_organization_parser.add_argument(
    "description",
    type=str,
    required=False
)

api = Namespace('organizations', path='/api', description='User organization')

@api.route('/organization')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class Organization(Resource):
    @jwt_required
    @is_admin
    def post(self):
        data = _organization_parser.parse_args()
        if Organizations.find_org_by_name(data['name']):
            return {
                "message": "The name {} is already taken by other organization".format(data['name'])
            }, 400
        
        org = Organizations(data['name'], data['description'])

        try:
            org.save_to_db()
            return {
                "message": "Organization {} has been created.".format(data['name'])
            }, 200
        except:
            return {
                "message": "The organization named as {} was not saved in the database.".format(data['name'])
            }, 403
