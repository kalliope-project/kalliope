from functools import wraps
from flask import request, Response

from kalliope import Utils
from kalliope.core.ConfigurationManager import SettingLoader


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    sl = SettingLoader()
    settings = sl.settings
    return username == settings.rest_api.login and password == settings.rest_api.password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        sl = SettingLoader()
        settings = sl.settings
        if settings.rest_api.password_protected:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated


def get_parameters_from_request(http_request):
    """
    Get "parameters" object from the
    :param http_request:
    :return:
    """
    parameters = None
    try:
        # Silent True in case no parameters it does not raise an error
        received_json = http_request.get_json(silent=True, force=True)
        if 'parameters' in received_json:
            parameters = received_json['parameters']
    except TypeError:
        pass
    return parameters


def get_value_flag_from_request(http_request, flag_to_find, is_boolean=False):
    """
    Get the value flag from the request if exist, None otherwise !
    :param http_request:
    :param flag_to_find: json flag to find in the http_request
    :param is_boolean: True if the expected value is a boolean, False Otherwise.
    :return: the Value of the flag that has been found in the request
    """
    flag_value = None
    try:
        received_json = http_request.get_json(force=True, silent=True, cache=True)
        if flag_to_find in received_json:
            flag_value = received_json[flag_to_find]
            if is_boolean:
                flag_value = Utils.str_to_bool(flag_value)
    except TypeError:
        # no json received
        pass
    return flag_value
