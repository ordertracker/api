import hashlib
from flask import current_app as app

from app.models.user import User, Role

'''
Create default admin user in database
'''
def default_user():
    
    username = app.config.get('DEFAULT_USERNAME') 
    password = app.config.get('DEFAULT_PASSWORD') 
    name = app.config.get('DEFAULT_NAME') 
    email = app.config.get('DEFAULT_EMAIL')

    user = User.find_user_by_username(username)
    if not user:
        user = User(username, hashlib.sha256(password.encode("utf-8")).hexdigest(), name, email)
        user.roles.append(Role(name='Admin'))
        user.save_to_db()
        app.logger.info('User %s created successfully', username)