import pytest
from torrentsearchengine.scraper.attribute import *


def test_to_string_returns_value_as_string():
    val = 4
    attr = Attribute(val)
    assert attr.to_string() == "4"


def test_to_string_returns_default_if_value_is_none():
    val = None
    default = "dflt"
    attr = Attribute(val)
    assert attr.to_string(default=default) == default


def test_to_int_returns_value_as_int():
    val = "4"
    attr = Attribute(val)
    assert attr.to_int() == 4


def test_to_int_returns_default_if_value_cannot_be_converted_to_int():
    val = "ciao"
    default = 4
    attr = Attribute(val)
    assert attr.to_int(default=default) == default


def test_re_returns_the_substring_that_matches_the_regex():
    val = "ciao123"
    attr = Attribute(val)
    regex = r"[a-z]+"
    assert attr.re(regex) == "ciao"


def test_re_returns_the_value_as_string_if_regex_is_empty():
    val = 1234
    attr = Attribute(val)
    assert attr.re("") == "1234"
