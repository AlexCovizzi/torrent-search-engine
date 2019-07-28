from typing import Any, List, Optional
import re
import requests
import logging
import time
import jsonschema
from .utils import urljoin, urlfix
from .providervalidator import torrent_provider_validator
from .exceptions import *
from .scraper import Scraper
from .scraper.selector import Selector, NullSelector
from .torrent import Torrent


logger = logging.getLogger(__name__)


class TorrentProvider:

    def __init__(self, validate=True, **kwargs):
        if validate:
            self._validate(kwargs)

        self.enabled = True
        # extract data
        self.name = kwargs.get('name')
        self.fullname = kwargs.get('fullname', self.name)
        self.url = kwargs.get('url')

        list_section = kwargs.get('list', {})
        list_item_section = list_section.get('item', {})
        item_section = kwargs.get('item', {})

        self._headers = kwargs.get('headers')
        self._whitespace_char = kwargs.get('whitespace')
        self._search = kwargs.get('search')
        # convert to dictionary
        self._search = self._search if isinstance(self._search, dict) \
            else {"all": self._search}

        # parse selectors
        self._next_page_selector = Selector.parse(list_section.get('next', ""))
        self._items_selector = Selector.parse(list_section.get('items', ""))
        self._list_item_selectors = {key: Selector.parse(sel)
                                     for key, sel in list_item_section.items()}
        self._item_selectors = {key: Selector.parse(sel)
                                for key, sel in item_section.items()}

    def search(self, query: str, category=None, limit=None, timeout=None):
        """
        Search torrents using this provider.

        Parameters:
            query: str - The query to perform.
            category: str - The category to search.
            limit: int - The number of results to return.
            timeout: int - The max number of seconds to wait.
                           If the search lasts longer than timeout,
                           raise TimeoutError.

        Yields:
            Torrent - The search results are yielded as they are retrieved.

        Raises:
            ParseError - Something went wrong parsing the page received.
            RequestError - Something went wrong requesting the search page.
            Timeout - The search lasted longer than timeout.
            FormatError - There was an error formatting the search path.
            NotSupportedError - The category is not supported.
        """

        if timeout is not None:
            start_time = time.time()
            elapsed_time = 0

        remaining = limit

        path = self._format_search_path(query, category)

        while path and (not limit or remaining > 0):
            if timeout is not None:
                elapsed_time = time.time() - start_time
                current_timeout = timeout - elapsed_time
                if current_timeout <= 0:
                    break
            else:
                current_timeout = None

            response = self.fetch(path, headers=self._headers,
                                  timeout=current_timeout)

            try:
                scraper = Scraper(response.text)
            except ValueError as e:
                raise ParseError(e) from e

            items = scraper.select_elements(self._items_selector,
                                            limit=remaining)
            for item in items:
                torrent_data = self._get_torrent_data(item)
                try:
                    torrent = Torrent(**torrent_data)
                    yield torrent
                except ValueError:
                    # the torrent is missing some important properties
                    # in this case we dont return the torrent
                    pass

            remaining -= len(items)

            path = scraper.select_one(self._next_page_selector)

    def fetch_details_data(self, torrent: Torrent, timeout=None) -> dict:
        """
        Fetch torrent details data (e.g link, description, files, ecc)
        from the Torrent's info_url.

        Parameters:
            torrent: Torrent - The torrent that we want the details of.
            timeout: int - Timeout in seconds.

        Returns:
            dict - Torrent details.

        Raises:
            ParseError - Something went wrong parsing the page received.
            RequestError - Something went wrong requesting the search page.
            Timeout - The search lasted longer than timeout.
        """

        # retrieve the info page url
        path = torrent.info_url
        if not path:
            # basically we return the same data of the torrent
            return {}

        # fetch the torrent info page and scrape
        response = self.fetch(path, timeout=timeout)
        try:
            scraper = Scraper(response.text)
        except ValueError as e:
            raise ParseError(e) from e

        details_data = self._get_torrent_details_data(scraper)

        return details_data

    def fetch(self, url: str, **kwargs) -> requests.Response:
        """
        Retrieve a page.

        Raises:
            RequestError - Something went wrong.
            Timeout - Request timed out.
        """
        if not url.startswith('http'):
            url = urljoin(self.url, url)
        url = urlfix(url)

        logger.debug("{}: GET {}".format(self.name, url))

        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            raise Timeout(e) from e
        except requests.exceptions.RequestException as e:
            raise RequestError(e) from e

        return response

    def enable(self):
        self.enabled = True
        logger.debug("{}: enabled.".format(self))

    def disable(self):
        self.enabled = False
        logger.debug("{}: disabled.".format(self))

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "fullname": self.fullname,
            "url": self.url,
            "enabled": self.enabled
        }

    def __str__(self):
        return self.name

    def _validate(self, data: dict):
        try:
            torrent_provider_validator.validate(data)
        except jsonschema.ValidationError as e:
            raise ValidationError(e) from e

    def _format_search_path(self, query, category):
        query = query.lower().strip()
        # replace whitespace with whitespace character
        if self._whitespace_char:
            query = re.sub(r"\s+", self._whitespace_char, query)

        if category is None:
            category = "all"
        if category not in self._search:
            message = "{}: category {} is not supported." \
                        .format(self.name, category)
            raise NotSupportedError(message)
        else:
            try:
                path = self._search.get(category)
                path = path.format(query=query)
            except KeyError as e:
                message = "{}: {} with query = {} and category = {}" \
                        .format(self.name, path, query, category)
                raise FormatError(message)
        return path

    def _get_torrent_data(self, element):
        props = {"provider": self}
        for key, selector in self._list_item_selectors.items():
            prop = element.select_one(selector)
            props[key] = prop

        # make the url full (with the host)
        url = props.get('info_url', '')
        if url and not url.startswith('http'):
            url = urljoin(self.url, url)
            url = urlfix(url)
            props['info_url'] = url

        return props

    def _get_torrent_details_data(self, element):
        props = {}
        # retrieve the info page selectors
        for key, selector in self._item_selectors.items():
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
