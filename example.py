import requests
from torrentsearchengine import TorrentSearchEngine
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

engine = TorrentSearchEngine()
engine.add_provider('examples/eztv.json')
# engine.add_provider('examples/ettv.json')
# engine.add_provider('examples/1337x.json')
# engine.disable_providers("magnetdl")

results = engine.search('breaking bad s04e06', 1, n_threads=1, timeout=5)
print(len(results))

for result in [r.fetch_details() for r in results]:
    print(result.asdict()["description"])
    pass
"""
import requests
import bs4

res = requests.get("https://rarbgmirror.com/torrents.php?search=doom%20patrol")
print(res.text.encode("utf-8"))
soup = bs4.BeautifulSoup(res.text, 'html.parser')
print(soup.select("table.table > tr"))

"""
