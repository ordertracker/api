import os, logging

from flask import Flask
from flask_cors import CORS

from app.resources import api_blueprint
from app.database.db import db
from app.helpers.bootstrap import default_user

def create_app(config, **kwargs):

    app = Flask(__name__, **kwargs)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    app.register_blueprint(api_blueprint)
    app.config.from_object(config)

    logging.basicConfig(level=logging.INFO)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        default_user()

    auth_token = app.config.get('AUTH_TOKEN') 
    
    if len(auth_token) == 0:
        raise EnvironmentError('AUTH_TOKEN is not set. Can not proceed operating without authorization token for the API.')
    elif len(auth_token) < 15:
        raise Exception('AUTH_TOKEN too weak, please use token with more than 14 characters')

    app.secret_key = app.config.get('AUTH_TOKEN')

    return app
