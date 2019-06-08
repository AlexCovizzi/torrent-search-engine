from bs4 import BeautifulSoup
from torrentsearchengine.scraper.element import Element, NullElement


class Scraper(Element):

    def __init__(self, markup: str = ''):
        try:
            parser = BeautifulSoup(markup, 'html.parser')
        except ValueError:
            parser = NullElement()

        super(Scraper, self).__init__(parser)
