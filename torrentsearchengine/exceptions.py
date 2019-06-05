import requests


class TorrentSearchEngineError(Exception):

    def __init__(self, message: str):
        self.request = request
        self.message = "Failed to retrieve {}: {}".format(request.url, message)


class SearchError(TorrentSearchEngineError):

    def __init__(self, request: requests.Request, message: str):
        self.request = request
        self.message = "Failed to retrieve {}: {}".format(request.url, message)
