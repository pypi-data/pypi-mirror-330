from typing import Union, Callable

from gtnapi._shared import Shared as Shared
from gtnapi._auth import Auth as Auth
from gtnapi._streaming import Streaming as Streaming
from gtnapi._requests import Requests as Requests

shared: Shared


def init(api_url: str, institution: str, app_key: str,
         app_secret: str = None, private_key: str = None,
         customer_number: str = None,
         user: str = None, password: str = None):
    """
    :param api_url: url of the api service
    :param app_key: app key of the institution
    :param app_secret: app secret of the institution
    :param private_key: private key of the institution
    :param institution: institution code
    :param customer_number: optional customer number. not required for the institution mode
    :param user: user name in user/pass mode
    :param password: password name in user/pass mode
    """
    global shared
    shared = Shared
    shared.init(api_url, app_key, app_secret, private_key, institution, customer_number, user, password)
    # key_rot._init()
    return Auth.init()


def get_api_url():
    """
    :return: the api service url
    """
    return shared.get_api_url()


def get_app_key():
    """
    :return: the app key
    """
    return shared.get_app_key()


def get_app_secret():
    """
    :return: the app secret
    """
    return shared.get_app_secret()


def get_private_key():
    """
    :return: the institution's private key
    """
    return shared.get_private_key()


def get_institution():
    """
    :return: the institution code
    """
    return shared.get_institution()


def set_assertion(assertion):
    """
    :param assertion: assertion string
    """
    shared.set_assertion(assertion)


def get_assertion():
    """
    :return: the assertion
    """
    return shared.get_assertion()


def set_server_token(server_token):
    """
    :param server_token: server token string
    """
    shared.set_server_token(server_token)


def get_server_token():
    """
    :return: the server token string
    """
    return shared.get_server_token()


def set_customer_token(customer):
    """
    :param customer: customer token string
    """
    shared.set_customer_token(customer)


def get_customer_token():
    """
    :return: the customer token
    """
    return shared.get_customer_token()


def get_user_name():
    """
    :return: the user name
    """
    return shared.get_user_name()


def get_password():
    """
    :return: the password
    """
    return shared.get_password()

@property
def access_token():
    if is_customer_mode():
        return get_customer_token()
    else:
        return get_server_token()


def get_token():
    """
    :return: customer token if in customer mode or server token otherwise
    """
    if is_customer_mode():
        return get_customer_token()
    else:
        return get_server_token()


def set_customer_number(customer_number):
    """
    :param customer_number: set the customer number
    """
    shared.set_customer_number(customer_number)


def get_customer_number():
    """
    :return: the customer number
    """
    if is_user_mode():
        return get_customer_token()['customerNumber']
    else:
        return shared.get_customer_number()


def is_customer_mode():
    """
    :return: True if in customer mode
    """
    return shared.get_customer_number() is not None or shared.get_user_name() is not None


def is_server_mode():
    """
    :return: True if in server mode
    """
    return shared.get_customer_number() is None and shared.get_user_name() is None


def is_user_mode():
    """
    :return: True if in server mode
    """
    return shared.get_user_name() is not None


def stop():
    """
    stop and shutdown the connection.
    APIs are not accessible after this
    """
    Auth._shut_down()
    if Streaming.MarketData.active():
        Streaming.MarketData.disconnect()
