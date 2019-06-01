import pytest
from searchengine.utils import *


def test_urljoin_returns_empty_string_if_there_are_no_arguments():
    actual = urljoin()
    expected = ""
    assert actual == expected


def test_urljoin_returns_string_ending_with_slash_if_last_arg_ends_with_slash():
    base_url = "http://alexcovizzi.com/"
    path1 = "/projects/"
    path2 = "this/"
    actual = urljoin(base_url, path1, path2)
    expected = "http://alexcovizzi.com/projects/this/"
    assert actual == expected


def test_urlfix_adds_scheme_at_the_start_if_not_present():
    url = "alexcovizzi.com/projects"
    scheme = "https"
    actual = urlfix(url, scheme)
    expected = "https://alexcovizzi.com/projects"
    assert actual == expected
