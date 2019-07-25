import requests


class _Error(Exception):

    def __init__(self, message: str = ""):
        super().__init__(message)


class RequestError(_Error, IOError):

    def __init__(self, message):
        super().__init__(str(message))


class Timeout(RequestError, TimeoutError):

    def __init__(self, message):
        super().__init__(str(message))


class ValidationError(_Error):

    def __init__(self, message):
        super().__init__(str(message))


class ParseError(_Error):

    def __init__(self, message):
        super().__init__(str(message))
