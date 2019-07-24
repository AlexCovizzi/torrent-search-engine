from typing import Any, List, Optional
import re
import requests
import logging
import time
from .utils import urljoin, urlfix
from .exceptions import *
from .provider import TorrentProvider
from .scraper import Scraper
from .scraper.selector import Selector, NullSelector
from .torrent import Torrent


logger = logging.getLogger(__name__)


class WebsiteTorrentProvider(TorrentProvider):

    def __init__(self, **kwargs: dict):
        name = kwargs.get('name')
        fullname = kwargs.get('fullname', name)
        url = kwargs.get('url')

        list_section = kwargs.get('list', {})
        list_item_section = list_section.get('item', {})
        item_section = kwargs.get('item', {})

        self.headers = kwargs.get('headers', {})
        self.search_path = kwargs.get('search')
        self.whitespace_char = kwargs.get('whitespace')
        self.next_page_selector = Selector.parse(list_section.get('next', ""))
        self.items_selector = Selector.parse(list_section.get('items', ""))
        self.list_item_selectors = {key: Selector.parse(str(s))
                                    for key, s in list_item_section.items()}
        self.item_selectors = {key: Selector.parse(str(s))
                               for key, s in item_section.items()}

        super(WebsiteTorrentProvider, self).__init__(name, fullname, url, True)

    def search(self, query: str, limit: int = 0, timeout=30):
        # return nothing if the provider is disabled
        if not self.enabled:
            return []

        start_time = time.time()
        elapsed_time = 0

        remaining = limit

        path = self._format_search_path(self.search_path, query)

        while path and (limit == 0 or remaining > 0):
            try:
                elapsed_time = time.time() - start_time
                current_timeout = timeout - elapsed_time
                response = self.fetch(path, headers=self.headers,
                                      timeout=current_timeout)
            except TorrentProviderRequestError as e:
                raise TorrentProviderSearchError(self, query, e.request) from e

            scraper = Scraper(response.text)

            items = scraper.select(self.items_selector.css, limit=remaining)
            for item in items:
                torrent_data = self._get_torrent_data(item)
                torrent = Torrent(**torrent_data)
                yield torrent

            remaining -= len(items)

            path = scraper.select_one(self.next_page_selector)

    def fetch_details(self, torrent: Torrent, timeout=30) -> dict:
        # retrieve the info page url
        path = torrent.info_url
        if not path:
            # basically we return the same data of the torrent
            return {}

        # fetch the torrent info page and scrape
        response = self.fetch(path, timeout=timeout)
        scraper = Scraper(response.text)

        torrent_details = self._get_torrent_details(scraper)

        return torrent_details

    def _format_search_path(self, path, query):
        query = query.strip()
        if self.whitespace_char:
            query = re.sub(r"\s+", self.whitespace_char, query)
        path = path.format(query=query)
        return path

    def _get_torrent_data(self, element):
        props = {"provider": self}
        for key, selector in self.list_item_selectors.items():
            prop = element.select_one(selector)
            props[key] = prop

        # make the url full (with the host)
        url = props.get('info_url', '')
        if not url.startswith('http'):
            url = urljoin(self.url, url)
            url = urlfix(url)
            props['info_url'] = url

        return props

    def _get_torrent_details(self, element):
        props = {}
        # retrieve the info page selectors
        for key, selector in self.item_selectors.items():
            # for some properties we need to select all elements that match
            if key == "files" or key == "trackers":
                prop = element.select(selector)
            else:
                prop = element.select_one(selector)
            props[key] = prop

        # make the uploader url full (add the host)
        url = props.get('uploader_url', None)
        if url and not url.startswith('http'):
            url = urljoin(self.url, url)
            url = urlfix(url)
            props['uploader_url'] = url
        return props
