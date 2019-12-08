from flask_restful import Resource, reqparse

from flask import current_app as app
from flask_restplus import Namespace, Resource

from app.helpers.common import authorize, welfare, get_service_token, status_code_responses
from app.models.attribute import AttributeModel

_attribute_parser = reqparse.RequestParser()
_attribute_parser.add_argument(
    "product_id",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_attribute_parser.add_argument(
    "attribute_id",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_attribute_parser.add_argument(
    "attribute_key",
    type=str,
    required=False
)
_attribute_parser.add_argument(
    "attribute_value",
    type=str,
    required=True,
    help="This field cannot be blank"
)

api = Namespace('attributes', path='/api/products', description='Product Attributes')

@api.route('/attribute/add')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class AttributeAdd(Resource):
    @authorize
    def post(self):
        data = _attribute_parser.parse_args()
        attribute = AttributeModel(data["product_id"], data["attribute_id"], data["attribute_key"], data["attribute_value"])
        attribute.save_to_db()
        return {
            "message": "Attribute {} created!".format(data)
        }, 200

@api.route('/attribute/get/<attribute_id>')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class AttributeGet(Resource):
    @authorize
    def get(self, attribute_id):
        attr = AttributeModel.get_attr_by_id(attribute_id)
        return {
            "attribute": attr
        }, 200