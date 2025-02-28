"""Tests for `requests_pelican.utils`."""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import pytest

from requests_pelican import (
    __version__,
    utils as rp_utils,
)


@pytest.mark.parametrize(("args", "kwargs", "result"), [
    pytest.param(
        ("example.com",),
        {},
        "https://example.com",
        id="hostname",
    ),
    pytest.param(
        ("http://example.com",),
        {},
        "http://example.com",
        id="scheme://hostname",
    ),
    pytest.param(
        ("example.com:80",),
        {},
        "http://example.com:80",
        id="scheme://hostname:port",
    ),
    pytest.param(
        ("example.com:8000",),
        {},
        "http://example.com:8000",
        id="hostname:port http",
    ),
    pytest.param(
        ("example.com:8443",),
        {},
        "https://example.com:8443",
        id="hostname:port https",
    ),
    pytest.param(
        ("example.com", "/path", "/path2"),
        {},
        "https://example.com/path/path2",
        id="hostame/paths",
    ),
    pytest.param(
        ("example.com/path", "path2/"),
        {},
        "https://example.com/path/path2/",
        id="hostname/path/paths",
    ),
    pytest.param(
        ("example.com:80/path", "path2"),
        {},
        "http://example.com:80/path/path2",
        id="hostname:80/paths",
    ),
    # host including port and path but duplicate port keyword
    pytest.param(
        ("example.com:80/path", "path2"),
        {"port": 1234},
        "http://example.com:80/path/path2",
        id="hostname:80/path/paths",
    ),
    # kwargs
    pytest.param(
        ("example.com", "path", "path2"),
        {
            "scheme": "imap",
            "port": 1234,
            "query": "a=1",
            "fragment": "loc",
        },
        "imap://example.com:1234/path/path2?a=1#loc",
        id="imap",
    ),
    pytest.param(
        ("example.com", "path", "path2"),
        {
            "scheme": "imap",
            "port": 1234,
            "query": {"key": "value", "key2": 0},
            "fragment": "loc",
        },
        "imap://example.com:1234/path/path2?key=value&key2=0#loc",
        id="idmap?query",
    ),
])
def test_make_url(args, kwargs, result):
    """Test `make_url()`."""
    assert rp_utils.make_url(*args, **kwargs) == result


def test_default_user_agent():
    """Test `default_user_agent()`."""
    assert rp_utils.default_user_agent() == f"requests-pelican/{__version__}"
    assert rp_utils.default_user_agent("test") == f"test/{__version__}"
