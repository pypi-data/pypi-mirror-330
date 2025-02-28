"""Tests for `requests_pelican.director`."""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import pytest

from requests_pelican import director as rp_director


@pytest.mark.usefixtures("pelican_mock")
def test_get_director_response():
    """Basic test of the `get_director_response` function."""
    director = rp_director.get_director_response(
        "pelican://pelican.example.com/test/data/1",
    )
    assert director.namespace["namespace"] == "/test"
    assert not director.namespace["require-token"]


@pytest.mark.parametrize(
    ("path", "federation", "random"),
    [
        ("pelican://pelican.example.com/test/data/1", None, False),
        ("/test/data/1", "pelican.example.com", False),
        ("pelican://pelican.example.com/test/data/1", None, True),
    ],
)
@pytest.mark.usefixtures("pelican_mock")
def test_get_urls(path, federation, random):
    """Test `requests_pelican.directory.get_urls`."""
    urls = rp_director.get_urls(
        path,
        federation=federation,
        random=random,
    )
    expected = [
        "https://cache1.example.com:443/test/data/1",
        "https://cache2.example.com:443/test/data/1",
        "https://cache3.example.com:443/test/data/1",
    ]
    if random:
        assert sorted(urls) == expected
    else:
        assert urls == expected
