import hashlib
from flask import current_app as app

from app.models.user import UserModel
from app.models.role import RoleModel

'''
Create default admin user in database
'''
def default_user():
    
    username = app.config.get('DEFAULT_USERNAME') 
    password = app.config.get('DEFAULT_PASSWORD') 
    name = app.config.get('DEFAULT_NAME') 
    email = app.config.get('DEFAULT_EMAIL')
    role_id = 1
    org_id = 0

    user = UserModel.find_user_by_username(username)
    if not user:
        user = UserModel(username, hashlib.sha256(password.encode("utf-8")).hexdigest(), name, email, role_id, org_id)
        user.save_to_db()
        app.logger.info('User %s created successfully', username)

'''
Creating the default user roles
'''
def init_roles():

    roles = {
            1: {
                'key': 'admin',
                'name': 'Administrator'
            },
            2: {
                'key': 'organization',
                'name': 'Organization'
            }
    }

    for key, value in roles.items():
        role = RoleModel.find_role_by_key(value['key'])
        if not role:
            role_model = RoleModel(value['key'], value['name'])
            role_model.save_to_db()
            app.logger.info('Role %s created successfully', value['key'])
