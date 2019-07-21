from bs4 import BeautifulSoup
from .element import Element, NullElement


class Scraper(Element):

    def __init__(self, markup: str = '', encoding: str = None):
        try:
            parser = BeautifulSoup(markup, 'html.parser',
                                   from_encoding=encoding)
        except ValueError:
            parser = NullElement()

        super(Scraper, self).__init__(parser)
