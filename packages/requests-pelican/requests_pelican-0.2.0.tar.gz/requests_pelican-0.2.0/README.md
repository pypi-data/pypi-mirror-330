# Python-requests interface for Pelican Platform

This project provides [`requests`](https://github.com/psf/requests) addons
to support HTTP requests to a [Pelican Federation](https://pelicanplatform.org/).

The main component is a new `PelicanAdapter` class that handles translating
Pelican URIs into HTTP URLs to enable standard `GET` requests, including
looping over Pelican caches.

This project also provides wrappers around `requests.get` (and friends) and
`requests.Session` to simplify configuring support for Pelican URIs.

## Install

To install this project, use `pip`:

```shell
pip install requests-pelican
```

To include support for [SciTokens](https://scitokens.org/)
include the `[scitokens]` extra:

```shell
pip install requests-pelican[scitokens]
```

## Examples

### 1. Public data

```python
import requests_pelican
print(requests_pelican.get("osdf:///gwdata/zenodo/README.zenodo").text)
```

### 2. Private data requiring token authorisation

Requests for data from a Private Pelican federation require a Bearer token.
`requests-pelican` will attempt to automatically discover a valid
[SciToken](https://scitokens.org/) before `GET`ting the data.

```python
import requests_pelican
print(requests_pelican.get("osdf:///igwn/ligo/README").text)
```

### 3. Integrating with other requests plugins

The `requests_pelican.PelicanAdapter` object can be integrated with the
standard `requests.Session` to simplify combining Pelican support with other
plugins, for example:

```python
from requests_pelican import PelicanAdapter
from igwn_auth_utils import Session
with Session() as sess:
    sess.mount("osdf://", PelicanAdapter("osdf"))
    resp = sess.get("osdf:///igwn/ligo/README", token_scope="read:/ligo")
    ...
```
