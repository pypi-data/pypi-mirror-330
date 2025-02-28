from typing import Dict, Union, Callable

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import json
from enum import Enum

import base64
import datetime, time
from gtnapi._connection import Connection
import gtnapi
import threading
import logging
import hashlib
import binascii


class Auth:
    class Statuses(Enum):
        AUTH_SUCCESS = 'AUTH_SUCCESS'
        AUTH_FAILED = 'AUTH_FAILED'
        ASSERTION_ERROR = 'ASSERTION_ERROR'
        SEVER_AUTH_FAILED = 'SEVER_AUTH_FAILED'
        CUSTOMER_AUTH_FAILED = 'CUSTOMER_AUTH_FAILED'
        SERVER_TOKEN_RENEWED = 'SERVER_TOKEN_RENEWED'
        SERVER_TOKEN_RENEW_FAILED = 'SERVER_TOKEN_RENEW_FAILED'
        CUSTOMER_TOKEN_RENEWED = 'CUSTOMER_TOKEN_RENEWED'
        CUSTOMER_TOKEN_RENEW_FAILED = 'CUSTOMER_TOKEN_RENEWED_FAILED'
        AUTH_EXPIRED = 'AUTH_EXPIRED'

    @classmethod
    def init(cls):
        if gtnapi.is_user_mode():
            return cls.init_user()
        else:
            return cls.init_institution()

    @classmethod
    def init_user(cls):
        """
        init in user/pass mode
        get the customer token only
        """

        cls.logger = logging.getLogger(__name__)

        token_status = gtnapi.Auth.Statuses.AUTH_SUCCESS.value

        status, customer_token = cls._get_customer_token_for_user(gtnapi.get_user_name(), gtnapi.get_password(),
                                                                  gtnapi.get_institution())

        if status == 200 and customer_token is not None and customer_token['status'] == 'SUCCESS':
            cls.logger.info('Customer authentication success')
            gtnapi.shared.set_customer_token(customer_token)
            cls.logger.info('GTN API initiated in Customer mode.')
        else:
            if customer_token is None:
                cls.logger.error(f"Customer authentication failed. http status {status} and token is None")
            else:
                cls.logger.error(
                    f"Customer authentication failed. status {status} and token status {customer_token['status']}")
            token_status = gtnapi.Auth.Statuses.CUSTOMER_AUTH_FAILED.value

        if token_status == gtnapi.Auth.Statuses.AUTH_SUCCESS.value:
            # start the token refresh thread
            cls._start_thread()
            pass
        else:
            if status == 200:
                status = -1

        return {'http_code': status, 'status': token_status}

    @classmethod
    def init_institution(cls):
        """
        Initialise the authentication system
            1. create the basic auth token
            2. create the assertion
            3. get the server token
            4. if customer mode, get the customer token
        """

        cls.logger = logging.getLogger(__name__)

        token_status = gtnapi.Auth.Statuses.AUTH_SUCCESS.value

        # create the basic auth
        cls._basic_auth = cls._get_basic_auth(gtnapi.get_app_key(), gtnapi.get_app_secret())

        # create the assertion
        _assertion = cls._create_token(gtnapi.get_private_key(), gtnapi.get_app_key(), gtnapi.get_institution())
        if _assertion is None:
            cls.logger.error('Assertion created failed')
            return {'http_code': -1, 'status': gtnapi.Auth.Statuses.ASSERTION_ERROR.value}

        gtnapi.set_assertion(_assertion)
        cls.logger.info('Assertion created successfully')

        # get the server token
        status, server_token = cls._get_server_token()
        if status == 200 and server_token is not None and server_token['status'] == 'SUCCESS':
            cls.logger.info('Institution authentication success')
            # server_token['accessTokenExpiresAt'] = int(
            #     (datetime.datetime.now() + datetime.timedelta(minutes=2)).timestamp() * 1000)
            gtnapi.set_server_token(server_token)
            # get the customer token
            if gtnapi.is_customer_mode():
                status, customer_token = cls._get_customer_token()
                if status == 200 and customer_token is not None and customer_token['status'] == 'SUCCESS':
                    cls.logger.info('Customer authentication success')
                    # customer_token['accessTokenExpiresAt'] = int(
                    #     (datetime.datetime.now() + datetime.timedelta(minutes=2)).timestamp() * 1000)
                    gtnapi.shared.set_customer_token(customer_token)
                    cls.logger.info('GTN API initiated in Customer mode.')
                else:
                    if customer_token is None:
                        cls.logger.error(f"Customer authentication failed. http status {status} and token is None")
                    else:
                        cls.logger.error(
                            f"Customer authentication failed. status {status} and token status {customer_token['status']}")
                    token_status = gtnapi.Auth.Statuses.CUSTOMER_AUTH_FAILED.value
            else:
                cls.logger.debug('GTN API initiated in Institution mode')
        else:
            if server_token is None:
                cls.logger.error(f"Institution authentication failed. http status {status} and token is None")
            else:
                cls.logger.error(
                    f"Institution authentication failed. http status {status} and token status {server_token['status']}")
            token_status = gtnapi.Auth.Statuses.SEVER_AUTH_FAILED.value

        if token_status == gtnapi.Auth.Statuses.AUTH_SUCCESS.value:
            # start the token refresh thread
            cls._start_thread()
        else:
            if status == 200:
                status = -1

        return {'http_code': status, 'status': token_status}

    @classmethod
    def __logout(cls):
        """
        logout the service
        """
        gtnapi.shared.destroy()

    @classmethod
    def __refresh(cls):
        """
        token refresh process
        works in a different thread
        """
        cls.logger.debug('Token refresh in progress ...')
        # if in server mode, refresh the server token
        if gtnapi.is_server_mode():
            status, server_token = cls._get_server_token_refresh()
            if status == 200:
                cls.logger.debug('Refresh server token success')
                gtnapi.set_server_token(server_token)
            else:
                cls.logger.debug('Refresh server token failed')
        else:
            # if in customer mode, refresh the server token
            status, customer_token = cls._get_customer_token_refresh()
            if status == 200:
                cls.logger.debug('Refresh customer token success')
                gtnapi.set_customer_token(customer_token)
            else:
                cls.logger.debug('Refresh customer token failed')

    @classmethod
    def _create_token(cls, private_key, app_key, institution) -> Union[Dict, None]:
        """
        Create the JWT token
        :param private_key: private key of the institute
        :param app_key: app key assigned to the institute
        :param institution: institution code
        :return: the JWT token
        """
        try:

            private_key_byte_array = cls._base16Decoder(private_key)

            # Create RSA private key object from raw bytes
            private_key = serialization.load_der_private_key(private_key_byte_array, password=None)

            issued_time = int(datetime.datetime.now().timestamp() * 1)
            expire_time = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp() * 1)

            if isinstance(private_key, rsa.RSAPrivateKey):
                access_token = jwt.encode(
                    {
                        "iss": app_key,
                        "instCode": institution,
                        "exp": expire_time,
                        "userId": '11111',
                        "iat": issued_time
                    },
                    private_key,
                    'RS256'
                )
                return access_token

        except Exception as e:
            cls.logger.exception('Error creating assertion')

        return None

    @classmethod
    def _get_server_token(cls) -> tuple[int, Union[Dict, None]]:
        """
        get the server token from the backend
        :return: the server token received
        """
        con = None
        try:
            con = Connection(gtnapi.get_api_url() + '/trade/auth/token', cls._basic_auth, gtnapi.get_app_key())
            data = {'assertion': gtnapi.get_assertion()}
            r = con.open_post(data=data)
            if r.status_code == 200:
                return r.status_code, json.loads(r.text)
            else:
                return r.status_code, None
        except Exception as e:
            cls.logger.exception(e)
            return -1, None
        finally:
            if con:
                con.close()

    @classmethod
    def _get_server_token_refresh(cls) -> tuple[int, Union[Dict, None]]:
        """
        refresh the server token
        :return: the new server token
        """
        con = None
        try:
            con = Connection(gtnapi.get_api_url() + '/trade/auth/token/refresh', None, gtnapi.get_app_key())
            data = {'refreshToken': gtnapi.get_server_token()['refreshToken']}
            r = con.open_post(data=data)
            if r.status_code == 200:
                # cls.__raise_event(gtnapi.Auth.Statuses.SERVER_TOKEN_RENEWED)
                return r.status_code, json.loads(r.text)
            else:
                # cls.__raise_event(gtnapi.Auth.Statuses.SERVER_TOKEN_RENEW_FAILED)
                return r.status_code, None
        except Exception as e:
            cls.logger.exception(e)
            # cls.__raise_event(gtnapi.Auth.Statuses.SERVER_TOKEN_RENEW_FAILED)
            return -1, None
        finally:
            if con:
                con.close()

    @classmethod
    def _get_customer_token(cls) -> tuple[int, Union[Dict, None]]:
        """
        get the customer token from the backend
        :return: the customer token received
        """
        con = None
        try:
            con = Connection(gtnapi.get_api_url() + '/trade/auth/customer/token', cls._basic_auth, gtnapi.get_app_key())
            data = {'customerNumber': gtnapi.get_customer_number(), 'accessToken': gtnapi.get_server_token()['accessToken']}
            r = con.open_post(data=data)
            if r.status_code == 200:
                cls.logger.debug(f"Customer Token:{r.text}")
                return r.status_code, json.loads(r.text)
            else:
                return r.status_code, None
        except Exception as e:
            cls.logger.exception(e)
            return -1, None
        finally:
            if con:
                con.close()

    @classmethod
    def _get_customer_token_refresh(cls) -> tuple[int, Union[Dict, None]]:
        """
        refresh the customer token
        :return: the new customer token
        """
        con = None
        try:
            con = Connection(gtnapi.get_api_url() + '/trade/auth/customer/token/refresh', None, gtnapi.get_app_key())
            data = {'refreshToken': gtnapi.get_customer_token()['refreshToken']}
            r = con.open_post(data=data)
            if r.status_code == 200:
                cls.logger.debug(f"New Customer Token: {r.text}")
                # cls.__raise_event(gtnapi.Auth.Statuses.CUSTOMER_TOKEN_RENEWED)
                return r.status_code, json.loads(r.text)
            else:
                # cls.__raise_event(gtnapi.Auth.Statuses.CUSTOMER_TOKEN_RENEW_FAILED)
                return r.status_code, None
        except Exception as e:
            cls.logger.exception(e)
            # cls.__raise_event(gtnapi.Auth.Statuses.CUSTOMER_TOKEN_RENEW_FAILED)
            return -1, None
        finally:
            if con:
                con.close()

    @classmethod
    def _get_customer_token_for_user(cls, user: str, passw: str, institution: str) -> tuple[int, Union[Dict, None]]:
        """
        get the customer token from the backend
        :return: the customer token received
        """
        con = None
        try:
            encoded_pw = cls.hash_password(passw)
            con = Connection(gtnapi.get_api_url() + '/trade/auth/user-login', None, gtnapi.get_app_key())
            data = {'loginName': user, 'password': encoded_pw, 'institutionCode': institution, 'encryptionType': 2}
            r = con.open_post(data=data)
            if r.status_code == 200:
                cls.logger.debug(f"Customer Token:{r.text}")
                return r.status_code, json.loads(r.text)
            else:
                return r.status_code, None
        except Exception as e:
            cls.logger.exception(e)
            return -1, None
        finally:
            if con:
                con.close()

    @classmethod
    def _base16Decoder(cls, hex_string):
        bts = bytearray(len(hex_string) // 2)
        for i in range(len(bts)):
            bts[i] = int(hex_string[2 * i:2 * i + 2], 16)
        return bytes(bts)

    @classmethod
    def _base16Encoder(cls, digestMsgByte):
        verifyMsg = ""
        for i in range(len(digestMsgByte)):
            hexChar = digestMsgByte[i] & 0xFF
            hexString = hex(hexChar)[2:]
            if len(hexString) == 1:
                verifyMsg += "0"
            verifyMsg += hexString
        return verifyMsg

    @classmethod
    def _get_basic_auth(cls, username, password) -> str:
        """
        create the basic auth token
        :param username: user name
        :param password: password
        :return:
        """
        token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    @property
    def basic_auth(self):
        return self._basic_auth

    @classmethod
    def _key_refresh(cls):
        """
        token refresh thread
        refreshes the token within last 100 seconds of the token lifetime
        """
        while cls.__thread_active:
            try:
                if gtnapi.is_server_mode():
                    token = gtnapi.get_server_token()
                    # check the refresh token validity first
                    expire_time = datetime.datetime.fromtimestamp(int(token['refreshTokenExpiresAt']) / 1000)
                    delta = (expire_time - datetime.datetime.now()).total_seconds()
                    cls.logger.debug(f'Time delta - server refresh token:  {delta}')
                    if delta < 50:
                        # refresh token no longer valid. must logout
                        cls._shut_down()
                        gtnapi.Auth.__logout()
                        # cls.__raise_event(gtnapi.Auth.Statuses.AUTH_EXPIRED)
                    else:
                        # refresh token valid lets check the access token
                        expire_time = datetime.datetime.fromtimestamp(int(token['accessTokenExpiresAt']) / 1000)
                        delta = (expire_time - datetime.datetime.now()).total_seconds()
                        cls.logger.debug(f'Time delta server access token: {delta}')
                        if 0 < delta < 100:
                            cls.logger.debug(f'refreshing institution access token')
                            status, server_token = cls._get_server_token_refresh()
                            if status == 200:
                                cls.logger.debug(f'refreshing institution access token successful')
                                # server_token['refreshTokenExpiresAt'] = int(
                                #     (datetime.datetime.now() + datetime.timedelta(minutes=2)).timestamp() * 1000)
                                gtnapi.shared.set_server_token(server_token)
                                cls._print_token()
                            else:
                                cls.logger.debug(f'Error refreshing the token: {delta}')
                else:
                    token = gtnapi.get_customer_token()
                    # check the refresh token validity first
                    expire_time = datetime.datetime.fromtimestamp(int(token['refreshTokenExpiresAt']) / 1000)
                    delta = (expire_time - datetime.datetime.now()).total_seconds()
                    cls.logger.debug(f'Time delta - customer refresh token: {delta}')
                    if delta < 50:
                        # refresh token no longer valid. must logout
                        cls._shut_down()
                        gtnapi.Auth.__logout()
                        # cls.__raise_event(gtnapi.Auth.Statuses.AUTH_EXPIRED)
                    else:
                        # refresh token valid lets check the access token
                        expire_time = datetime.datetime.fromtimestamp(int(token['accessTokenExpiresAt']) / 1000)
                        delta = (expire_time - datetime.datetime.now()).total_seconds()
                        cls.logger.debug(f'Time delta customer access token: {delta}')
                        if 0 < delta < 100:
                            cls.logger.debug(f'refreshing customer access token')
                            status, customer_token = cls._get_customer_token_refresh()
                            if status == 200:
                                cls.logger.debug(f'refreshing customer access token successful')
                                # customer_token['refreshTokenExpiresAt'] = int(
                                #     (datetime.datetime.now() + datetime.timedelta(minutes=2)).timestamp() * 1000)
                                gtnapi.shared.set_customer_token(customer_token)
                                cls._print_token()
                            else:
                                cls.logger.debug(f'Error refreshing the token: {status}')
            except Exception as e:
                cls.logger.exception(e)

            time.sleep(10)

        cls.logger.debug('Key rotation thread exit!')

    @classmethod
    def _start_thread(cls):
        """
        start the token refresh thread
        """
        cls.logger.debug('Starting refresh thread')
        cls.__thread_active = True
        cls.t = threading.Thread(target=cls._key_refresh)
        cls.t.start()

    @classmethod
    def _print_token(cls):
        if gtnapi.is_server_mode():
            token = gtnapi.get_server_token()
        else:
            token = gtnapi.get_customer_token()
        cls.logger.debug(json.dumps(token, indent=4))
        cls.logger.debug('Access', token['accessToken'])
        cls.logger.debug("Access expire", datetime.datetime.fromtimestamp(int(token['accessTokenExpiresAt']) / 1000))
        cls.logger.debug('Refresh', token['refreshToken'])
        cls.logger.debug("Refresh expire", datetime.datetime.fromtimestamp(int(token['refreshTokenExpiresAt']) / 1000))

        # print("------ customer details ------")
        # status, details = gtnapi.Customer.get_details('949316473')
        # print(json.dumps(details, indent=4))

    @classmethod
    def _shut_down(cls):
        """
        stop the refresh thread
        """
        cls.__logout()
        cls.__thread_active = False
        cls.logger.info('GTN API session terminated')

    @classmethod
    def hash_password(cls, password: str) -> Union[str, None]:
        salt = b"MUBASHER"  # Convert the salt to bytes
        iterations = 10000
        key_length = 64  # 512 bits / 8 = 64 bytes

        try:
            # Derive the key using PBKDF2 with HMAC-SHA-512
            hash_bytes = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, iterations, key_length)

            # Convert the resulting byte array into a hexadecimal string
            return binascii.hexlify(hash_bytes).decode()
        except Exception as e:
            cls.logger.exception(f"Error obtaining hashPassword: {e}")
            return None
