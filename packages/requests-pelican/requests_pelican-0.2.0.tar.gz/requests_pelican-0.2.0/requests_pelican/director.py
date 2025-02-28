"""Pelican federation director interactions."""

from __future__ import annotations

import logging
import typing
from dataclasses import (
    dataclass,
    field,
)
from random import shuffle
from threading import RLock

from requests.utils import (
    parse_dict_header,
    parse_list_header,
)
from urllib3.util import (
    Url,
    parse_url,
)

from .config import get_pelican_configuration
from .pelican import pelican_uri
from .utils import (
    _pooled_request,
    make_url,
    parse_mirror_link_header,
)

if typing.TYPE_CHECKING:
    from typing import Any
    try:
        from typing import Self
    except ImportError:  # python < 3.11
        from typing_extensions import Self

    import requests

log = logging.getLogger(__name__)

DIRECTOR_CACHE: list[DirectorResponse] = []
DIRECTOR_CACHE_LOCK = RLock()


@dataclass
class DirectorResponse:
    """Information for a Pelican namespace.

    As returned by the director endpoint for a path in the namespace.
    """

    federation: str
    namespace: dict[str, Any]
    auth: list[dict[str, Any]] = field(default_factory=list)
    token_generation: list[dict[str, Any]] = field(default_factory=list)
    links: list[str] = field(default_factory=list)

    @staticmethod
    def _parse_info_header(value: str) -> list[dict[str, str]]:
        return list(map(parse_dict_header, parse_list_header(value)))

    @staticmethod
    def _parse_link_header_urls(value: str) -> list[str]:
        links = parse_mirror_link_header(value)
        return [
            str(Url(scheme=u.scheme, host=u.host, port=u.port))
            for u in (parse_url(link["url"]) for link in links)
        ]

    @classmethod
    def from_response(
        cls,
        federation: str,
        response: requests.Response,
    ) -> Self:
        """Build a new `DirectorResponse` from a `requests.Response`.

        Parameters
        ----------
        federation : `str`
            The URL of the Pelican federation.

        response : `requests.Response`
            The HTTP response to parse.

        Returns
        -------
        dirresp : `DirectorResponse`
            The formatter response from the Pelican director.
        """
        headers = response.headers

        # parse namespace information
        namespace = parse_dict_header(headers.get("x-pelican-namespace", ""))
        # make bool string actually a bool
        namespace["require-token"] = namespace.get(
            "require-token",
            "",
        ).lower() == "true"

        # parse authorisation info
        auth = cls._parse_info_header(headers.get("x-pelican-authorization", ""))

        # parse token generation info
        token_gen = cls._parse_info_header(
            headers.get("x-pelican-token-generation", ""),
        )

        # parse links
        links = cls._parse_link_header_urls(headers.get("link", ""))

        return cls(
            auth=auth,
            federation=federation,
            namespace=namespace,
            links=links,
            token_generation=token_gen,
        )

    def urls(
        self,
        path: str,
        *,
        random: bool = False,
    ) -> list[str]:
        """Return the list of fully-qualified URLs that serve the given path.

        Parameters
        ----------
        path : `str`
            The Pelican data path, must be a sub-path of the right namespace
            for this `DirectorResponse`.

        random : `bool`
            If `True`, shuffle the list of URLs before returning.

        Returns
        -------
        urls : `list` of `str`
            The list of fully-qualified HTTP URLs that should serve the
            given path.
        """
        urls = [
            f"{link}{path}" for link in self.links
        ]
        if random:
            shuffle(urls)
        return urls


def get_director_endpoint(
    federation: str,
    **kwargs,
) -> str:
    """Get the director endpoint URL for a Pelican federation."""
    return get_pelican_configuration(
        federation,
        **kwargs,
    )["director_endpoint"]


def get_director_response(
    path: str,
    federation: str | None = None,
    *,
    cache: bool | str = True,
    timeout: float | tuple[float, float] | tuple[float, None] | None = 60,
    **kwargs,
) -> DirectorResponse:
    """Query for director information for a Pelican path.

    Parameters
    ----------
    path : `str`
        The Pelican data path, must be a sub-path of the right namespace
        for this `DirectorResponse`.

    federation : `str`
        The name or URL of the Pelican Federation that contains the path.
        This is required if ``path`` isn't a valid Pelican URI from which
        the federation URL can be parsed.

    cache : `bool`, `str`
        Whether to use a cached copy of the `DirectorResponse` for the
        federation (`True` or `False`).
        If ``cache="update"`` is given, query the director again and
        update the cache with the new response.

    timeout : `int`, optional
        The timeout (seconds) after which to abort requests to the
        Pelican director.

    random : `bool`
        If `True`, shuffle the list of URLs before returning.

    kwargs
        Other keyword arguments are passed to `get_director_response`.

    Returns
    -------
    dirresp : `DirectorResponse`
        The response from the Pelican director.
    """
    # parse the federation URL and path for this path
    uri = parse_url(pelican_uri(path, federation=federation))
    federation = str(uri.host)
    path = str(uri.path)

    # get namespace info from cache
    director = None
    if cache is True:
        for dresp in DIRECTOR_CACHE:
            if path.startswith(dresp.namespace["namespace"]):
                director = dresp
                break

    # namespace not in cache
    if director is None:
        log.debug("querying federation for director endpoint")
        endpoint = get_director_endpoint(
            federation,
            timeout=timeout,
        )
        log.debug("querying director for cache URLs for %s", path)
        director_url = make_url(endpoint, path)

        # make a request to the director and parse the `link` header response
        if "adapter" not in kwargs:  # adapters don't redirect
            kwargs["allow_redirects"] = False
        resp = _pooled_request(
            director_url,
            method="HEAD",
            timeout=timeout,
            **kwargs,
        )
        resp.raise_for_status()
        director = DirectorResponse.from_response(
            federation,
            resp,
        )

    # update cache
    if cache:
        with DIRECTOR_CACHE_LOCK:
            DIRECTOR_CACHE.append(director)

    return director


def get_urls(
    path: str,
    federation: str | None = None,
    *,
    cache: bool | str = True,
    timeout: float | tuple[float, float] | tuple[float, None] | None = 60,
    random: bool = False,
    **kwargs,
) -> list[str]:
    """Return the list of fully-qualified URLs that serve the given path.

    Parameters
    ----------
    path : `str`
        The Pelican data path, must be a sub-path of the right namespace
        for this `DirectorResponse`.

    federation : `str`
        The name or URL of the Pelican Federation that contains the path.
        This is required if ``path`` isn't a valid Pelican URI from which
        the federation URL can be parsed.

    cache : `bool`, `str`
        Whether to use a cached copy of the `DirectorResponse` for the
        federation (`True` or `False`).
        If ``cache="update"`` is given, query the director again and
        update the cache with the new response.

    timeout : `int`, optional
        The timeout (seconds) after which to abort requests to the
        Pelican director.

    random : `bool`
        If `True`, shuffle the list of URLs before returning.

    kwargs
        Other keyword arguments are passed to `get_director_response`.

    Returns
    -------
    urls : `list` of `str`
        The list of fully-qualified HTTP URLs that should serve the
        given path.

    See Also
    --------
    DirectorResponse.urls
        For details of the URL formatting.
    """
    uri = parse_url(pelican_uri(path, federation=federation))
    director = get_director_response(
        str(uri),
        cache=cache,
        timeout=timeout,
        **kwargs,
    )
    return director.urls(str(uri.path), random=random)
