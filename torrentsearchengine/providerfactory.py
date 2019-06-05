from typing import Optional, List
import json
from torrentsearchengine.providervalidator import torrent_provider_validator
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.websiteprovider import WebsiteTorrentProvider
from torrentsearchengine.providervalidator import torrent_provider_validator


class TorrentProviderFactory:

    def __init__(self):
        pass

    def createall(self, path: str) -> List[TorrentProvider]:
        providers = []

        with open(path, 'r', encoding='utf-8') as f:
            pdict = json.load(f)
        
        torrent_provider_validator.validate(pdict)

        for key, value in pdict.items():
            provider = WebsiteTorrentProvider(key, **value)
            providers.append(provider)
        
        return providers

