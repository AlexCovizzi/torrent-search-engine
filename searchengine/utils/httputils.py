from typing import Tuple, Union, List
from re import match
from urllib import parse
import requests


def fetch_with_fallback(base_urls: Union[str, List[str]], path: str, user_agent: str = None):
    headers = {}
    if user_agent:
        headers['User-Agent'] = user_agent

    base_urls = [base_urls] if "str" in str(type(base_urls)) else base_urls

    for base_url in base_urls:
        url = join_url(base_url, path)
        url = fix_url(url, 'https')

        try:
            response = requests.get(url, headers=headers)
            if response.status_code in range(200, 300):
                return response
            print(str(response))
        except requests.exceptions.RequestException as e:
            print(str(e))

    raise Exception('Failed to fetch {path} from {urls}'.format(path=path, urls=', '.join(base_urls)))


def join_url(*urls) -> str:
    has_trailing_slash = urls[-1].endswith('/')
    trailing_slash = '/' if has_trailing_slash else ''
    return '/'.join([url.strip('/') for url in urls]) + trailing_slash


def fix_url(s: str, scheme='https') -> str:
    has_scheme = match('(?:http|https)://', s)
    if not has_scheme:
        s = scheme + '://' + s
    scheme, netloc, path, qs, anchor = parse.urlsplit(s)
    path = parse.quote(path, '/%')
    qs = parse.quote_plus(qs, ':&=')
    return parse.urlunsplit((scheme, netloc, path, qs, anchor))


def get_base_url(url: str) -> str:
    parts = parse.urlsplit(url)
    base_url = parse.urlunsplit((parts.scheme, parts.netloc, '', '', ''))
    return base_url


if __name__ == '__main__':
    url = 'eztv.yt/search'
    fixed = fix_url(url, 'https')
    print(fix_url(fixed))
