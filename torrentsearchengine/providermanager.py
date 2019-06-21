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

    def add(self, *providers: List[TorrentProvider]):
        for provider in providers:
            self._add(provider)

    def add_from_file(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            pdict = json.load(f)

        torrent_provider_validator.validate(pdict)

        for key, value in pdict.items():
            provider = WebsiteTorrentProvider(key, **value)
            self._add(provider)

    def get(self, name: str) -> Optional[TorrentProvider]:
        return self.providers.get(name, None)

    def get_all(self, enabled=None) -> List[TorrentProvider]:
        return [provider
                for provider in self.providers.values()
                if enabled is None or enabled == provider.enabled]

    def remove(self, *providers: List[Union[TorrentProvider, str]]):
        for provider in providers:
            self._remove(provider)

    def remove_all(self):
        providers = self.get_all()
        self.remove(*providers)

    def disable(self, *providers: List[Union[TorrentProvider, str]]):
        for provider in providers:
            self._disable(provider)

    def disable_all(self):
        providers = self.get_all()
        self.disable(*providers)

    def enable(self, *providers: List[Union[TorrentProvider, str]]):
        for provider in providers:
            self._enable(provider)

    def enable_all(self):
        providers = self.get_all()
        self.enable(*providers)

    def _add(self, provider: TorrentProvider):
        self.providers[provider.name] = provider

        logger.debug("Added provider:\n{}".format(json.dumps(provider.asdict(),
                                                  indent=2, sort_keys=True)))

    def _remove(self, provider: Union[str, TorrentProvider]):
        provider_name = provider.name if isinstance(provider, TorrentProvider) \
                                  else provider
        if provider_name in self.providers:
            del self.providers[provider_name]
            logger.debug("Removed provider: {}".format(provider_name))

    def _disable(self, provider: Union[str, TorrentProvider]):
        provider = provider if isinstance(provider, TorrentProvider) \
                            else self.providers.get(provider, None)
        if provider:
            provider.disable()

    def _enable(self, provider: Union[str, TorrentProvider]):
        provider = provider if isinstance(provider, TorrentProvider) \
                            else self.providers.get(provider_id, None)
        if provider:
            provider.enable()
