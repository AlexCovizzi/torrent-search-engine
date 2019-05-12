import requests
from bs4 import BeautifulSoup
from torrenttv.search_engine.torrentprovider import TorrentProvider


class SearchEngine(object):

    def __init__(self):
        super().__init__()

        self.providers = []


    def search_torrents(self, query: str):
        result = {
            'provider': '',
            'title': '',
            'seeds': 0,
            'peers': 0,
            'time': '',
            'size': '',
            'magnetUri': '??'
        }
        pass


    def _search(self, query: str, limit: int, providers: list[TorrentProvider]):
        pass

    def add_provider(self, provider: TorrentProvider):
        same_id_providers = [prv for prv in self.providers if prv.id == provider.id]
        if len(same_id_providers) != 0:
            same_id_provider = same_id_providers[0]
            self.providers.remove(same_id_provider)

        self.providers.append(provider)

    def add_providers(self, providers: list[TorrentProvider]):
        for prv in providers:
            self.add_provider(prv)

    def remove_provider(self, provider_id):
        providers = [prv for prv in self.providers if prv.id == provider_id]
        for provider in providers:
            self.providers.remove(provider)
