"""Python Requests wrappers for `requests_pelican`."""

from __future__ import annotations

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import typing
from functools import wraps as _wraps

import requests
import requests.api

from . import sessions

if typing.TYPE_CHECKING:
    from collections.abc import Callable


@_wraps(requests.request)
def request(
    method: str,
    url: str,
    *,
    session: requests.Session | None = None,
    **kwargs,
) -> requests.Response:
    """Send a Pelican request.

    Parameters
    ----------
    method : `str`
        The method to use.

    url : `str`,
        The URL to request.

    session : `requests.Session`, optional
        The connection session to use, if not given one will be
        created on-the-fly.

    kwargs
        All other keyword arguments are passed directly to
        `requests.Session.request`.

    Returns
    -------
    resp : `requests.Response`
        the response object

    See Also
    --------
    igwn_auth_utils.requests.Session.request
        for information on how the request is performed
    """
    # user's session
    if session:
        return sessions.Session.request(
            session,
            method,
            url,
            **kwargs,
        )

    # new session
    with sessions.Session() as sess:
        return sess.request(method, url, **kwargs)


def _request_wrapper_factory(method: str) -> Callable:
    """Wrap a `requests` HTTP method to use our request function."""
    func = getattr(requests.api, method)

    @_wraps(func)
    def _request_wrapper(*args, **kwargs):
        return request(method, *args, **kwargs)

    _request_wrapper.__doc__ = func.__doc__ + f"""
    See also
    --------
    `requests.{method}`
        The upstream function of which this is a wrapper.
    """

    return _request_wrapper


# request methods
delete = _request_wrapper_factory("delete")
get = _request_wrapper_factory("get")
head = _request_wrapper_factory("head")
patch = _request_wrapper_factory("patch")
post = _request_wrapper_factory("post")
put = _request_wrapper_factory("put")
