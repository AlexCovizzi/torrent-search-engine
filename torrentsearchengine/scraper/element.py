from typing import Union, Any, Optional, List
from bs4 import BeautifulSoup, Tag
from .selector import Selector
from .attribute import Attribute, NullAttribute


class Element:

    def __init__(self, parser: Optional[Tag] = None):
        self.parser = parser

    def select(self, selector: Union[Selector, str]="",
               limit: int = 0) -> List["Element"]:
        if not self.parser or not selector:
            return []

        if isinstance(selector, str):
            selector = Selector.parse(selector)

        try:
            tags = self.parser.select(selector.css, limit=limit)
        except ValueError:
            tags = []

        elements = [Element(tag) for tag in tags]

        return elements

    def select_one(self, selector: Union[Selector, str]="") -> "Element":
        if not self.parser or not selector:
            return NullElement()

        if isinstance(selector, str):
            selector = Selector.parse(selector)

        try:
            tag = self.parser.select_one(selector.css)
        except ValueError:
            tag = None

        element = Element(tag) if tag else NullElement()

        return element

    def attr(self, attr: str = 'text') -> Attribute:
        if not self.parser:
            return NullAttribute()

        if attr == 'text' or attr == '':
            return Attribute(self.parser.text)

        return Attribute(self.parser.get(attr, ''))

    def __str__(self):
        return str(self.parser)


class NullElement(Element):

    def __init__(self):
        super(NullElement, self).__init__(None)
