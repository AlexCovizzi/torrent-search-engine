from typing import Union, Tuple, Any


class KwArgs:

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

    def items(self):
        return self.kwargs.items()

    def get(self, key: Union[str, int, Tuple], default: Any = None):
        value = self.kwargs.get(key, default)
        return value

    def getstr(self, key: Union[str, int, Tuple], default: str = ""):
        value = self.get(key, default)
        try:
            return str(value)
        except Exception:
            return default

    def getint(self, key: Union[str, int, Tuple], default: int = 0):
        value = self.get(key, default)
        try:
            return int(value)
        except Exception:
            return default

    def getdict(self, key: Union[str, int, Tuple], default: dict = {}):
        value = self.get(key, default)
        if isinstance(value, dict):
            return value
        else:
            return default
