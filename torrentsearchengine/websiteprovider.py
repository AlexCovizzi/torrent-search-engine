from typing import Any, List
import requests
from torrentsearchengine.exceptions import ProviderSearchError
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.scraper import Scraper
from torrentsearchengine.scraper.selector import Selector, NullSelector
from torrentsearchengine.torrent import Torrent


class WebsiteTorrentProvider(TorrentProvider):

    def __init__(self, pid: str, **kwargs: dict):
        name = str(kwargs.get('name', pid))
        url = str(kwargs.get('url', ''))
        user_agent = str(kwargs.get('userAgent', ''))

        self.search_path = str(kwargs.get('search', ''))

        next_page_url_selector = str(kwargs.get('list', {}).get('next', ''))
        items_selector = str(kwargs.get('list', {}).get('items', ''))
        list_item_selectors = kwargs.get('list', {}).get('item', {})
        item_selectors = kwargs.get('item', {})

        self.next_page_url_selector = Selector.parse(next_page_url_selector)
        self.items_selector = Selector.parse(items_selector)
        self.list_item_selectors = {key: Selector.parse(str(s)) for key, s in list_item_selectors.items()}
        self.item_selectors = {key: Selector.parse(str(s)) for key, s in item_selectors.items()}

        super(WebsiteTorrentProvider, self).__init__(pid, name, url, user_agent)

    def search(self, query: str, limit: int = 0) -> List[Torrent]:
        torrents = []

        path = self.search_path.format(query=query)

        try:
            response = self.fetch(path)
        except requests.exceptions.HTTPError as e:
            raise ProviderSearchError(e.request, e.strerror)

        if response.status_code not in range(200, 300):
            raise ProviderSearchError(response.request, "responded with status code " + str(response.status_code))

        scraper = Scraper(response.text)

        items = scraper.select(self.items_selector, limit=limit)
        for item in items:
            props = {"provider_id": self.id, "provider": self.name}
            for key, selector in self.list_item_selectors.items():
                prop = item.select_one(selector.css).attr(selector.attr).re(selector.re)
                props[key] = prop

            torrent = Torrent(**props)
            torrents.append(torrent)

        return torrents

    def fetch_magnet(self, torrent: Torrent) -> str:
        magnet = torrent.magnet
        if magnet:
            return magnet

        path = torrent.url
        if not path:
            return ''

        selector = self.item_selectors.get('magnet', NullSelector())

        response = self.fetch(path)
        scraper = Scraper(response.text)

        magnet = scraper.select_one(selector.css).attr(selector.attr).re(selector.re)

        torrent.magnet = magnet

        return magnet


if __name__ == '__main__':
    import json

    path = 'C:\\Users\\Alex\Documents\\torrent-tv\\torrenttv\\search_engine\\eztv.json'
    with open(path, 'r', encoding='utf-8') as f:
        provider_dict = json.load(f).get('eztv', {})

    provider = ScrapeTorrentProvider('eztv', **provider_dict)

    results = provider.search_torrents('game of thrones', 5)
    for result in results:
        print(str(result))
