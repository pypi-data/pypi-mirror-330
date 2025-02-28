"""Pelican federation interactions."""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from functools import cache

from urllib3.util import parse_url

KNOWN_FEDERATIONS = {
    "osdf": "osg-htc.org",
    "stash": "osg-htc.org",  # legacy handle
}


@cache
def federation_url(
    url: str,
) -> str:
    """Parse a federation discovery URL from a federation name or a Pelican URL.

    This function just matches known federation names and returns their
    cached discovery URL, otherwise returns the input unmodified.

    Parameters
    ----------
    url : `str`
        The URL to parse, or the common name of a known federation.

    Returns
    -------
    fedurl : `str`
        The federation URL of the known federation.

    Examples
    --------
    >>> federation_url("osdf")
    'osg-htc.org'
    >>> federation_url("osdf:///igwn/ligo/README")
    'osg-htc.org'
    >>> federation_url("pelican://osg-htc.org/igwn/ligo/README")
    'osg-htc.org'
    >>> federation_url("my-federation.org")
    'my-federation.org'
    >>> federation_url("pelican://my-federation.org/igwn/ligo/README")
    'my-federation.org'
    """
    try:
        return KNOWN_FEDERATIONS[url.lower()]
    except KeyError:
        if "/" in url:
            parsed = parse_url(url)
            if parsed.host:
                return parsed.host
            if parsed.scheme:
                return federation_url(parsed.scheme.rsplit("+", 1)[-1])
        return url
