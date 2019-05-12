from typing import Union, Any
from bs4 import BeautifulSoup
from re import sub


class Scraper(object):

    def __init__(self, source: Any):
        if hasattr(source, 'select') and hasattr(source, 'select_one'):
            self.source = source
        elif isinstance(source, str):
            self.source = BeautifulSoup(str(source), 'html.parser')
        else:
            self.source = None

    def get_all(self, selector: str, limit: int = 0):
        if not self.source or not selector:
            return []

        elements = self.source.select(selector, limit=limit)

        return elements

    def get_one(self, selector: Union[str, dict]):
        if not self.source or not selector:
            return None

        element = self.source.select_one(selector)

        return element

    def get_value(self, selector: str, def_val='') -> str:
        if not selector:
            return def_val

        selector_parts = selector.split('@')
        if len(selector_parts) > 1:
            selector = selector_parts[0].strip()
            attr = selector_parts[1].strip()
        else:
            selector = selector_parts[0].strip()
            attr = ''

        element = self.source.select_one(selector)
        if element is None:
            return def_val

        if not attr:
            value = element.get_text()
        elif element.has_attr(attr):
            value = str(element[attr])
        else:
            return def_val

        return value
