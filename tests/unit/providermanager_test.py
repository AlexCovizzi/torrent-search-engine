from unittest.mock import patch, Mock
import requests
from torrentsearchengine import TorrentProvider
from torrentsearchengine.providermanager import TorrentProviderManager


class FakeTorrentProvider(TorrentProvider):

    def search(self, query, limit):
        return []

    def fetch_magnet(self, torrent):
        return ""


def test_get_should_return_the_provider_with_the_id_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider1 = FakeTorrentProvider("id1", "name1", "url1")
    provider2 = FakeTorrentProvider("id2", "name2", "url2")
    provider_manager.add_one(provider1)
    provider_manager.add_one(provider2)

    provider_by_id = provider_manager.get(provider1.id)

    assert provider_by_id.id == provider1.id


def test_getall_should_return_the_providers_with_the_name_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider1 = FakeTorrentProvider("id1", "name", "url1")
    provider2 = FakeTorrentProvider("id2", "name", "url2")
    provider3 = FakeTorrentProvider("id3", "name2", "url2")
    provider4 = FakeTorrentProvider("id4", "name3", "url2")
    provider_manager.add_one(provider1)
    provider_manager.add_one(provider2)
    provider_manager.add_one(provider3)
    provider_manager.add_one(provider4)

    providers_by_name = provider_manager.getall(name=provider1.name)

    assert len(providers_by_name) == 2
    assert providers_by_name[0].name == provider1.name
    assert providers_by_name[1].name == provider1.name


def test_add_one_should_add_the_provider():
    provider_manager = TorrentProviderManager()
    provider = FakeTorrentProvider("id", "name", "url")
    provider_manager.add_one(provider)

    provider_by_id = provider_manager.get(provider.id)

    assert provider_by_id == provider
