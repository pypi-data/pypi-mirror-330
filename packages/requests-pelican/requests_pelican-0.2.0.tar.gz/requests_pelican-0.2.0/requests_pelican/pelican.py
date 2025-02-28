"""Pelican URI handling."""

from __future__ import annotations

from functools import cache

from urllib3.util import (
    Url,
    parse_url,
)

from .federation import federation_url


@cache
def pelican_uri(
    uri: str,
    federation: str | None = None,
) -> str:
    """Properly format a Pelican federation URI.

    See <https://docs.pelicanplatform.org/getting-data-with-pelican/client#the-different-pelican-url-schemes>

    Parameters
    ----------
    uri : `str`
        The Pelican request URI to parse.

    federation : `str`, optional
        The Pelican federation name or URL.

    Returns
    -------
    uri : `str`
        The fully-qualified Pelican URI.

    Examples
    --------
    >>> pelican_uri("osdf:///igwn/ligo/README")
    'pelican://osg-htc.org/igwn/ligo/README'
    >>> pelican_uri("igwn+osdf:///igwn/ligo/README")
    'pelican://osg-htc.org/igwn/ligo/README'
    >>> pelican_uri("/igwn/ligo/README", "OSDF")
    'pelican://osg-htc.org/igwn/ligo/README'
    """
    parsed = parse_url(uri)
    host = parsed.host or federation_url(federation or uri)
    return str(Url(
        scheme="pelican",
        auth=parsed.auth,
        host=host,
        port=parsed.port,
        path=parsed.path,
        query=parsed.query,
        fragment=parsed.fragment,
    ))
