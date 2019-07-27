import pytest
from torrentsearchengine.scraper import *


def test_nullelement_select_returns_empty_list():
    nullelement = NullElement()
    result = nullelement.select_elements("h2")
    assert len(result) == 0


def test_nullelement_select_one_returns_null_element():
    nullelement = NullElement()
    result = nullelement.select_one_element("h2")
    assert isinstance(result, NullElement)
