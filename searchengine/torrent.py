class Torrent:

    def __init__(self, **kwargs: dict):
        self.provider_id = kwargs.get('provider_id', '')
        self.provider = kwargs.get('provider', '')
        self.title = kwargs.get('title', '')
        self.url = kwargs.get('url', '')
        self.size = kwargs.get('size', '')
        self.time = kwargs.get('time', '')
        self.seeds = kwargs.get('seeds', -1)
        self.leechers = kwargs.get('leechers', -1)
        self.magnet = kwargs.get('magnet', '')

    def to_dict(self):
        return {
            "provider_id": self.provider_id,
            "provider": self.provider,
            "title": self.title,
            "url": self.url,
            "size": self.size,
            "seeds": self.seeds,
            "leechers": self.leechers,
            "magnet": self.magnet
        }

    def __str__(self):
        s = "(provider: {provider}, title: {title}, url: {url}, size: {size}, time: {time},"
        s += "seeds: {seeds}, leechers: {leechers}, magnet: {magnet})"
        s = s.format(provider=self.provider, title=self.title, url=self.url, size=self.size, time=self.time,
                     seeds=self.seeds, leechers=self.leechers, magnet=self.magnet)
        return s
