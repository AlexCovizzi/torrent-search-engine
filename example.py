from torrentsearchengine import TorrentSearchEngine

path = 'providers.json'

engine = TorrentSearchEngine()
engine.add_providers(path)

results = engine.search('doom patrol')
for result in results:
    print(str(result))
    pass
for err in engine.errors:
    print(str(err))
    pass
