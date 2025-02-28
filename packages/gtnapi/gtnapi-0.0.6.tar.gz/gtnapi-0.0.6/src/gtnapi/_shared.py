class Shared:

    @classmethod
    def init(cls, api_url, app_key: str, app_secret: str, private_key: str,
             institution: str, customer_number: str, user: str, password: str):
        cls._api_url = api_url
        cls._app_key = app_key
        cls._app_secret = app_secret
        cls._private_key = private_key
        cls._institution = institution
        cls._customer_number = customer_number
        cls._customer_token = None
        cls._server_token = None
        cls._user = user
        cls._password = password
        cls._ready = True

    @classmethod
    def destroy(cls):
        cls._ready = False
        cls._api_url = None
        cls._app_key = None
        cls._app_secret = None
        cls._private_key = None
        cls._institution = None
        cls._customer_number = None
        cls._customer_token = None
        cls._server_token = None

    @classmethod
    def set_assertion(cls, assertion):
        cls._assertion = assertion

    @classmethod
    def get_assertion(cls):
        return cls._assertion

    @classmethod
    def set_server_token(cls, server_token):
        cls._server_token = server_token

    @classmethod
    def get_server_token(cls):
        return cls._server_token

    @classmethod
    def set_customer_token(cls, customer_token):
        cls._customer_token = customer_token

    @classmethod
    def get_customer_token(cls):
        return cls._customer_token

    @classmethod
    def get_api_url(cls):
        return cls._api_url

    @classmethod
    def get_app_key(cls):
        return cls._app_key

    @classmethod
    def get_app_secret(cls):
        return cls._app_secret

    @classmethod
    def get_private_key(cls):
        return cls._private_key

    @classmethod
    def get_institution(cls):
        return cls._institution

    @classmethod
    def print(cls):
        print('App Key: ', cls._app_key)

    @classmethod
    def set_customer_number(cls, customer_number):
        cls._customer_number = customer_number

    @classmethod
    def get_customer_number(cls):
        return cls._customer_number

    @classmethod
    def get_user_name(cls):
        return cls._user

    @classmethod
    def get_password(cls):
        return cls._password
