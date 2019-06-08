import pytest
from torrentsearchengine.scraper.selector import *


def test_parse_returns_the_correct_selector():
    s = "parent > child:focus@ text| re: \\w+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr == "text"
    assert selector.re == "\\w+"


def test_parse_returns_selector_with_no_attr():
    s = "parent > child:focus | re: \\w+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr is None
    assert selector.re == "\\w+"


def test_parse_returns_selector_with_no_re():
    s = "parent > .child:focus@ text| no: \\w+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr == "text"
    assert selector.re is None


def test_parse_returns_selector_with_no_attr_and_re():
    s = "parent > child:focus"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr is None
    assert selector.re is None
