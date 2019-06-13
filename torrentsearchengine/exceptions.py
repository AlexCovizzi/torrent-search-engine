import requests


class TorrentSearchEngineError(Exception):

    def __init__(self, message: str = ""):
        super().__init__(message)


class TorrentProviderError(Exception):

    def __init__(self, provider, message: str = ""):
        self.provider = provider


class TorrentProviderRequestError(TorrentProviderError):

    def __init__(self, provider, request: requests.Request, message: str = ""):
        self.provider = provider
        self.request = request


class TorrentProviderSearchError(TorrentProviderRequestError):

    def __init__(self, provider, query: str, request: requests.Request,
                 reason: str = ""):
        message = "Search failed (provider: {}, query: {}): {}" \
                  .format(str(provider), query, reason)
        super().__init__(provider, request, message)
