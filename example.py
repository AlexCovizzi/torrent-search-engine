import requests
from torrentsearchengine import TorrentSearchEngine
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

engine = TorrentSearchEngine()
engine.add_provider('examples/eztv.json')
engine.add_provider('examples/ettv.json')
engine.add_provider('examples/1337x.json')
engine.add_provider('examples/magnetdl.json')
# engine.disable_providers("magnetdl")

results = engine.search('doom patrol s01e03', limit=50, timeout=5)
print(len(results))

for result in [r for r in results]:
    print("{}: {}".format(result.provider, result.name.encode("utf-8")))
    pass
