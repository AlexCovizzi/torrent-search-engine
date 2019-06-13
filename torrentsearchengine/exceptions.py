import requests
from torrentsearchengine import TorrentProvider


class TorrentSearchEngineError(Exception):

    def __init__(self, message: str = ""):
        super().__init__(message)


class TorrentProviderError(Exception):

    def __init__(self, provider: TorrentProvider, message: str = ""):
        self.provider = provider


class TorrentProviderSearchError(TorrentProviderError):

    def __init__(self, provider: TorrentProvider, query: str, reason: str = ""):
        message = "Search failed (provider: {}, query: {}): {}" \
                  .format(provider.name, query, reason)
        super().__init__(provider, message)
