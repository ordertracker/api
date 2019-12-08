import subprocess, os, logging
from app import create_app
from app.database.db import db
from flask_jwt_extended import JWTManager

env = os.environ.get('APP_ENV')
app = create_app('app.config.' + env)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)