import hashlib
import hmac
import json
import logging
import time
from json import JSONDecodeError
from threading import Thread
from urllib.parse import urlencode

import requests
import websocket

from tabdeal.enums import RequestTypes, SecurityTypes
from tabdeal.exceptions import (
    ClientException,
    SecurityException,
    ServerException,
    UnStructuredResponseException,
)

logger = logging.getLogger(__name__)


class Client(object):
    """
    Tabdeal API Client

    Keyword Args:
        base_url (str, optional): API Base URL. Default: https://api.tabdeal.org
        version (str, optional): API Version. Default: v1
        api_key (str, optional): API Key To Authenticate. Default: None
        api_key (str, optional): API Secret To Authenticate. Default: None
        timeout (int, optional): Request Timeout. Default: None
        receive_window (int, optional): Milliseconds Request IS Valid. Default: None
    """

    def __init__(
        self,
        api_key=None,
        api_secret=None,
        base_url="https://api1.tabdeal.org",
        version="v1",
        timeout=None,
        receive_window=None,
    ):
        self.base_url = f"{base_url}/api/{version}/"
        self.base_read_url = f"{base_url}/r/api/{version}/"
        self.version = version
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.receive_window = receive_window
        self.session = requests.Session()

    def request(
        self,
        url: str,
        method: RequestTypes = RequestTypes.GET,
        security_type: SecurityTypes = SecurityTypes.NONE,
        data: dict = dict(),
        headers: dict = dict(),
    ):
        self._check_security_requirements(security_type)
        self._set_security_header(headers, security_type)
        self._update_session_headers(headers)
        self._set_security_data(data, security_type)

        if method == RequestTypes.GET:
            response = self._get(url, params=data)
        elif method == RequestTypes.POST:
            response = self._post(url, data=data)
        elif method == RequestTypes.DELETE:
            response = self._delete(url, params=data)
        elif method == RequestTypes.PUT:
            response = self._put(url, data=data)

        return self._handle_response(response)

    def _check_security_requirements(self, security_type: SecurityTypes):
        if security_type == SecurityTypes.TRADE:
            if not self.api_key or not self.api_secret:
                raise SecurityException("'api-key' and 'api-secret' must provided")

    def _get(self, url, params: dict = dict()):
        return self.session.get(self.base_read_url + url, params=params)

    def _post(self, url, data: dict = dict()):
        return self.session.post(self.base_url + url, data=data)

    def _delete(self, url, params: dict = dict()):
        return self.session.delete(self.base_url + url, params=params)

    def _put(self, url, data: dict = dict()):
        return self.session.put(self.base_url + url, data=data)

    def _handle_response(self, response):
        if response.status_code < 400:
            return self._get_response_json(response)
        elif 400 <= response.status_code < 500:
            js = self._get_response_json(response)
            raise ClientException(
                status=response.status_code,
                message=js["msg"],
                code=js["code"],
                detail=js.get("detail", None),
            )
        else:
            raise ServerException(status=response.status_code, message=response.text)

    def _get_response_json(self, response):
        try:
            return response.json()
        except JSONDecodeError:
            raise UnStructuredResponseException(response.status_code, response.text)

    def _set_security_header(self, headers: dict, security_type: SecurityTypes):
        if security_type in [SecurityTypes.TRADE, SecurityTypes.USER_STREAM]:
            headers.update({"X-MBX-APIKEY": self.api_key})

    def _set_security_data(self, data: dict, security_type: SecurityTypes):
        if security_type == SecurityTypes.TRADE:
            timestamp = time.time() * 1000
            data.update({"timestamp": timestamp})

            if self.receive_window:
                data.update({"recvWindow": self.receive_window})

            data_query = urlencode(data)
            signature = hmac.new(
                self.api_secret.encode("utf-8"),
                data_query.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            data.update({"signature": signature})

    def _update_session_headers(self, headers):
        self.session.headers.update(headers)


class TabdealWebsocketClientThread(Thread):
    def __init__(self, callback, stream=None, payload=None):
        self.payload = payload
        self.callback = callback
        self.base_url = "wss://api.tabdeal.org/stream/"

        if stream:
            url = self.base_url + f"?streams={stream}"
        else:
            url = self.base_url

        self.ws = websocket.WebSocketApp(
            url=url, on_message=self.on_message, on_open=self.on_open
        )

        super().__init__()

    def on_open(self, ws):
        logger.debug("Websocket connected....")
        if self.payload:
            self.ws.send(json.dumps(self.payload))

    def on_message(self, ws, message):
        self.callback(message)

    def run(self):
        self.ws.run_forever()

    def join(self, timeout=None):
        self.ws.close()
        super().join(timeout=timeout)
        logger.debug("Websocket disconnected ...")
