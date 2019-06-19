from re import match


class Selector:

    def __init__(self, css: str = '', attr: str = None, re: str = None):
        self.css = css
        self.attr = attr
        self.re = re

    def asdict(self) -> dict:
        return {"css": self.css, "attr": self.attr, "re": self.re}

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
        re_part = parts[1] if len(parts) > 1 and \
            parts[1].startswith('re:') else None
        if re_part:
            m = match(r"re:\s*(.*)\s*", re_part)
            if m:
                regex = m.group(1).strip()

        return Selector(css, attr, regex)


class NullSelector(Selector):

    def __init__(self):
        super(NullSelector, self).__init__()
