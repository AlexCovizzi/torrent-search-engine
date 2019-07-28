import pytest
import requests
import os
from helpers.httpserver import httpserver
from torrentsearchengine import *


HOST = "127.0.0.1"
PORT = 8082
BASE_URL = "http://{}:{}".format(HOST, PORT)


provider_dict = {
    "name": "provider",
    "url": BASE_URL,
    "search": "/{query}",
    "list": {
        "items": "table > tr.item",
        "next": "a.next @ href",
        "item": {
            "name": "td.name @ text",
            "info_url": "td.info_url > a @ href",
            "time": "td.time @ text",
            "size": "td.size @ text",
            "seeds": "td.seeds @ text @ text | re: ([0-9]+)",
            "leeches": "td.leeches @ text | re: ([0-9]+)"
        }
    },
    "item": {
        "link": "a.link @ href"
    }
}

"""
def test_new_TorrentProvider():
    provider = TorrentProvider(**provider_dict)
    assert provider.name == "provider"
    assert provider.fullname == "provider"
    assert provider.url == "https://{}:{}".format(HOST, PORT)
    assert provider.search_path == "/{query}"
"""


def test_fetch_returns_response():
    content = "<html></html>"
    with httpserver(HOST, PORT, content=content):
        provider = TorrentProvider(validate=False, name="name", url=BASE_URL)
        assert provider.fetch("/").text == content


def test_fetch_raises_TimeoutError():
    content = "<html></html>"
    with httpserver(HOST, PORT, content=content, timeout=2):
        provider = TorrentProvider(validate=False, name="name", url=BASE_URL)
        with pytest.raises(Timeout):
            provider.fetch("/", timeout=1)


def test_fetch_raises_RequestError():
    provider = TorrentProvider(validate=False, name="name", url=BASE_URL)
    with pytest.raises(RequestError):
        provider.fetch("/")
