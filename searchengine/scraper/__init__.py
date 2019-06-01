from bs4 import BeautifulSoup
from searchengine.scraper.pageelement import PageElement, NullPageElement


class Scraper(PageElement):

    def __init__(self, markup: str = ''):
        try:
            parser = BeautifulSoup(markup, 'html.parser')
        except ValueError:
            parser = NullPageElement()

        super(Scraper, self).__init__(parser)