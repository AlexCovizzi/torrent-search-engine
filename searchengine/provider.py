from typing import Union, List, Any
import json
import os
from torrenttv.utils.stringutils import format_string
from torrenttv.search_engine.website import Website
from torrenttv.search_engine.scraper import Scraper
from torrenttv.search_engine.torrent import Torrent


class Provider(object):

    def __init__(self, provider_id: str, **kwargs: dict):
        super().__init__()

        self.id = provider_id
        self.name = kwargs.get('name', provider_id)
        self.url = kwargs.get('url', '')
        self.user_agent = kwargs.get('userAgent', '')
        self.search_path = kwargs.get('search', '')
        self.next_page_url_selector = kwargs.get('next', '')
        self.items_selector = kwargs.get('list', {}).get('items', '')
        self.list_item_selectors = kwargs.get('list', {}).get('item', {})
        self.item_selectors = kwargs.get('item', {})

        self.website = Website(self.url, self.user_agent)

    def get_torrents(self, query: str, limit: int = 50) -> List[Torrent]:
        torrents = []

        path = self.search_path.format(query=query)
        response = self.website.get(path)

        scraper = Scraper(response.text)

        while len(torrents) < limit:
            for element in scraper.get_all(self.items_selector, limit - len(torrents)):
                torrent = self.get_torrent(element)
                torrents.append(torrent)

            next_page_path = scraper.get_value(self.next_page_url_selector)
            if not next_page_path:
                break

            try:
                response = self.website.get(next_page_path)
            except IOError:
                # if it fails retrieving the page we return the torrents found
                break

            scraper = Scraper(response.text)

        return torrents

    def get_torrent(self, source: Any) -> Torrent:
        scraper = Scraper(source)

        title = scraper.get_value(self.list_item_selectors.get('title'))
        url = scraper.get_value(self.list_item_selectors.get('url'))
        size = scraper.get_value(self.list_item_selectors.get('size'))
        time = scraper.get_value(self.list_item_selectors.get('time'))
        seeds = scraper.get_value(self.list_item_selectors.get('seeds'))
        leechers = scraper.get_value(self.list_item_selectors.get('leechers'))
        magnet = scraper.get_value(self.list_item_selectors.get('magnet'))

        torrent = Torrent(title=title, url=url, size=size, time=time,
                          seeds=seeds, leechers=leechers, magnet=magnet)

        return torrent

    def get_magnet(self, torrent: Torrent) -> str:
        magnet = torrent.magnet
        if magnet:
            return magnet

        info_path = torrent.url
        if not info_path:
            return ''

        response = self.website.get(info_path)
        scraper = Scraper(response.text)

        magnet = scraper.get_value(self.item_selectors.get('magnet'))

        return magnet


if __name__ == '__main__':
    path = 'C:\\Users\\Alex\Documents\\torrent-tv\\torrenttv\\search_engine\\eztv.json'
    with open(path, 'r', encoding='utf-8') as f:
        provider_dict = json.load(f).get('eztv', {})

    provider = Provider('eztv', **provider_dict)

    results = provider.get_torrents('game of thrones', 5)
    for result in results:
        print(result)
        print(provider.get_magnet(result))
