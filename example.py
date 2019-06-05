from torrentsearchengine.providerfactory import TorrentProviderFactory

path = 'providers.json'

factory = TorrentProviderFactory()
providers = factory.createall(path)

results = providers[0].search('game of thrones', 5)
for result in results:
    print(str(result))
