"""A `requests.HTTPAdapter` that understands Pelican URIs."""

from __future__ import annotations

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import logging
import sys
import typing

import requests
import requests.utils
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError
from urllib3.util import parse_url

from .auth import scitoken_auth
from .director import (
    DirectorResponse,
    get_director_response,
)
from .federation import federation_url
from .pelican import pelican_uri

if typing.TYPE_CHECKING:
    from collections.abc import (
        Iterator,
        Mapping,
    )

    import requests_scitokens
    from scitokens import SciToken

log = logging.getLogger(__name__)


class PelicanAdapter(HTTPAdapter):
    """`HTTPAdapter` for Pelican federation URLs.

    This adapter handles accessing and caching the redirect links that
    the Pelican director supplies for each namespace, to transform a
    Pelican federation URI into an HTTP(S) URL.

    Parameters
    ----------
    federation : `str`, optional
        The name or URL of the Pelican federation to use.

    max_retries : `int`, optional
        The number of Pelican caches to try for each request.
        Default is 3.
    """

    def __init__(
        self,
        federation: str | None = None,
        max_retries: int = 3,
        **kwargs,
    ) -> None:
        """Create a new `PelicanAdapter`."""
        super().__init__(
            max_retries=max_retries,
            **kwargs,
        )
        self.federation: str | None = None
        if federation:
            self.federation = federation_url(federation)

    @staticmethod
    def _scitoken_auth(
        request: requests.PreparedRequest,
        director: DirectorResponse,
        token: str | None = None,
    ) -> requests_scitokens.HTTPSciTokenAuth:
        return scitoken_auth(
            request,
            director,
            token=token,
        )

    def _resolve_requests(
        self,
        request: requests.PreparedRequest,
        federation: str | None = None,
        token: SciToken | None = None,
        timeout: float | tuple[float, float] | tuple[float, None] | None = 60,
        **kwargs,
    ) -> Iterator[requests.PreparedRequest]:
        """Query the Pelican federation director for URLs that could serve us."""
        # parse the Pelican federation information
        uri = parse_url(pelican_uri(
            request.url,
            federation=federation or self.federation,
        ))
        # and query the director for information about this namespace
        director = get_director_response(
            str(uri),
            adapter=super(),
            request=request,
            timeout=timeout,
            **kwargs,
        )

        # if request didn't come with its own auth header, and the
        # director tells us we need a token, try and find one now
        if (
            "Authorization" not in request.headers
            and director.namespace["require-token"]
        ):
            auth = self._scitoken_auth(
                request,
                director,
                token=token,
            )
        else:
            auth = None

        # construct a request for each URL we got from the director
        for url in director.urls(str(uri.path)):
            req = request.copy()
            req.url = url
            req.prepare_auth(auth)
            yield req

    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: float | tuple[float, float] | tuple[float, None] | None = 60,
        verify: bool | str = True,
        cert: str | bytes | tuple[str | bytes, str | bytes] | None = None,
        proxies: Mapping[str, str] | None = None,
        federation: str | None = None,
    ) -> requests.Response:
        """Send a request using this adapter.

        This will loop over the Pelican cache URLs in an attempt to download
        the requested URI.
        """
        if timeout is None:
            timeout = 60
        retries = self.max_retries
        responses = []
        error = None
        reqs = list(self._resolve_requests(
            request,
            federation=federation,
            timeout=timeout,
            verify=True,
            cert=cert,
            proxies=proxies,
        ))
        log.debug(
            "Identified %s endpoints for %s, will attempt at most %s",
            len(reqs),
            request.url,
            retries.total,
        )
        for req in reqs:
            log.debug("Sending %s request to %s", req.method, req.url)
            try:
                resp = super().send(
                    req,
                    stream=stream,
                    timeout=timeout,
                    verify=verify,
                    cert=cert,
                    proxies=proxies,
                )
            except requests.ConnectionError as exc:
                if error is None:
                    error = exc
                retries = retries.increment(
                    request.method,
                    request.url,
                    error=exc,
                    _stacktrace=sys.exc_info()[2],
                )
                log.debug(
                    "Connection error from %s, moving to next target",
                    request.url,
                )
                continue
            log.debug("%s response received from %s", resp.status_code, resp.url)
            responses.append(resp)
            if resp.status_code >= requests.codes.BAD_REQUEST:  # 400
                try:
                    retries = retries.increment(
                        method=request.method,
                        url=request.url,
                        response=resp.raw,
                    )
                except MaxRetryError:
                    break
                continue
            break

        # if we got out response
        if responses:
            # attach history of our attempts
            r = responses.pop(-1)
            r.history = responses + r.history
            return r

        # if we identified an error, use that
        if error:
            raise error
        # otherwise panic
        msg = "no responses received, but no error identified"
        raise RuntimeError(msg)
