from typing import List
from abc import ABC, abstractmethod
import requests
import logging
from torrentsearchengine.utils import urljoin, urlfix
from torrentsearchengine.exceptions import TorrentProviderRequestError
from torrentsearchengine.torrent import Torrent


logger = logging.getLogger(__name__)


class TorrentProvider(ABC):

    def __init__(self, name: str, url: str, enabled=True):
        self.name = name
        self.url = url
        self.enabled = enabled

    @abstractmethod
    def search(self, query: str, limit: int = 25) -> List[Torrent]:
        """
        Search torrents using this provider.

        Parameters:
            query: str - The query to perform.
            limit: int - The number of results to return.

        Returns:
            List[Torrent] - A List of Torrents.
        """
        pass

    @abstractmethod
    def fetch_magnet(self, torrent: Torrent) -> str:
        """
        Fetch the magnet for this torrent.

        Parameters:
            torrent: Torrent - The torrent of which to fetch the magnet uri.

        Returns:
            str - The torrent magnet uri or an empty
                  string if the magnet is not found.
        """
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
            "url": self.url,
            "enabled": self.enabled
        }

    def __str__(self):
        return self.name
