from .utils import simple_hash
from .torrentbase import TorrentBase
from .torrentdetails import TorrentDetails


class Torrent(TorrentBase):

    def fetch_details(self, timeout=30) -> TorrentDetails:
        """
        Retrieve details about this torrent (e.g link, description, files...)

        Parameters:
            timeout: int - Timeout in seconds.

        Returns:
            TorrentDetails - Torrent details.

        Raises:
            ValueError - Missing some properties.
            RequestError - Something went wrong requesting the search page.
            Timeout - The search lasted longer than timeout.
        """
        details_data = self.provider.fetch_details_data(self, timeout)
        # the torrent details are a combination of the data
        # we already have and the new data found in the info page
        details = TorrentDetails(**{**self.data, **details_data})
        return details
