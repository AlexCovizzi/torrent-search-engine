import pytest
from torrentsearchengine.scraper.selector import *


def test_parse_returns_the_correct_selector():
    s = "parent > child:focus@ text| re: [A-Z]+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr == "text"
    assert selector.re == "[A-Z]+"
    assert selector.fmt is None


def test_parse_returns_selector_with_no_attr():
    s = "parent > child:focus | fmt: \\1he |re: \\w+ | "
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr is None
    assert selector.re == "\\w+"
    assert selector.fmt == "\\1he"


def test_parse_returns_selector_with_no_re():
    s = "parent > .child:focus@ text| no: \\w+"
    selector = Selector.parse(s)
    assert selector.css == "parent > .child:focus"
    assert selector.attr == "text"
    assert selector.re is None
    assert selector.fmt is None


def test_parse_returns_selector_with_no_attr_and_re():
    s = "parent > child:focus | fmt: "
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr is None
    assert selector.re is None
    assert selector.fmt == ""


def test_parse_string_with_brackets():
    s = "parent > child:focus @ text | re: (\w+|\s)+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr == "text"
    assert selector.re == "(\w+|\s)+"


def test_parse_string_with_escaped_brackets():
    s = "parent > child:focus @ text | re: \(ciao | fmt: hey\)+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr == "text"
    assert selector.re == "\(ciao"
    assert selector.fmt == "hey\)+"


def test_parse_string_with_escaped_pipe_char():
    s = "parent > child:focus @ text | re: (ciao\|)+"
    selector = Selector.parse(s)
    assert selector.css == "parent > child:focus"
    assert selector.attr == "text"
    assert selector.re == "(ciao\|)+"
