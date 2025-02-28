"""Authorisation utilities for requests_pelican."""

from __future__ import annotations

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import logging
import typing

if typing.TYPE_CHECKING:
    import requests
    import requests_scitokens
    import scitokens

    from .director import DirectorResponse

log = logging.getLogger(__name__)


def scitoken_auth(
    request: requests.PreparedRequest,
    namespace: DirectorResponse,
    token: scitokens.SciToken | str | None = None,
) -> requests_scitokens.HTTPSciTokenAuth | None:
    """Configure a `~requests_scitokens.HTTPSciTokenAuth` handler.

    Parameters
    ----------
    request : `requests.PreparedRequest`
        The request to handle.

    namespace : `requests_pelican.DirectorReponse`
        The namespace information to use.

    token : `scitokens.SciToken`, `str`, optional
        The token to use for authorisation.

    Returns
    -------
    auth : `requests_scitokens.HTTPSciTokenAuth`, or `None`.
        A new auth handler for this request, or `None` if
        `requests_scitokens` could not be imported.
    """
    log.debug(
        "Configuring HTTPSciTokenAuth for namespace '%s'",
        namespace.namespace,
    )
    try:
        from requests_scitokens import HTTPSciTokenAuth
    except ImportError as exc:
        log.debug(
            "Failed to import HTTPSciTokenAuth (%s)",
            str(exc),
        )
        return None

    auth = HTTPSciTokenAuth(token=token)
    if token is None:
        auth.token = auth.find_token(
            request.url,
            error=False,
        )
    if auth.token is None:
        log.debug(
            "Failed to find SciToken for namespace '%s'",
            namespace.namespace,
        )
    return auth
