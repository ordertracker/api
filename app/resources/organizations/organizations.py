from flask_restful import reqparse
from flask_restplus import Namespace, Resource

from flask import current_app as app

from app.helpers.common import authorize, welfare, get_service_token, status_code_responses
from app.models.organizations import OrganizationsModel

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
    @authorize
    def post(self):
        data = _organization_parser.parse_args()
        if OrganizationsModel.find_org_by_name(data['name']):
            return {
                "message": "The name {} is already taken by other organization".format(data['name'])
            }, 400
        
        org = OrganizationsModel(data['name'], data['description'])
        org.save_to_db()
        return {
            "message": "Organization {} has been created.".format(data['name'])
        }, 200