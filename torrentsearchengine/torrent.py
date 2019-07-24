from .utils import simple_hash


class Torrent:

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
        self._kwargs = kwargs

        self.provider = self._kwargs.pop('provider')
        self.name = self._kwargs.pop('name')
        self.info_url = self._kwargs.pop('info_url', "")
        self.size = self._kwargs.pop('size', "")
        self.seeds = self._kwargs.pop('seeds', -1)
        self.leeches = self._kwargs.pop('leeches', -1)

        # convert seeds to int
        try:
            self.seeds = int(self.seeds)
        except Exception:
            self.seeds = -1
        # convert leeches to int
        try:
            self.leeches = int(self.leeches)
        except Exception:
            self.leeches = -1

        self._details = None

        self.id = simple_hash(str(self.provider) + ";" + self.name)

    def fetch_details(self, timeout=30) -> dict:
        if self._details is None:
            details = self.provider.fetch_details(self, timeout)
            # the torrent details are a combination of the data
            # we already have and the new data found in the info page
            self._details = {**self._kwargs, **self.asdict(), **details}
        return self._details

    def asdict(self) -> dict:
        return {"id": self.id, "provider": self.provider.name,
                "name": self.name, "info_url": self.info_url,
                "size": self.size, "seeds": self.seeds,
                "leeches": self.leeches}

    def __str__(self):
        return self.name
