"""Pytest configuration for `requests_pelican`."""

import logging
import re
from random import shuffle

import pytest
from urllib3.response import HTTPHeaderDict

from requests_pelican.config import PELICAN_CONFIGURATION_PATH

TEST_FEDERATION = "pelican.example.com"
TEST_FEDERATION_CONFIG_URL = (
    f"https://{TEST_FEDERATION}{PELICAN_CONFIGURATION_PATH}"
)
TEST_FEDERATION_CONFIG = {
  "director_endpoint": f"https://director.{TEST_FEDERATION}",
  "namespace_registration_endpoint": f"https://registry.{TEST_FEDERATION}",
  "jwks_uri": f"https://directory.{TEST_FEDERATION}/.well-known/issuer.jwks",
}

TEST_CACHES = [
    "https://cache1.example.com:443",
    "https://cache2.example.com:443",
    "https://cache3.example.com:443",
]
shuffle(TEST_CACHES)  # enables checking of sortedness

TEST_PATHS = [
    "/test/data/1",
    "/test/data/2",
    "/test/data/3",
]
TEST_PATH_DNE = "/test/bad"


@pytest.fixture
def pelican_mock(requests_mock):
    """Configure a mocked Pelican federation."""
    # pelican configuration
    requests_mock.get(
        TEST_FEDERATION_CONFIG_URL,
        json=TEST_FEDERATION_CONFIG,
    )

    # director response
    director = TEST_FEDERATION_CONFIG["director_endpoint"]
    for path in TEST_PATHS:
        durl = f"{director}{path}"
        headers = HTTPHeaderDict()
        for cache in TEST_CACHES:
            link = f"{cache}{path}"
            match = re.search(r"cache(\d+).example.com", cache)
            if match and (pri := match.groups()[0]) == 1:
                headers.add("Location", link)
            headers.add(
                "Link",
                f'<{link}>; rel="duplicate"; pri={pri}; depth=3"',
            )
        for value in (
            "namespace=/test",
            "require-token=false",
        ):
            headers.add("X-Pelican-Namespace", value)
        for issuer in (
            "https://token.example.com/test",
            "https://token-test.example.com/test",
        ):
            headers.add("X-Pelican-Authorization", f"issuer={issuer}")
        for meth in (requests_mock.get, requests_mock.head):
            meth(
                durl,
                headers=headers,
                status_code=307,
            )

    # cache responses
    for cache in TEST_CACHES:
        for path in TEST_PATHS:
            url = f"{cache}{path}"
            text = f"Data path {path.rsplit('/', 1)[-1]}"
            requests_mock.get(url, text=text)
        requests_mock.get(
            re.compile(f"{TEST_PATH_DNE}.*"),
            status_code=404,
        )

    return requests_mock


def _set_debug_log(name):
    logging.getLogger(name).setLevel(logging.DEBUG)


for mod in (
    "adapters",
    "auth",
    "director",
):
    _set_debug_log(f"requests_pelican.{mod}")
