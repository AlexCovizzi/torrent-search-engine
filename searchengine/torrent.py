from collections import namedtuple


Torrent = namedtuple('Torrent', 'title, url, size, time, seeds, leechers, magnet')
