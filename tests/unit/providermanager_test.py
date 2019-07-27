import pytest
import os
import requests
from torrentsearchengine import TorrentProvider, ValidationError, RequestError
from torrentsearchengine.providermanager import TorrentProviderManager


def test_add_should_add_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider1 = TorrentProvider(validate=False, name="name1")
    provider2 = TorrentProvider(validate=False, name="name2")
    provider_manager.add(provider1)
    provider_manager.add(provider2)

    returned_provider1 = provider_manager.get(provider1.name)
    returned_provider2 = provider_manager.get(provider2.name)

    assert returned_provider1 == provider1
    assert returned_provider2 == provider2


def test_add_raises_IOError_if_the_path_is_not_a_file():
    provider_manager = TorrentProviderManager()
    with pytest.raises(IOError):
        provider_manager.add(os.path.join(__file__, "nope.json"))


def test_add_raises_ValidationError_if_the_path_is_not_a_json(tmpdir):
    path = tmpdir.join("fake.json")
    path.write("{\"value\": {}, } }")
    provider_manager = TorrentProviderManager()
    with pytest.raises(ValidationError):
        provider_manager.add(str(path))


def test_add_raises_ValidationError_if_the_path_is_not_a_valid_json(tmpdir):
    path = tmpdir.join("invalid.json")
    path.write("""
    {
        "name": "nm",
        "fullname": "hello",
        "search": 1234
    }
    """)
    provider_manager = TorrentProviderManager()
    with pytest.raises(ValidationError):
        provider_manager.add(str(path))


def test_add_raises_RequestError_if_the_url_is_not_valid():
    url = "http://localhost:12000/nope"
    provider_manager = TorrentProviderManager()
    with pytest.raises(RequestError):
        provider_manager.add(url)


def test_disable_should_disable_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider = TorrentProvider(validate=False, name="name")
    provider_manager.add(provider)

    provider_manager.disable(provider.name)

    assert not provider.enabled


def test_enable_should_enable_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider = TorrentProvider(validate=False, name="name")
    provider.disable()
    provider_manager.add(provider)

    provider_manager.enable(provider.name)

    assert provider.enabled


def test_remove_should_remove_the_provider_passed_as_argument():
    provider_manager = TorrentProviderManager()
    provider = TorrentProvider(validate=False, name="name")
    provider_manager.add(provider)

    provider_manager.remove(provider.name)

    assert not provider_manager.get(provider.name)
