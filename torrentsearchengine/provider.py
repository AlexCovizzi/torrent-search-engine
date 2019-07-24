from typing import List
import requests
import logging
from .utils import urljoin, urlfix
from .exceptions import TorrentProviderRequestError
from .torrent import Torrent


logger = logging.getLogger(__name__)


class TorrentProvider:

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
        """
        pass

    def fetch_details(self, torrent: Torrent, timeout=30) -> dict:
        pass

    def fetch(self, url: str, **kwargs) -> requests.Response:
        if not url.startswith('http'):
            url = urljoin(self.url, url)
        url = urlfix(url)

        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            message = "Failed to connect to {}: {}".format(url, e)
            raise TorrentProviderRequestError(self, message, e.request) from e
        except requests.exceptions.RequestException as e:
            message = "An error occurred while fetching {}: {}".format(url, e)
            raise TorrentProviderRequestError(self, message, e.request) from e

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
