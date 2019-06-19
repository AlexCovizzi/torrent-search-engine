from typing import List, Union, Optional
import json
import logging
from torrentsearchengine.providervalidator import torrent_provider_validator
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.websiteprovider import WebsiteTorrentProvider


logger = logging.getLogger(__name__)


class TorrentProviderManager:

    def __init__(self):
        self.providers = {}

    def add(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            pdict = json.load(f)

        torrent_provider_validator.validate(pdict)

        for key, value in pdict.items():
            provider = WebsiteTorrentProvider(key, **value)
            self.add_one(key, provider)

    def add_one(self, provider: TorrentProvider):
            provider_dict = {"provider": provider, "enabled": True}
            self.providers[provider.id] = provider_dict

            logger.debug("Added provider:\n{}"
                         .format(json.dumps(provider.asdict(), indent=2,
                                            sort_keys=True)))

    def clear(self):
        n_providers = len(self.providers.items())
        self.providers = {}
        logger.debug("Cleared providers ({}): ".format(n_providers))

    def remove(self, *names: List[str]):
        for name in names:
            self._remove(name)

    def disable(self, *names: List[str]):
        for name in names:
            self._disable(name)

    def enable(self, *names: List[str]):
        for name in names:
            self._enable(name)

    def getall(self, name=None, enabled=None) -> List[TorrentProvider]:
        return [item.get("provider")
                for item in self.providers.values()
                if (name is None or name == item["provider"].name) and
                   (enabled is None or enabled == item["enabled"])]

    def get(self, pid: str) -> Optional[TorrentProvider]:
        item = self.providers.get(pid)
        if item:
            return item["provider"]
        else:
            return None

    def _remove(self, name: str):
        rem = []
        for key, value in self.providers.items():
            provider = value["provider"]
            if provider.name == name:
                rem.append(key)
        for key in rem:
            del self.providers[key]
            logger.debug("Removed provider: {}".format(key))

    def _disable(self, name: str):
        for key, value in self.providers.items():
            provider = value["provider"]
            if provider.name == name:
                value["enabled"] = False
                logger.debug("Disabled provider: {}".format(provider_id))

    def _enable(self, name: str):
        for key, value in self.providers.items():
            provider = value["provider"]
            if provider.name == name:
                value["enabled"] = True
                logger.debug("Enabled provider: {}".format(provider_id))
