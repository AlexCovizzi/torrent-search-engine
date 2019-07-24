from re import match
import soupsieve


class Selector:

    def __init__(self, css: str = '', attr: str = None, re: str = None,
                 fmt: str = None):
        self.css = css
        self.attr = attr
        self.re = re
        self.fmt = fmt

    def asdict(self) -> dict:
        return {"css": self.css, "attr": self.attr, "re": self.re,
                "fmt": self.fmt}

    def has_attr(self) -> bool:
        return self.attr is not None

    def has_re(self) -> bool:
        return self.re is not None

    def has_fmt(self) -> bool:
        return self.fmt is not None

    def __str__(self):
        return str(self.asdict())

    @staticmethod
    def parse(selector: str) -> "Selector":
        """
        Selector format is: <css selector>@<attribute> | re:<formatter>
        """
        parts = selector.split('|')
        parts = [part.strip() for part in parts]

        attr_selector = parts[0] if len(parts) > 0 else ''

        attr_selector_parts = attr_selector.split('@')
        attr_selector_parts = [part.strip() for part in attr_selector_parts]

        css = attr_selector_parts[0] if len(attr_selector_parts) > 0 else ''
        attr = attr_selector_parts[1] if len(attr_selector_parts) > 1 else None

        regex = None
        fmt = None
        for part in parts[1:]:
            if part.startswith('re:'):
                m = match(r"re:\s*(.*)\s*", part)
                if m:
                    regex = m.group(1).strip()
            elif part.startswith('fmt:'):
                m = match(r"fmt:\s*(.*)\s*", part)
                if m:
                    fmt = m.group(1).strip()

        if css:
            soupsieve.compile(css)

        return Selector(css, attr, regex, fmt)


class NullSelector(Selector):

    def __init__(self):
        super(NullSelector, self).__init__()
