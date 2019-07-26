from typing import List
import requests
import logging
from .exceptions import *
from .utils import urljoin, urlfix
from .torrent import Torrent


logger = logging.getLogger(__name__)


class TorrentProvider:

    # if the time left is less than this number, we raise Timeout
    TIMEOUT_EPSILON = 0.1

    def __init__(self, name: str, fullname: str, url: str, enabled=True):
        self.name = name
        self.fullname = fullname
        self.url = url
        self.enabled = enabled

    def search(self, query: str, limit: int = 25, timeout=30):
        """
        Search torrents using this provider.

        Parameters:
            query: str - The query to perform.
            limit: int - The number of results to return.
            timeout: int - The max number of seconds to wait.
                           If the search lasts longer than timeout,
                           raise Timeout.

        Yields:
            Torrent - The search results are yielded as they are retrieved.

        Raises:
            ParseError - Something went wrong parsing the page received.
            RequestError - Something went wrong requesting the search page.
            Timeout - The search lasted longer than timeout.
        """
        pass

    def fetch_details_data(self, torrent: Torrent, timeout=30) -> dict:
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
        pass

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
