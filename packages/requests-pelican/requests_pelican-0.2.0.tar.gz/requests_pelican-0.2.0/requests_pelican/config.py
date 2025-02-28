"""Pelican configuration interactions."""

from functools import cache
from typing import (
    Any,
)

from .federation import (
    federation_url,
)
from .utils import (
    _pooled_request,
    make_url,
)

PELICAN_CONFIGURATION_PATH = "/.well-known/pelican-configuration"


@cache
def pelican_configuration_url(
    federation: str,
) -> str:
    """Construct the URL of the pelican configuration of a federation.

    Parameters
    ----------
    federation : `str`
        The Pelican federation name or discovery URL.

    Returns
    -------
    url : `str`
        The fully qualified URL of the pelican configuration endpoint.

    Examples
    --------
    >>> pelican_configuration_url("my-federation.org")
    'https://my-federation.org/.well-known/pelican-configuration'
    >>> pelican_configuration_url("OSDF")
    'https://osg-htc.org/.well-known/pelican-configuration'
    """
    return make_url(
        federation_url(federation),
        PELICAN_CONFIGURATION_PATH,
        scheme="https",
    )


def get_pelican_configuration(
    federation: str,
    timeout: int = 60,
    **kwargs: Any,
) -> dict[str, Any]:
    """Query for the Pelican federation configuration using HTTP GET."""
    url = pelican_configuration_url(federation)
    resp = _pooled_request(
        url,
        timeout=timeout,
        **kwargs,
    )
    resp.raise_for_status()
    return resp.json()
