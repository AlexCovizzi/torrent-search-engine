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
from .torrentprovider import TorrentProvider
from .torrent import Torrent


logger = logging.getLogger(__name__)


class TorrentSearchEngine:

    def __init__(self):
        self.provider_manager = TorrentProviderManager()

    def search(self, query: str, category: str = None, limit: int = None,
               providers=None, timeout: int = None,
               n_threads: int = None) -> List[Torrent]:
        """
        Search torrents.

        Parameters:
            query: str - The query to perform.
            category: str - The category to search.
            limit: int - The number of results to return.
            providers: List[Union[str, TorrentProvider]] - Providers to use.
            timeout: int - The max number of seconds to wait.

        Returns:
            List[Torrent] - The torrents found.
                            Returns an empty list if the query is empty
                            or if no provider is used.
        """

        # an empty query simply returns no torrent (for now?)
        if not query:
            return []

        if providers is None:
            # get only enabled providers
            providers = self.get_providers(enabled=True)
        else:
            # get as TorrentProvider
            providers = [provider if isinstance(provider, TorrentProvider)
                         else self.get_provider(provider)
                         for provider in providers]
            providers = [provider for provider in providers
                         if provider is not None]

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

        torrents = self._multithreaded_search(providers, category, query,
                                              limit, timeout, n_threads)

        torrents = self._sort_by_seeds(torrents)

        return torrents

    def add_provider(self, provider: Union[str, dict, TorrentProvider]):
        """
        Add a provider from dict/file/url.

        Raises:
            ValueError - There is an error in a property.
            ValidationError - The resource is incorrect.
            RequestError - The resource could not be retrieve from url.
            IOError - The file could not be read.
        """
        self.provider_manager.add(provider)

    def get_providers(self, enabled=None) -> List[TorrentProvider]:
        return self.provider_manager.get_all(enabled=enabled)

    def get_provider(self, name: str) -> Optional[TorrentProvider]:
        return self.provider_manager.get(name)

    def disable_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Disabling providers: {}".format(providers))
        self.provider_manager.disable(*providers)

    def enable_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Enabling providers: {}".format(providers))
        self.provider_manager.enable(*providers)

    def remove_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Removing providers: {}".format(providers))
        self.provider_manager.remove(*providers)

    def _multithreaded_search(self, providers, category, query, limit,
                              timeout, n_threads):

        def task(q, provider, query, category, limit, timeout):
            logger.debug("Search on provider {} running on thread: {} ({})"
                         .format(provider.name,
                                 current_thread().name,
                                 current_thread().ident))
            if timeout is not None:
                elapsed_time = time.time() - start_time
                current_timeout = timeout - elapsed_time
                if current_timeout <= 0:
                    return
            else:
                current_timeout = None
            try:
                for torrent in provider.search(query, category=category,
                                               limit=limit,
                                               timeout=current_timeout):
                    q.put_nowait(torrent)
            except queue.Full:
                pass
            except Exception as e:
                message = "Stopped search on provider {}: {}" \
                          .format(provider.name, e)
                logger.warning(message)

        start_time = time.time()
        torrents = []
        q = queue.Queue(limit)
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            executor.daemon = True
            n = len(providers)
            args = [[q]*n, providers, [query]*n, [category]*n,
                    [limit]*n, [timeout]*n]
            for result in executor.map(task, *args):
                pass
        while not q.empty():
            torrents.append(q.get_nowait())

        return torrents

    def _sort_by_seeds(self, items: List[Torrent]) -> List[Torrent]:
        return sorted(items, key=lambda item: item.seeds, reverse=True)
