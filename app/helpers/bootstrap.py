import hashlib
from flask import current_app as app

from app.models.user import UserModel

'''
Create default user in database
'''
def default_user():
    
    username = app.config.get('DEFAULT_USERNAME') 
    password = app.config.get('DEFAULT_PASSWORD') 
    name = app.config.get('DEFAULT_NAME') 
    email = app.config.get('DEFAULT_EMAIL') 

    user = UserModel.find_user_by_username(username)
    if not user:
        user = UserModel(username, hashlib.sha256(password.encode("utf-8")).hexdigest(), name, email)
        user.save_to_db()
        app.logger.info('%s created successfully', username)