import traceback
from functools import wraps
from flask import request, current_app as app

class NoServiceToken(Exception):
    pass

def welfare(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoServiceToken as e:
            return {
                'status': 'fail',
                'description': str(e)
            }, 400
        except Exception as e:
            traceback.print_exc()
            return {
                       'status': 'error',
                       'description': str(e)
                   }, 500

    return wrapper

def authorize(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('API-TOKEN') == app.config.get('AUTH_TOKEN'):
            return func(*args, **kwargs)

        return {
                   'status': 'fail',
                   'description': 'Wrong token.'
               }, 401

    return wrapper

def get_service_token():
    service_token = request.headers.get('SERVICE-TOKEN')
    if not service_token:
        raise NoServiceToken('SERVICE-TOKEN header is missing.')

    return service_token

status_code_responses = {
    200: 'Success',
    204: 'Success without body',
    400: 'Bad request',
    401: 'Not Authorized',
    403: 'Forbidden',
    500: 'Internal server error',
    503: 'Service unavailable'
}
