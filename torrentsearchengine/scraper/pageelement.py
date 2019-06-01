from typing import Union, Any, Optional, List
from bs4 import BeautifulSoup, Tag
from torrentsearchengine.scraper.selector import Selector
from torrentsearchengine.scraper.attribute import Attribute, NullAttribute


class PageElement:

    def __init__(self, parser: Optional[Tag] = None):
        self.parser = parser

    def select(self, selector: Union[Selector, str] = "", limit: int = 0) -> List["PageElement"]:
        if not self.parser or not selector:
            return []

        selector = selector if isinstance(selector, Selector) else Selector.parse(selector)

        try:
            tags = self.parser.select(selector.css, limit=limit)
        except ValueError:
            tags = []

        elements = [PageElement(tag) for tag in tags]

        return elements

    def select_one(self, selector: Union[Selector, str] = '') -> "PageElement":
        if not self.parser or not selector:
            return NullPageElement()

        selector = selector if isinstance(selector, Selector) else Selector.parse(selector)

        try:
            tag = self.parser.select_one(selector.css)
        except ValueError:
            tag = None

        element = PageElement(tag) if tag else NullPageElement()

        return element

    def attr(self, attr: str = 'text') -> Attribute:
        if not self.parser:
            return NullAttribute()

        if attr == 'text' or attr == '':
            return Attribute(self.parser.text)

        return Attribute(self.parser.get(attr, ''))

    def __str__(self):
        return str(self.parser)


class NullPageElement(PageElement):

    def __init__(self):
        super(NullPageElement, self).__init__(None)
