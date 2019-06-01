import requests


class ProviderSearchError(Exception):

    def __init__(self, request: requests.Request, message: str):
        self.request = request
        self.message = "Failed to retrieve {}: {}".format(request.url, message)
