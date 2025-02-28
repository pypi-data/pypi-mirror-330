import json
import threading
from typing import Union
import gtnapi

import websocket


class Streaming:
    class MarketData:

        __active: bool

        @classmethod
        def __open_connection(cls, on_open, on_message, on_error, on_close):
            """
            open the websocket connection
            :param on_open: method reference
            :param on_message: method reference
            :param on_error: method reference
            :param on_close: method reference
            :return:
            """
            cls.__on_open = on_open
            cls.__on_message = on_message
            cls.__on_error = on_error
            cls.__on_close = on_close
            websocket.enableTrace(False)
            cls.__ws = websocket.WebSocketApp('wss' + gtnapi.get_api_url()[5:] + "/market-data/websocket/price",
                                              on_open=cls.on_open,
                                              on_message=cls.on_message,
                                              on_error=cls.on_error,
                                              on_close=cls.on_close)

            cls.__active = True
            cls.__ws.run_forever()
            cls.__active = False

        @classmethod
        def connect(cls, on_open, on_message, on_error, on_close):
            """
            Start the websocket thred
            :param on_open: method reference
            :param on_message: method reference
            :param on_error: method reference
            :param on_close: method reference
            :return:
            """
            t = threading.Thread(target=cls.__open_connection, args=(on_open, on_message, on_error, on_close))
            t.start()

        @classmethod
        def disconnect(cls):
            """
            disconnect the socket on demand
            :return:
            """
            cls.__active = False
            cls.__ws.close()

        @classmethod
        def on_open(cls, ws):
            """
            on open event handler
            :param ws: web socket reference
            """
            ws.send(f'{{ "token": {gtnapi.get_token()["accessToken"]} }}')
            cls.__on_open()

        @classmethod
        def on_message(cls, ws, message):
            """
            on message event handler
            :param ws: web socket reference
            :param message: message received
            """
            cls.__on_message(message)

        @classmethod
        def on_error(cls, ws, error):
            """
            on open error handler
            :param ws: web socket reference
            :param error: error message
            """
            cls.__on_error(error)

        @classmethod
        def on_close(cls, ws, close_status_code, close_msg):
            """
            on close event handler
            :param ws: web socket reference
            :param close_status_code: code
            :param close_msg: closing message
            """
            cls.__active = False
            cls.__on_close(close_status_code, close_msg)

        @classmethod
        def send_message(cls, message: Union[dict, str]):
            """
            sends a message via the web socket
            :param message: to be sent
            """
            if type(message) is dict:
                cls.__ws.send_text(json.dumps(message))
            else:
                cls.__ws.send_text(message)

        @classmethod
        def active(cls):
            """
            :return: True if market data streaming is active
            """
            try:
                return cls.__active
            except Exception as e:
                return False

    class TadeData:
        __active: bool

        @classmethod
        def __open_connection(cls, on_open, on_message, on_error, on_close):
            """
            open the websocket connection
            :param on_open: method reference
            :param on_message: method reference
            :param on_error: method reference
            :param on_close: method reference
            :return:
            """
            cls.__on_open = on_open
            cls.__on_message = on_message
            cls.__on_error = on_error
            cls.__on_close = on_close
            websocket.enableTrace(False)
            cls.__ws = websocket.WebSocketApp('wss' + gtnapi.get_api_url()[5:] + "/trade/websocket/v1.2.1",
                                              on_open=cls.on_open,
                                              on_message=cls.on_message,
                                              on_error=cls.on_error,
                                              on_close=cls.on_close)

            cls.__active = True
            cls.__ws.run_forever()
            cls.__active = False

        @classmethod
        def connect(cls, on_open, on_message, on_error, on_close):
            """
            Start the websocket thred
            :param on_open: method reference
            :param on_message: method reference
            :param on_error: method reference
            :param on_close: method reference
            :return:
            """
            t = threading.Thread(target=cls.__open_connection, args=(on_open, on_message, on_error, on_close))
            t.start()

        @classmethod
        def disconnect(cls):
            """
            disconnect the socket on demand
            :return:
            """
            cls.__active = False
            cls.__ws.close()

        @classmethod
        def on_open(cls, ws):
            """
            on open event handler
            :param ws: web socket reference
            """
            ws.send(f'{{ "token": {gtnapi.get_token()["accessToken"]} }}')
            print('{ "token": "' + gtnapi.get_customer_token()["accessToken"] + '"}')
            cls.__on_open()

        @classmethod
        def on_message(cls, ws, message):
            """
            on message event handler
            :param ws: web socket reference
            :param message: message received
            """
            cls.__on_message(message)

        @classmethod
        def on_error(cls, ws, error):
            """
            on open error handler
            :param ws: web socket reference
            :param error: error message
            """
            cls.__on_error(error)

        @classmethod
        def on_close(cls, ws, close_status_code, close_msg):
            """
            on close event handler
            :param ws: web socket reference
            :param close_status_code: code
            :param close_msg: closing message
            """
            cls.__active = False
            cls.__on_close(close_status_code, close_msg)

        @classmethod
        def send_message(cls, message: Union[dict, str]):
            """
            sends a message via the web socket
            :param message: to be sent
            """
            if type(message) is dict:
                cls.__ws.send_text(json.dumps(message))
            else:
                cls.__ws.send_text(message)

        @classmethod
        def active(cls):
            """
            :return: True if market data streaming is active
            """
            try:
                return cls.__active
            except Exception as e:
                return False
