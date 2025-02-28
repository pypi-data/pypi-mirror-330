from gtnapi._connection import Connection
import gtnapi
import json
from typing import Optional, Union


class Requests:

    @classmethod
    def __send_request(cls, method, endpoint, params) -> tuple[int, Union[dict, None]]:
        """
        send a request to the backend
        :param method: HTTP method
        :param endpoint: endpoint to call
        :param params: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        con = None
        try:
            # make sure to begin with a '/'
            if not endpoint[0] == '/':
                endpoint = '/' + endpoint

            con = Connection(gtnapi.get_api_url() + endpoint,
                             'Bearer ' + gtnapi.get_token()['accessToken'],
                             gtnapi.get_app_key())
            if method == 'POST':
                r = con.open_post(params)
            elif method == 'GET':
                r = con.open_get(params)
            elif method == 'PATCH':
                r = con.open_patch(params)
            elif method == 'DELETE':
                r = con.open_delete(params)
            else:
                return 405, {
                    "status": "FAILED",
                    "reason": "unknown method: " + method}

            if r.status_code == 200:
                return r.status_code, json.loads(r.text)
            else:
                try:
                    return r.status_code, json.loads(r.text)
                except Exception as e:
                    # possible JSON decode error
                    return r.status_code, {}
        except Exception as e:
            print(e)
            return -1, None
        finally:
            if con:
                con.close()

    @classmethod
    def get(cls, endpoint: str, **kwargs) -> tuple[int, Union[dict, None]]:
        """
        call to the HTTP GET method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("GET", endpoint, kwargs)

    @classmethod
    def post(cls, endpoint: str, **kwargs) -> tuple[int, Union[dict, None]]:
        """
        call to the HTTP POST method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("POST", endpoint, kwargs)

    @classmethod
    def patch(cls, endpoint: str, **kwargs) -> tuple[int, Union[dict, None]]:
        """
        call to the HTTP PATCH method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("PATCH", endpoint, kwargs)

    @classmethod
    def delete(cls, endpoint: str, **kwargs) -> tuple[int, Union[dict, None]]:
        """
        call to the HTTP DELETE method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("DELETE", endpoint, kwargs)
