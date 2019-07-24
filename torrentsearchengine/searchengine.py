from typing import List, Union, Optional
import json
import jsonschema
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import queue
from .exceptions import *
from .providermanager import TorrentProviderManager
from .torrent import Torrent
from .provider import TorrentProvider


logger = logging.getLogger(__name__)


class TorrentSearchEngine:

    def __init__(self):
        self.provider_manager = TorrentProviderManager()

    def search(self, query: str, limit: int = 0, timeout: int = 30,
               n_threads: int = None) -> List[Torrent]:

        # an empty query simply returns no torrent (for now?)
        if not query:
            return []

        providers = self.get_providers(enabled=True)
        n_providers = len(providers)
        if n_providers == 0:
            return []

        if n_threads is None or n_threads < 1:
            max_threads = (os.cpu_count() or 1) * 5
            n_threads = n_providers if n_providers < max_threads \
                else max_threads

        logger.debug(("Searching on {} providers ({} threads): " +
                      "'{}' (limit: {}, timeout: {})")
                     .format(n_providers, n_threads, query, limit, timeout))

        torrents = self._multithreaded_search(providers, query,
                                              limit, timeout, n_threads)

        torrents = self._filter(torrents)
        torrents = self._sort(torrents)

        return torrents

    def get_providers(self, enabled=None) -> List[TorrentProvider]:
        return self.provider_manager.get_all(enabled=enabled)

    def get_provider(self, name: str) -> Optional[TorrentProvider]:
        return self.provider_manager.get(name)

    def add_provider(self, provider: Union[str, dict, TorrentProvider]):
        self.provider_manager.add(provider)

    def disable_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Disabling providers: {}".format(providers))
        self.provider_manager.disable(*providers)

    def enable_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Enabling providers: {}".format(providers))
        self.provider_manager.enable(*providers)

    def remove_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Removing providers: {}".format(providers))
        self.provider_manager.remove(*providers)

    def _multithreaded_search(self, providers, query, limit,
                              timeout, n_threads):

        def task(q, provider, query, limit, timeout):
            logger.debug("Search on provider {} running on thread: {} ({})"
                         .format(provider.name,
                                 current_thread().name,
                                 current_thread().ident))
            elapsed_time = time.time() - start_time
            timeout = timeout - elapsed_time
            if timeout <= 0.01:
                return
            try:
                for torrent in provider.search(query, limit, timeout):
                    q.put_nowait(torrent)
            except TorrentProviderError as e:
                message = "Search on provider %s failed: %s"
                logger.warning(message, provider.name, str(e))
            except queue.Full:
                pass

        start_time = time.time()
        torrents = []
        q = queue.Queue(limit)
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            n = len(providers)
            args = [[q]*n, providers, [query]*n, [limit]*n, [timeout]*n]
            for result in executor.map(task, *args):
                pass
        while not q.empty():
            torrents.append(q.get_nowait())

        return torrents

    def _filter(self, items: List[Torrent]):
        # find duplicats and keep only the one with more seeds
        filtered = []
        for item in items:
            duplicate = False
            for idx in range(len(filtered)):
                if item.name == filtered[idx].name:
                    duplicate = True
                    # replace the item only if it has more seeds
                    if item.seeds > filtered[idx].seeds:
                        filtered[idx] = item
            if not duplicate:
                # add the item only if its not a duplicate
                filtered.append(item)
        return filtered

    def _sort(self, items: List[Torrent]) -> List[Torrent]:
        return sorted(items, key=lambda item: item.seeds, reverse=True)
