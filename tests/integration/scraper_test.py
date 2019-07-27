import pytest
from torrentsearchengine.scraper import *


html = """
<body>
    <div class="example">
        <input type="text" />
        <input type="button" />
    </div>
</body>
"""


def test_select_elements_should_return_an_array_of_elements_that_matches_the_selector():
    scraper = Scraper(html)
    elements = scraper.select_elements("div.example > input")
    assert str(elements[0]) == '<input type="text"/>'
    assert str(elements[1]) == '<input type="button"/>'


def test_select_elements_should_return_an_empty_array_if_no_element_matches_selector():
    scraper = Scraper(html)
    elements = scraper.select_elements("div.example > span")
    assert len(elements) == 0


def test_select_one_element_should_return_the_first_element_that_matches_the_sel():
    scraper = Scraper(html)
    element = scraper.select_one_element("div.example > input")
    assert str(element) == '<input type="text"/>'


def test_select_one_element_should_return_NullElement_if_no_element_matches_the_sel():
    scraper = Scraper(html)
    element = scraper.select_one_element("div.example > span")
    assert str(element) == "None"
