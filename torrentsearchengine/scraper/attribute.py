from typing import Any
import re


class Attribute:

    def __init__(self, value: Any):
        self.value = value

    def get(self) -> Any:
        return self.value

    def re(self, regex: str, fmt: str = None) -> str:
        if not regex:
            return self.to_string()

        value = self.value if isinstance(self.value, str) else self.to_string()
        # if no format is specified we just return the matched string
        if not fmt:
            match = re.match(regex, value)
            if match:
                value = match.group(0)
        # otherwise we replace
        else:
            value = re.sub(regex, fmt, value)

        return value

    def to_string(self, default: str = "") -> str:
        if self.value is None:
            return default
        try:
            return str(self.value)
        except Exception:
            return default

    def to_int(self, default: int = 0) -> int:
        try:
            return int(self.value)
        except Exception:
            return default

    def __str__(self):
        return self.to_string()


class NullAttribute(Attribute):

    def __init__(self):
        super(NullAttribute, self).__init__(None)
