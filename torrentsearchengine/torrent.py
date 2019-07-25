from .utils import simple_hash
from .torrentbase import TorrentBase
from .torrentdetails import TorrentDetails


class Torrent(TorrentBase):

    def fetch_details(self, timeout=30) -> dict:
        details_data = self.provider.fetch_details_data(self, timeout)
        # the torrent details are a combination of the data
        # we already have and the new data found in the info page
        details = TorrentDetails(**{**self.data, **details_data})
        return details
