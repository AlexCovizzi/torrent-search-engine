from unittest.mock import patch, Mock
import requests

@patch('requests.get')
def test_get(requests_get_mock: Mock):
    requests.get('https://github.com/')
    requests_get_mock.assert_called_once_with('https://github.com/')