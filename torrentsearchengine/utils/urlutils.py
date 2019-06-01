from typing import Iterable
from urllib import parse
from re import match


def urljoin(*urls: Iterable[str]) -> str:
    if len(urls) == 0:
        return ""

    has_trailing_slash = True if urls[-1].endswith('/') else False
    joined = '/'.join([url.strip('/') for url in urls])
    joined = joined + ('/' if has_trailing_slash else '')
    return joined


def urlfix(s: str, scheme: str = 'https') -> str:
    has_scheme = match('(?:http:|https:)?//', s)
    if not has_scheme:
        s = scheme + '://' + s
    scheme, netloc, path, qs, anchor = parse.urlsplit(s)
    path = parse.quote(path, '/%')
    qs = parse.quote_plus(qs, ':&=')
    return parse.urlunsplit((scheme, netloc, path, qs, anchor))
