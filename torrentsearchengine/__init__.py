from typing import List, Union, Optional
from concurrent.futures import ThreadPoolExecutor
from torrentsearchengine.exceptions import ProviderSearchError
from torrentsearchengine.torrent import Torrent
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.websiteprovider import WebsiteTorrentProvider


SEARCH_LIMIT_DEFAULT = 25


class TorrentSearchEngine:

    def __init__(self):
        self.providers = []


    def search(self, query: str, limit: int = SEARCH_LIMIT_DEFAULT):
        n_providers = len(self.providers)
        n_workers = n_providers if n_providers < 10 else None
        executor = ThreadPoolExecutor(n_workers)
        args = [self.providers, [query]*n_providers, [limit]*n_providers]
        results = executor.map(self._search, *args)
        return [item for sublist in results for item in sublist]


    def fetch_magnet(self, torrent: Torrent):
        provider = self.get_provider(torrent.provider_id)
        if provider:
            return provider.get_magnet(torrent)
        else:
            return ''


    def add_provider(self, provider: TorrentProvider):
        same_id_providers = [prv for prv in self.providers if prv.id == provider.id]
        if len(same_id_providers) != 0:
            same_id_provider = same_id_providers[0]
            self.providers.remove(same_id_provider)

        self.providers.append(provider)


    def add_providers(self, providers: List[TorrentProvider]):
        for prv in providers:
            self.add_provider(prv)


    def remove_provider(self, provider_id):
        providers = [prv for prv in self.providers if prv.id == provider_id]
        for provider in providers:
            self.providers.remove(provider)


    def get_provider(self, provider_id) -> Optional[TorrentProvider]:
        providers = [prv for prv in self.providers if prv.id == provider_id]
        if len(providers) == 0:
            return None

        return providers[0]


    def _search(self, provider: TorrentProvider, query: str, limit: int) -> Union[List[Torrent], Exception]:
        try:
            torrents = provider.search_torrents(query, limit)
            return torrents
        except ProviderSearchError as e:
            return e





if __name__ == "__main__":
    import json

    search_engine = SearchEngine()

    path = "C:\\Users\\Alex\\Documents\\Projects\\torrent-tv\\src\\main\\resources\\base\\providers\\providers.json"
    with open(path, 'r', encoding='utf-8') as f:
        providers_json = json.load(f)
        for key in providers_json.keys():
            provider_dict = providers_json.get(key)
            provider = ScrapeTorrentProvider(key, **provider_dict)
            search_engine.add_provider(provider)

    results = search_engine.search_torrents('game of thrones', 5)
    for result in results:
        print(str(result))
