from typing import Any, List
import requests
from torrentsearchengine.utils import KwArgs
from torrentsearchengine.exceptions import TorrentProviderSearchError
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.scraper import Scraper
from torrentsearchengine.scraper.selector import Selector, NullSelector
from torrentsearchengine.torrent import Torrent


class WebsiteTorrentProvider(TorrentProvider):

    def __init__(self, pid: str, **kwargs: dict):
        kwargs = KwArgs(kwargs)

        name = kwargs.getstr('name', pid)
        url = kwargs.getstr('url')
        user_agent = kwargs.getstr('userAgent')

        list_section = KwArgs(kwargs.getdict('list'))
        list_item_section = KwArgs(list_section.getdict('item'))
        item_section = KwArgs(kwargs.getdict('item'))

        next_page_url_selector_str = list_section.getstr('next')
        items_selector_str = list_section.getstr('items')

        self.search_path = kwargs.getstr('search')
        self.next_page_url_selector = Selector.parse(next_page_url_selector_str)
        self.items_selector = Selector.parse(items_selector_str)
        self.list_item_selectors = {key: Selector.parse(str(s))
                                    for key, s in list_item_section.items()}
        self.item_selectors = {key: Selector.parse(str(s))
                               for key, s in item_section.items()}

        super(WebsiteTorrentProvider, self).__init__(pid, name, url, user_agent)

    def search(self, query: str, limit: int = 0) -> List[Torrent]:
        torrents = []

        # fetch the search page
        path = self.search_path.format(query=query)
        response = self.fetch(path)

        scraper = Scraper(response.text)

        items = scraper.select(self.items_selector, limit=limit)
        for item in items:
            props = {"provider": self}
            for key, selector in self.list_item_selectors.items():
                prop = item.select_one(selector.css) \
                           .attr(selector.attr) \
                           .re(selector.re)
                props[key] = prop

            torrent = Torrent(**props)
            torrents.append(torrent)

        return torrents

    def fetch_magnet(self, torrent: Torrent) -> str:
        if torrent._magnet:
            return torrent._magnet

        # retrieve the torrent info page url
        path = torrent.url
        if not path:
            return ''

        # retrieve the magnet selector
        selector = self.item_selectors.get('magnet')
        if not selector:
            return ''

        # fetch the torrent info page and scrape
        response = self.fetch(path)

        scraper = Scraper(response.text)

        magnet = scraper.select_one(selector.css) \
                        .attr(selector.attr) \
                        .re(selector.re)

        # save the magnet in the torrent
        torrent._magnet = magnet

        return magnet


if __name__ == '__main__':
    import json

    path = 'providers.json'
    with open(path, 'r', encoding='utf-8') as f:
        provider_dict = json.load(f).get('eztv', {})

    provider = ScrapeTorrentProvider('eztv', **provider_dict)

    results = provider.search_torrents('game of thrones', 5)
    for result in results:
        print(str(result))
