from unittest.mock import patch, Mock
import requests
from torrentsearchengine import TorrentProvider
from torrentsearchengine.providermanager import TorrentProviderManager


class FakeTorrentProvider(TorrentProvider):

    def search(self, query, limit):
        return []

    def fetch_magnet(self, torrent):
        return ""


def test_add_should_add_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider1 = FakeTorrentProvider("name1", "name1", "url1")
    provider2 = FakeTorrentProvider("name2", "name2", "url2")
    provider_manager.add(provider1, provider2)

    returned_provider1 = provider_manager.get(provider1.name)
    returned_provider2 = provider_manager.get(provider2.name)

    assert returned_provider1 == provider1
    assert returned_provider2 == provider2


def test_disable_should_disable_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider = FakeTorrentProvider("name", "name", "url", enabled=True)
    provider_manager.add(provider)

    provider_manager.disable(provider.name)

    assert not provider.enabled


def test_enable_should_enable_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider = FakeTorrentProvider("name", "name", "url", enabled=True)
    provider_manager.add(provider)

    provider_manager.enable(provider.name)

    assert provider.enabled


def test_remove_should_remove_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider = FakeTorrentProvider("name", "name", "url", enabled=True)
    provider_manager.add(provider)

    provider_manager.remove(provider.name)

    assert not provider_manager.get(provider.name)

