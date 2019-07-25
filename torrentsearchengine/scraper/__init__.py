from bs4 import BeautifulSoup
from .element import Element, NullElement


class Scraper(Element):

    def __init__(self, markup: str = '', enc: str = None):
        parser = BeautifulSoup(markup, 'html.parser', from_encoding=enc)

        super(Scraper, self).__init__(parser)
