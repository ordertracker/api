from flask_restx import Model, fields

magento_model = Model('magento_model', {
    'url': fields.String(required=True),
    'consumer_key': fields.String(required=True),
    'consumer_secret': fields.Integer(required=True),
    'access_token': fields.String(required=True),
    'access_token_secret': fields.String(required=True)
})
