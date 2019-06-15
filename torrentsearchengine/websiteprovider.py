from typing import Any, List
import re
import requests
from torrentsearchengine.utils import KwArgs
from torrentsearchengine.exceptions import *
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.scraper import Scraper
from torrentsearchengine.scraper.selector import Selector, NullSelector
from torrentsearchengine.torrent import Torrent


class WebsiteTorrentProvider(TorrentProvider):

    def __init__(self, pid: str, **kwargs: dict):
        kwargs = KwArgs(kwargs)

        name = kwargs.getstr('name', pid)
        url = kwargs.getstr('url')
        headers = kwargs.getdict('headers')

        list_section = KwArgs(kwargs.getdict('list'))
        list_item_section = KwArgs(list_section.getdict('item'))
        item_section = KwArgs(kwargs.getdict('item'))

        next_page_url_selector_str = list_section.getstr('next')
        items_selector_str = list_section.getstr('items')

        self.search_path = kwargs.getstr('search')
        self.whitespace_char = kwargs.getstr('whitespace')
        self.next_page_url_selector = Selector.parse(next_page_url_selector_str)
        self.items_selector = Selector.parse(items_selector_str)
        self.list_item_selectors = {key: Selector.parse(str(s))
                                    for key, s in list_item_section.items()}
        self.item_selectors = {key: Selector.parse(str(s))
                               for key, s in item_section.items()}

        super(WebsiteTorrentProvider, self).__init__(pid, name, url, headers)

    def search(self, query: str, limit: int = 0) -> List[Torrent]:
        torrents = []

        query = query.strip()
        if self.whitespace_char:
            query = re.sub(r"\s+", self.whitespace_char, query)

        path = self.search_path.format(query=query)

        while path and limit > 0:
            try:
                response = self.fetch(path)
            except TorrentProviderRequestError as e:
                raise TorrentProviderSearchError(self, query, e.request) from e

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

            limit -= len(items)

            path = scraper.select_one(self.next_page_url_selector.css) \
                          .attr(self.next_page_url_selector.attr) \
                          .re(self.next_page_url_selector.re)

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
