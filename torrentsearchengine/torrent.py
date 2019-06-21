from torrentsearchengine.utils import KwArgs


class Torrent:

    def __init__(self, **kwargs: dict):
        """
        Parameters:
            provider: TorrentProvider - The provider that provided this torrent.
            title: str - The title of this torrent.
            url: str - The info page path of this torrent.
            size: str - The size of this torrent.
            time: str - When this torrent was released.
            seeds: int - The number of seeders.
            leechers: int - The number of leechers.

        Returns:
            Torrent
        """
        kwargs = KwArgs(kwargs)

        self.provider = kwargs.get('provider')
        self.title = kwargs.getstr('title')
        self.url = kwargs.getstr('url')
        self.size = kwargs.getstr('size')
        self.time = kwargs.getstr('time')
        self.seeds = kwargs.getint('seeds', -1)
        self.leechers = kwargs.getint('leechers', -1)

        self._magnet = kwargs.getstr('magnet')

        self.id = str(self.provider) + ";" + self.title

    def fetch_magnet(self) -> str:
        """
        Fetch the magnet uri of this torrent.

        Returns:
            str - The torrent magnet uri or an empty
                  string if the magnet is not found.
        """
        return self.provider.fetch_magnet(self)

    def asdict(self) -> dict:
        return {"id": self.id, "provider": self.provider.name,
                "title": self.title, "url": self.url, "size": self.size,
                "seeds": self.seeds, "leechers": self.leechers}

    def __str__(self):
        return str(self.asdict())
