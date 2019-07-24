from typing import Union, Any, Optional, List
from bs4 import BeautifulSoup, Tag
from .selector import Selector, NullSelector
from .attribute import Attribute, NullAttribute


class Element:

    def __init__(self, parser: Optional[Tag] = None):
        self.parser = parser

    def select(self, selector: Union[Selector, str], limit: int = 0):
        if not self.parser or not selector:
            return []

        if isinstance(selector, str):
            selector = Selector.parse(selector)

        try:
            tags = self.parser.select(selector.css, limit=limit)
        except ValueError:
            tags = []

        rets = [Element(tag) for tag in tags]

        for i in range(len(rets)):
            if selector.has_attr():
                rets[i] = rets[i].attr(selector.attr)
                if selector.has_re():
                    rets[i] = rets[i].re(selector.re, selector.fmt)

        return rets

    def select_one(self, selector: Union[Selector, str]):
        if not self.parser or not selector \
           or isinstance(selector, NullSelector):
            return NullElement()

        if isinstance(selector, str):
            selector = Selector.parse(selector)

        try:
            tag = self.parser.select_one(selector.css)
        except (ValueError, SyntaxError):
            tag = None

        ret = Element(tag) if tag else NullElement()

        if selector.has_attr():
            ret = ret.attr(selector.attr)
            if selector.has_re():
                ret = ret.re(selector.re, selector.fmt)
            else:
                ret = ret.to_string()

        return ret

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
