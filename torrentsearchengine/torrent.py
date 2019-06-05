from torrentsearchengine.utils import KwArgs


class Torrent:

    def __init__(self, **kwargs: dict):
        kwargs = KwArgs(kwargs)

        self.provider = kwargs.get('provider')
        self.title = kwargs.getstr('title')
        self.url = kwargs.getstr('url')
        self.size = kwargs.getstr('size')
        self.time = kwargs.getstr('time')
        self.seeds = kwargs.getint('seeds', -1)
        self.leechers = kwargs.getint('leechers', -1)

        self._magnet = kwargs.getstr('magnet')

        self.id = self.provider.id + ";" + self.title

    def to_dict(self):
        return {
            "id": self.id,
            "provider": self.provider,
            "title": self.title,
            "url": self.url,
            "size": self.size,
            "seeds": self.seeds,
            "leechers": self.leechers
        }

    def __str__(self):
        return str(self.to_dict())
