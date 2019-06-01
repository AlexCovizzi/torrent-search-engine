from urllib import parse
from re import match


def urljoin(*urls: str) -> str:
    if len(urls) == 0:
        return ""
    has_trailing_slash = True if urls[-1].endswith('/') else False
    return '/'.join([url.strip('/') for url in urls]) + ('/' if has_trailing_slash else '')


def urlfix(s: str, scheme: str = 'https') -> str:
    has_scheme = match('(?:http:|https:)?//', s)
    if not has_scheme:
        s = scheme + '://' + s
    scheme, netloc, path, qs, anchor = parse.urlsplit(s)
    path = parse.quote(path, '/%')
    qs = parse.quote_plus(qs, ':&=')
    return parse.urlunsplit((scheme, netloc, path, qs, anchor))
