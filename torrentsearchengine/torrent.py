from torrentsearchengine.utils import KwArgs


class Torrent:

    def __init__(self, **kwargs: dict):
        kwargs = KwArgs(kwargs)

        self.provider_id = kwargs.getstr('provider_id')
        self.provider = kwargs.getstr('provider')
        self.title = kwargs.getstr('title')
        self.url = kwargs.getstr('url')
        self.size = kwargs.getstr('size')
        self.time = kwargs.getstr('time')
        self.seeds = kwargs.getint('seeds', -1)
        self.leechers = kwargs.getint('leechers', -1)
        self.magnet = kwargs.getstr('magnet')

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
        return str(self.to_dict())
