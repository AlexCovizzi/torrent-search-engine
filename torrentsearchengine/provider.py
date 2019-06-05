from typing import List
from abc import ABC, abstractmethod
import requests
from torrentsearchengine.utils import urljoin, urlfix
from torrentsearchengine.torrent import Torrent


class TorrentProvider(ABC):

    def __init__(self, pid: str, name: str, url: str, user_agent: str = None):
        self.id = pid
        self.name = name
        self.url = url
        self.user_agent = user_agent

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
        """
        pass

    def fetch(self, path: str) -> requests.Response:
        headers = {}
        if self.user_agent:
            headers['User-Agent'] = self.user_agent

        url = urljoin(self.url, path)
        url = urlfix(url)

        return requests.get(url, headers=headers)
