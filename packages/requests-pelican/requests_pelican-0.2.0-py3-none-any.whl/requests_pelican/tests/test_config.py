"""Tests for `requests_pelican.config`."""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import pytest

from requests_pelican import config as rp_config


@pytest.mark.parametrize(("federation", "result"), [
    # federation url
    (
        "my-federation.org",
        "https://my-federation.org/.well-known/pelican-configuration",
    ),
    # known federation name
    (
        "osdf",
        "https://osg-htc.org/.well-known/pelican-configuration",
    ),
])
def test_pelican_configuration_url(federation, result):
    """Test `requests_pelican.config.pelican_configuration_url`."""
    assert rp_config.pelican_configuration_url(federation) == result


@pytest.mark.usefixtures("pelican_mock")
def test_get_pelican_configuration():
    """Test `requests_pelican.config.pelican_configuration_url`."""
    conf = rp_config.get_pelican_configuration(
        "pelican.example.com",
    )
    assert conf["director_endpoint"] == "https://director.pelican.example.com"
