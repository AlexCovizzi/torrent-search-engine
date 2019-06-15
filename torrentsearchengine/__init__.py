from typing import List, Union, Optional
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from torrentsearchengine.providermanager import TorrentProviderManager
from torrentsearchengine.exceptions import TorrentProviderError
from torrentsearchengine.torrent import Torrent
from torrentsearchengine.provider import TorrentProvider


logger = logging.getLogger(__name__)


class TorrentSearchEngine:

    def __init__(self):
        self.provider_manager = TorrentProviderManager()
        self.errors = []

    def search(self, query: str, limit: int = 0) -> List[Torrent]:
        self.errors = []

        providers = self.get_enabled_providers()
        n_providers = len(providers)
        n_workers = n_providers if n_providers < 10 else None

        logger.debug("Searching on {} providers ({} threads): '{}' (max {})"
                     .format(len(self.get_enabled_providers()), n_workers,
                             query, limit))

        executor = ThreadPoolExecutor(n_workers)

        args = [providers, [query]*n_providers, [limit]*n_providers]

        results = executor.map(self._search, *args)

        return [item for sublist in results for item in sublist]

    def get_providers(self):
        return self.provider_manager.get_all()

    def get_enabled_providers(self):
        return self.provider_manager.get_enabled()

    def get_disabled_providers(self):
        return self.provider_manager.get_disabled()

    def add_providers(self, path: str):
        self.provider_manager.add(path)

    def disable_provider(self, provider: Union[str, TorrentProvider]):
        self.provider_manager.disable(provider)

    def enable_provider(self, provider: Union[str, TorrentProvider]):
        self.provider_manager.enable(provider)

    def remove_provider(self, provider: Union[str, TorrentProvider]):
        self.provider_manager.remove(provider)

    def get_provider(self, provider_id: str) -> Optional[TorrentProvider]:
        return self.provider_manager.get(provider_id)

    def _search(self, provider: TorrentProvider, query: str, limit: int):
        logger.debug("Provider {} running on thread: {} ({})"
                     .format(provider.id, current_thread().name,
                             current_thread().ident))
        torrents = []
        try:
            torrents = provider.search(query, limit)
        except TorrentProviderError as e:
            self.errors.append(e)
        return torrents
