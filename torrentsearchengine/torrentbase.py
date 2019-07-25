from .utils import simple_hash


# base implementation of a torrent, it has only the main properties
# extended by Torrent and TorrentDetails
class TorrentBase:

    def __init__(self, **kwargs: dict):
        """
        Parameters:
            provider: TorrentProvider - The provider.
            name: str - The name of this torrent.
            url: str - The info page path of this torrent.
            size: str - The size of this torrent.
            seeds: int - The number of seeders.
            leeches: int - The number of leeches.
        """
        self.data = kwargs
        self.id = simple_hash(str(self.provider) + ";" + self.name)

    @property
    def provider(self):
        return self.data.get("provider")

    @property
    def name(self):
        return self.data.get("name")

    @property
    def info_url(self):
        return self.data.get("info_url", "")

    @property
    def size(self):
        return self.data.get("size", "")

    @property
    def seeds(self):
        seeds = self.data.get("seeds", -1)
        try:
            return int(seeds)
        except Exception:
            return -1

    @property
    def leeches(self):
        leeches = self.data.get("leeches", -1)
        try:
            return int(leeches)
        except Exception:
            return -1

    def asdict(self) -> dict:
        return {"id": self.id, "provider": self.provider.name,
                "name": self.name, "info_url": self.info_url,
                "size": self.size, "seeds": self.seeds,
                "leeches": self.leeches}

    def __str__(self):
        return self.name
