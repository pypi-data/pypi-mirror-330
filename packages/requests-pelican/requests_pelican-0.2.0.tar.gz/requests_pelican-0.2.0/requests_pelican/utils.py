"""Utilities for requests-pelican."""

from __future__ import annotations

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import typing

import requests
import requests.adapters
import requests.utils
from requests.models import PreparedRequest
from urllib3.util import (
    Url,
    parse_url,
)

from ._version import version as __version__

if typing.TYPE_CHECKING:
    from collections.abc import MutableMapping

# list of ports to be considered HTTP (not HTTPS)
HTTP_PORTS = [
    80,
    591,  # IANA HTTP alternative
    8000,  # XRootD over HTTP
    8008,  # IANA HTTP alternative
    8080,  # IANA HTTP alternative
]

_REQUESTS_USER_AGENT = requests.utils.default_user_agent()


def make_url(
    url: str,
    *paths: str,
    scheme: str | None = None,
    port: int | None = None,
    query: str | dict | None = None,
    fragment: str | None = None,
) -> str:
    """Construct a URL by combining a ``host`` and optional ``path``.

    url : `str`
        URL or part thereof.

    paths : `str`
        Zero or more path components to append to the full URL.

    scheme : `str`
        The scheme to use if not included in the ``host``.
        If ``host`` specifies port 80, this defaults to ``"http"``,
        otherwise ``"https"``.

    port : `int`
        The port to use if not included in the ``host``.
        Default is to not include a port number.

    query : `str`, `dict`
        A query string or `dict` of params to include in the full URL.

    fragment : `str`
        A URL fragment to include in the full URL.

    Returns
    -------
    url : `str`
        A fully-qualified URL.

    Examples
    --------
    >>> make_url('osg-htc.org')
    'https://osg-htc.org'
    >>> make_url('osg-htc.org:443', '/.well-known', 'pelican-configuration')
    'https://osg-htc.org:443/.well-known/pelican-configuration
    """
    # parse url
    parsed = parse_url(url)

    # scheme
    if parsed.scheme is None and scheme is None and parsed.port in HTTP_PORTS:
        scheme = "http"
    elif parsed.scheme is None and scheme is None:
        scheme = "https"
    elif parsed.scheme is not None:
        scheme = parsed.scheme

    # combine paths in a normalised way
    if parsed.path:
        paths = (parsed.path, *paths)
    if paths:
        path = "/".join(x.strip("/") for x in paths)
        if paths[-1].endswith("/"):  # reinstate trailing slash
            path += "/"
    else:
        path = ""

    # encode query params
    params = PreparedRequest._encode_params(
        parsed.query or query,
    )

    # then join it up using requests to format a query
    return str(Url(
        scheme=scheme,
        auth=parsed.auth,
        host=parsed.host,
        port=parsed.port or port,
        path=path,
        query=params,
        fragment=parsed.fragment or fragment,
    ))


def _pooled_request(
    url: str,
    adapter: requests.adapters.BaseAdapter | None = None,
    request: requests.PreparedRequest | None = None,
    session: requests.Session | None = None,
    timeout: float | tuple[float, float] | tuple[float, None] | None = 60,
    method: str = "GET",
    **kwargs,
) -> requests.Response:

    def _inject_default_user_agent(headers: MutableMapping) -> None:
        """Inject our default user agent over the top of the requests default."""
        if headers.get(
            "User-Agent",
            _REQUESTS_USER_AGENT,
        ) == _REQUESTS_USER_AGENT:
            headers["User-Agent"] = default_user_agent()

    # send the request using an adapter
    if adapter and request:
        request = request.copy()
        request.url = url
        _inject_default_user_agent(request.headers)
        return adapter.send(
            request,
            timeout=timeout,
            **kwargs,
        )
    send = (session or requests).request
    _inject_default_user_agent(kwargs.setdefault("headers", {}))
    return send(
        method,
        url,
        timeout=timeout,
        **kwargs,
    )


def parse_mirror_link_header(
    value: str,
    relation: str = "duplicate",
) -> list[dict]:
    """Parse prioritised mirror links from a link header."""
    return sorted(
        (
            link for link in requests.utils.parse_header_links(value)
            if link.get("rel") == relation
        ),
        key=lambda link: ("pref" not in link, int(link.get("pri", 1e5))),
    )


def default_user_agent(
    name: str = "requests-pelican",
) -> str:
    """Return the default User-Agent header content.

    Parameters
    ----------
    name : `str`
        The name for the User-Agent value

    Returns
    -------
    useragent : `str`
        The string to use for the ``User-Agent`` header.
    """
    return f"{name}/{__version__}"
