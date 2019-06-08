from typing import List, Union, Optional
import json
from torrentsearchengine.providervalidator import torrent_provider_validator
from torrentsearchengine.provider import TorrentProvider
from torrentsearchengine.websiteprovider import WebsiteTorrentProvider


class TorrentProviderManager:

    def __init__(self):
        self.providers = {}

    def add(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            pdict = json.load(f)

        torrent_provider_validator.validate(pdict)

        for key, value in pdict.items():
            provider = WebsiteTorrentProvider(key, **value)
            provider_dict = {"provider": provider, "enabled": True}
            self.providers[key] = provider_dict

    def remove(self, provider: Union[str, TorrentProvider]):
        provider_id = provider if isinstance(provider, str) else provider.id
        try:
            del self.providers[provider_id]
        except KeyError:
            pass

    def clear(self):
        self.providers = {}

    def disable(self, provider: Union[str, TorrentProvider]):
        provider_id = provider if isinstance(provider, str) else provider.id
        provider_dict = self.providers.get(provider_id)
        if provider_dict:
            provider_dict["enabled"] = False

    def enable(self, provider: Union[str, TorrentProvider]):
        provider_id = provider if isinstance(provider, str) else provider.id
        provider_dict = self.providers.get(provider_id)
        if provider_dict:
            provider_dict["enabled"] = True

    def get_all(self) -> List[TorrentProvider]:
        return [provider_dict.get("provider")
                for provider_dict in self.providers.values()]

    def get_enabled(self) -> List[TorrentProvider]:
        return [provider_dict.get("provider")
                for provider_dict in self.providers.values()
                if provider_dict.get("enabled")]

    def get_disabled(self) -> List[TorrentProvider]:
        return [provider_dict.get("provider")
                for provider_dict in self.providers.values()
                if not provider_dict.get("enabled")]

    def get(self, provider_id: str) -> Optional[TorrentProvider]:
        return self.providers.get(provider_id, None)
