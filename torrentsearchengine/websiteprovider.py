from typing import Any, List
import re
import requests
import logging
import time
from torrentsearchengine.utils import KwArgs, urljoin, urlfix
from torrentsearchengine.exceptions import *
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.scraper import Scraper
from torrentsearchengine.scraper.selector import Selector, NullSelector
from torrentsearchengine.torrent import Torrent


logger = logging.getLogger(__name__)


class WebsiteTorrentProvider(TorrentProvider):

    def __init__(self, **kwargs: dict):
        kwargs = KwArgs(kwargs)

        name = kwargs.getstr('name')
        fullname = kwargs.getstr('fullname', name)
        url = kwargs.getstr('url')

        list_section = KwArgs(kwargs.getdict('list'))
        list_item_section = KwArgs(list_section.getdict('item'))
        item_section = KwArgs(kwargs.getdict('item'))

        next_page_url_selector_str = list_section.getstr('next')
        items_selector_str = list_section.getstr('items')

        self.headers = kwargs.getdict('headers')
        self.search_path = kwargs.getstr('search')
        self.whitespace_char = kwargs.getstr('whitespace')
        self.next_page_url_selector = Selector.parse(next_page_url_selector_str)
        self.items_selector = Selector.parse(items_selector_str)
        self.list_item_selectors = {key: Selector.parse(str(s))
                                    for key, s in list_item_section.items()}
        self.item_selectors = {key: Selector.parse(str(s))
                               for key, s in item_section.items()}

        super(WebsiteTorrentProvider, self).__init__(name, fullname, url, True)

    def search(self, query: str, limit: int = 0, timeout=30):
        if not self.enabled:
            return

        start_time = time.time()
        elapsed_time = 0

        remaining = limit

        # format query for url
        query = query.strip()
        if self.whitespace_char:
            query = re.sub(r"\s+", self.whitespace_char, query)

        path = self.search_path.format(query=query)

        while path and (limit == 0 or remaining > 0):
            try:
                elapsed_time = time.time() - start_time
                current_timeout = timeout - elapsed_time
                response = self.fetch(path, headers=self.headers, timeout=current_timeout)
            except TorrentProviderRequestError as e:
                raise TorrentProviderSearchError(self, query, e.request) from e

            scraper = Scraper(response.text)

            items = scraper.select(self.items_selector, limit=remaining)
            for item in items:
                props = {"provider": self}
                for key, selector in self.list_item_selectors.items():
                    prop = item.select_one(selector.css) \
                               .attr(selector.attr) \
                               .re(selector.re, selector.fmt)
                    props[key] = prop

                # make the url full (with the host)
                url = props.get('url', '')
                if not url.startswith('http'):
                    url = urljoin(self.url, url)
                    url = urlfix(url)
                    props['url'] = url

                torrent = Torrent(**props)
                yield torrent

            remaining -= len(items)

            path = scraper.select_one(self.next_page_url_selector.css) \
                          .attr(self.next_page_url_selector.attr) \
                          .re(self.next_page_url_selector.re,
                              self.next_page_url_selector.fmt)

    def fetch_magnet(self, torrent: Torrent, timeout=30) -> str:
        if torrent._magnet:
            return torrent._magnet

        # retrieve the torrent info page url
        path = torrent.url
        if not path:
            return ''

        # retrieve the magnet selector
        selector = self.item_selectors.get("magnet")
        if not selector:
            return ''

        # fetch the torrent info page and scrape
        response = self.fetch(path, timeout=timeout)

        scraper = Scraper(response.text)

        magnet = scraper.select_one(selector.css) \
                        .attr(selector.attr) \
                        .re(selector.re, selector.fmt)

        torrent._magnet = magnet

        return magnet
    """
    def asdict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "headers": self.headers,
            "search": self.search_path,
            "whitespace": self.whitespace_char,
            "list": {
                "items": self.items_selector.asdict(),
                "item": {key: selector.asdict() for key, selector
                         in self.list_item_selectors.items()},
                "next": self.next_page_url_selector.asdict()
            },
            "item": {key: selector.asdict() for key, selector
                     in self.item_selectors.items()}
        }
    """
