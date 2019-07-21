from typing import List, Union, Optional
import json
import jsonschema
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from torrentsearchengine.exceptions import *
from torrentsearchengine.providermanager import TorrentProviderManager
from torrentsearchengine.torrent import Torrent
from torrentsearchengine.provider import TorrentProvider


logger = logging.getLogger(__name__)


class TorrentSearchEngine:

    def __init__(self):
        self.provider_manager = TorrentProviderManager()
        self.errors = []

    def search(self, query: str, limit: int = 0) -> List[Torrent]:
        # reset errors, we dont care about past errors
        self.errors = []

        # an empty query simply returns no torrent (for now?)
        if not query:
            return []

        providers = self.get_providers(enabled=True)
        n_providers = len(providers)
        if n_providers == 0:
            return []

        max_workers = (os.cpu_count() or 1) * 5
        n_workers = n_providers if n_providers < max_workers else max_workers

        logger.debug("Searching on {} providers ({} threads): '{}' (Max {})"
                     .format(n_providers, n_workers, query, limit))

        torrents = self._multithreaded_search(providers, query,
                                              limit, n_workers)

        torrents = self._filter(torrents)
        torrents = self._sort(torrents)
        torrents = torrents[:limit] if limit > 0 else torrents

        return torrents

    def get_providers(self, enabled=None) -> List[TorrentProvider]:
        return self.provider_manager.get_all(enabled=enabled)

    def get_provider(self, provider_name: str) -> Optional[TorrentProvider]:
        return self.provider_manager.get(provider_name)

    def add_providers(self, providers: Union[str, dict]):
        if isinstance(providers, dict):
            logger.debug("Adding providers from dictionary")
            try:
                self.provider_manager.add_from_dict(providers)
            except Exception as e:
                message = "Failed to add providers from dictionary: {}" \
                        .format(str(e))
                raise TorrentSearchEngineError(message) from None
        else:
            # providers can be url or path
            if providers.startswith("http"):
                # url
                logger.debug("Adding providers from url: '{}'".format(providers))
                try:
                    self.provider_manager.add_from_url(providers)
                except Exception as e:
                    message = "Failed to add providers from url '{}': {}" \
                            .format(providers, str(e))
                    raise TorrentSearchEngineError(message) from None
            else:
                # path
                logger.debug("Adding providers from file: '{}'".format(providers))
                try:
                    self.provider_manager.add_from_file(providers)
                except Exception as e:
                    message = "Failed to add providers from file '{}': {}" \
                            .format(providers, str(e))
                    raise TorrentSearchEngineError(message) from None

    def disable_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Disabling providers: {}".format(providers))
        self.provider_manager.disable(*providers)

    def enable_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Enabling providers: {}".format(providers))
        self.provider_manager.enable(*providers)

    def remove_providers(self, *providers: List[Union[str, TorrentProvider]]):
        logger.debug("Removing providers: {}".format(providers))
        self.provider_manager.remove(*providers)

    def _multithreaded_search(self, providers: List[TorrentProvider],
                              query: str, limit: int, n_workers: int):

        def job(provider: TorrentProvider, query: str, limit: int):
            logger.debug("Search on provider {} running on thread: {} ({})"
                         .format(provider.name,
                                 current_thread().name,
                                 current_thread().ident))
            torrents = []
            try:
                torrents = provider.search(query, limit)
            except TorrentProviderError as e:
                # save errors in the list
                self.errors.append(e)
            return torrents

        executor = ThreadPoolExecutor(n_workers)

        args = [providers, [query]*len(providers), [limit]*len(providers)]

        results = executor.map(job, *args)
        results = [item for sublist in results for item in sublist]

        return results

    def _filter(self, items: List[Torrent]):
        # find duplicats and keep only the one with more seeds
        filtered = []
        for item in items:
            duplicate = False
            for idx in range(len(filtered)):
                if item.title == filtered[idx].title:
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
