from flask.blueprints import Blueprint
from flask_restx import Api

from .orders import api as orders_api
from .user import api as user_api
from .products.attributes import api as products_attribute_api
from .organizations.organizations import api as organizations_organizations_api

authorizations = {
    'apitoken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'API-TOKEN',
        'description': 'Token for authorization the Ordertracker app'
    }
}

api_blueprint = Blueprint("Ordertracker API", __name__)
api = Api(
        api_blueprint,
        title="Ordertracker API",
        version="1.0",
        authorizations=authorizations,
        security='apitoken'
)

# Initializing the API
api.add_namespace(orders_api)
api.add_namespace(organizations_organizations_api)
api.add_namespace(user_api)
api.add_namespace(products_attribute_api)
