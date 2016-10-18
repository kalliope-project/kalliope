from functools import wraps
from flask import request, Response

from core.ConfigurationManager import SettingLoader


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    settings = SettingLoader.get_settings()
    # we only check the password if the user select password protected
    if settings.rest_api.password_protected:
        return username == settings.rest_api.login and password == settings.rest_api.password
    return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
