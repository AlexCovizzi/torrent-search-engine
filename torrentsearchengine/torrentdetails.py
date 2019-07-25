from .torrentbase import TorrentBase


# TorrentDetails has the same data as TorrentBase and some more data
class TorrentDetails(TorrentBase):

    @property
    def time(self):
        return self.data.get("time", "")

    @property
    def link(self):
        return self.data.get("link", "")

    @property
    def files(self):
        return self.data.get("files", [])

    @property
    def infohash(self):
        return self.data.get("infohash", "")

    @property
    def description(self):
        return self.data.get("description", "")

    @property
    def uploader(self):
        return self.data.get("uploader", "")

    @property
    def uploader_url(self):
        return self.data.get("uploader_url", "")

    @property
    def trackers(self):
        return self.data.get("trackers", [])

    def asdict(self):
        return {"id": self.id, "provider": self.provider.name,
                "name": self.name, "info_url": self.info_url,
                "size": self.size, "seeds": self.seeds,
                "leeches": self.leeches, "time": self.time,
                "link": self.link, "files": self.files,
                "infohash": self.infohash, "description": self.description,
                "uploader": self.uploader, "uploader_url": self.uploader_url,
                "trackers": self.trackers}
