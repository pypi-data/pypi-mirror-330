"""End-to-end integration tests for `requests_pelican`."""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import pytest
import requests

import requests_pelican

# ET MDC data (it's public and it works)
OSDF_TEST_URL = "osdf:///et-gw/PUBLIC/MDC1/params/ET/params_1.txt"
OSDF_TEST_CONTENT = b"11 999998266.071"


def _skip_exception(exc):
    return pytest.skip(f"caught {type(exc).__name__}: {exc}")


@pytest.mark.remote_data
def test_osdf_et_mdc():
    """Test a real round-trip with `requests_pelican.Session`.

    This test talks to the internet, so has some default protections to
    redirect to `pytest.skip` on transient errors.
    """
    # get the data
    with requests_pelican.Session() as sess:
        # requests_session.Session auto-mounts the osdf:// adapter
        try:
            resp = sess.get(OSDF_TEST_URL)
            resp.raise_for_status()
        except (  # pragma: no cover
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            _skip_exception(exc)
        except requests.exceptions.HTTPError as exc:  # pragma: no cover
            if exc.response.status_code >= 500:
                _skip_exception(exc)
            raise

    # assert that we got the real thing
    data = next(resp.iter_content(chunk_size=16, decode_unicode=False))
    assert data == OSDF_TEST_CONTENT


@pytest.mark.remote_data
def test_osdf_notfound():
    """Test a real round-trip with `requests_pelican.Session` that doesn't work.

    This should execute the retry loop for multiple caches and eventually return a 404.
    """
    # get the data
    with requests_pelican.Session() as sess:
        # requests_session.Session auto-mounts the osdf:// adapter
        try:
            resp = sess.get(OSDF_TEST_URL + "BAD")
        except (  # pragma: no cover
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            _skip_exception(exc)

        # if we got a 500 error (or above), something went wrong
        if resp.status_code >= requests.codes.INTERNAL_SERVER_ERROR:  # pragma: no cover
            try:
                resp.raise_for_status()
            except requests.exceptions.HTTPError as exc:
                _skip_exception(exc)

        # check that we got a 404
        assert resp.status_code == requests.codes.NOT_FOUND
        # and that multiple caches were tried
        assert len(resp.history) >= 3
