from unittest.mock import patch, Mock
import requests
import os
from helpers.http_server import HTTPServer
from torrentsearchengine.websiteprovider import WebsiteTorrentProvider

"""
@patch('requests.get')
def test_get(requests_get_mock: Mock):
    requests.get('https://github.com/')
    requests_get_mock.assert_called_once_with('https://github.com/')
"""


def test_server():
    server = HTTPServer().serve("127.0.0.1", 8000, content="Funziona")
    assert requests.get('http://127.0.0.1:8000').text == "Funziona"
    server.shutdown()
