"""Session wrappers for Pelican."""

from __future__ import annotations

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from requests import (
    Session as _Session,
)

from .adapters import PelicanAdapter
from .federation import KNOWN_FEDERATIONS
from .utils import default_user_agent


class SessionMixin:
    """`requests.Session` mixin to mount adapters for Pelican URIs."""

    def __init__(
        self: _Session,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.headers["User-Agent"] = default_user_agent()
        self.mount("pelican://", PelicanAdapter())
        for fed in KNOWN_FEDERATIONS:  # mount them all
            self.mount(f"{fed}://", PelicanAdapter(fed))


class Session(SessionMixin, _Session):
    """`requests.Session` that understands Pelican URIs."""
