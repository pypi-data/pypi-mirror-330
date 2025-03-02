from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import requests
from requests import Response


# -----------------------------------------------------------

class Method(Enum):
    GET = 'GET'
    POST = 'POST'


@dataclass
class Endpoint:
    ip : str
    port : int
    path : str

    @classmethod
    def make_localhost(cls, port : int, path : str):
        return cls(ip='127.0.0.1', port=port, path=path)

    def get_url(self, protocol : str) -> str:
        socket_addr = f'{protocol}://{self.ip}:{self.port}'
        return f'{socket_addr}{self.path}'

    def get(self, secure : bool = True) -> Response:
        protocol = 'https' if secure else 'http'
        url = self.get_url(protocol=protocol)
        print(f'Making get request to {url}')
        return requests.get(url)

    def post(self, msg : str, secure : bool = True) -> Response:
        protocol = 'https' if secure else 'http'
        url = self.get_url(protocol=protocol)
        print(f'Making post request to {url}')
        return requests.post(self.get_url(protocol=protocol), data=msg)
