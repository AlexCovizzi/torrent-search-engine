from typing import List
from abc import ABC, abstractmethod
import requests
from torrentsearchengine.utils import urljoin, urlfix
from torrentsearchengine.exceptions import TorrentProviderRequestError
from torrentsearchengine.torrent import Torrent


class TorrentProvider(ABC):

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.enabled = True

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

    def fetch(self, path: str, **kwargs) -> requests.Response:
        url = urljoin(self.url, path)
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

    def disable(self):
        self.enabled = False

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "enabled": self.enabled
        }

    def __str__(self):
        return self.name
