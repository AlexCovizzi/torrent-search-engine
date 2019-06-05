from unittest.mock import patch, Mock
import requests
from torrentsearchengine.websiteprovider import WebsiteTorrentProvider


@patch('requests.get')
def test_get(requests_get_mock: Mock):
    requests.get('https://github.com/')
    requests_get_mock.assert_called_once_with('https://github.com/')

