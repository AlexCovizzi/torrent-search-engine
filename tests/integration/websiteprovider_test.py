import pytest
import requests
import os
from helpers.httpserver import httpserver
from torrentsearchengine import *

"""
@patch('requests.get')
def test_get(requests_get_mock: Mock):
    requests.get('https://github.com/')
    requests_get_mock.assert_called_once_with('https://github.com/')
"""


def test_fetch_raises_TimeoutError():
    content = "<html></html>"
    with httpserver("127.0.0.1", 8000, content=content, timeout=2):
        provider = TorrentProvider("name", "fullname", "http://127.0.0.1:8000")
        with pytest.raises(Timeout):
            provider.fetch("/", timeout=1)
