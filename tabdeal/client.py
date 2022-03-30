import hashlib
import hmac
import time
from json import JSONDecodeError
from urllib.parse import urlencode

import requests

from tabdeal.enums import RequestTypes, SecurityTypes
from tabdeal.exceptions import (
    ClientException,
    ServerException,
    UnStructuredResponseException,
)


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
        base_url="https://api.tabdeal.org",
        version="v1",
        api_key=None,
        api_secret=None,
        timeout=None,
        receive_window=None,
    ):
        self.base_url = f"{base_url}/api/{version}/"
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
        self._set_security_header(headers, security_type)
        self._update_session_headers(headers)
        self._set_security_data(data, security_type)

        if method == RequestTypes.GET:
            response = self._get(url, params=data)
        elif method == RequestTypes.POST:
            response = self._post(url, data=data)
        elif method == RequestTypes.DELETE:
            response = self._delete(url, params=data)

        return self._handle_response(response)

    def _get(self, url, params: dict = dict()):
        return self.session.get(self.base_url + url, params=params)

    def _post(self, url, data: dict = dict()):
        return self.session.post(self.base_url + url, data=data)

    def _delete(self, url, params: dict = dict()):
        return self.session.delete(self.base_url + url, params=params)

    def _handle_response(self, response):
        if response.status_code < 400:
            return self._get_response_json(response)
        elif 400 <= response.status_code < 500:
            js = self._get_response_json(response)
            raise ClientException(
                status=response.status_code, message=js["msg"], code=js["code"]
            )
        else:
            raise ServerException(status=response.status_code, message=response.text)

    def _get_response_json(self, response):
        try:
            return response.json()
        except JSONDecodeError:
            raise UnStructuredResponseException(response.status_code, response.text)

    def _set_security_header(self, headers: dict, security_type: SecurityTypes):
        if security_type == SecurityTypes.TRADE:
            headers.update({"api-key": self.api_key})

    def _set_security_data(self, data: dict, security_type: SecurityTypes):
        if security_type == SecurityTypes.TRADE:
            timestamp = time.time() * 1000
            data.update({"timestamp": timestamp})

            data_query = urlencode(data)
            signature = hmac.new(
                self.api_secret.encode("utf-8"),
                data_query.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            data.update({"signature": signature})

            if self.receive_window:
                data.update({"recvWindow": self.receive_window})

    def _update_session_headers(self, headers):
        self.session.headers.update(headers)
