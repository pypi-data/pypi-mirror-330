import json

import requests
from urllib.parse import urlencode


class Connection:
    """
    Connection object to keep the http connection alive
    for the performance
    """

    def __init__(self, url, auth_token, throttle_key):
        self.url = url

        self.http_session = requests.Session()
        self.http_session.keep_alive = False
        if auth_token:
            self.http_session.headers.update(
                {'Authorization': auth_token, 'Throttle-Key': throttle_key, 'Content-Type': 'application/json'})
        else:
            self.http_session.headers.update(
                {'Throttle-Key': throttle_key, 'Content-Type': 'application/json'})

    def open_post(self, data):
        """
        Open the http connection
        """
        response = self.http_session.post(self.url, json.dumps(data))
        return response

    def open_get(self, data):
        """
        Open the http connection
        """
        response = self.http_session.get(self.url, params=data)
        return response

    def open_patch(self, data):
        """
        Open the http connection
        """
        response = self.http_session.patch(self.url, json.dumps(data))
        return response

    def open_delete(self, data):
        """
        Open the http connection
        """
        response = self.http_session.delete(self.url, params=urlencode(data))
        return response

    def close(self):
        """
        close the http session
        """
        self.http_session.close()
