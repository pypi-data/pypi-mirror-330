requests-pelican
################

.. toctree::
   :hidden:

   requests_pelican <self>

`requests-pelican` provides a
`Requests <http://requests.readthedocs.io/>`__ plugin
to support HTTP requests to a
`Pelican Federation <https://pelicanplatform.org/>`__.

The main component is a new :class:`~requests_pelican.PelicanAdapter`
class that handles translating Pelican URIs into HTTP URLs to enable standard
``GET`` requests, including looping over Pelican caches.

This project also provides wrappers around `requests.get` (and friends) and
`requests.Session` to simplify configuring support for Pelican URIs.

.. image:: https://badge.fury.io/py/requests-pelican.svg
    :target: http://badge.fury.io/py/requests-pelican
    :alt: requests-pelican PyPI version badge
.. image:: https://img.shields.io/conda/vn/conda-forge/requests-pelican.svg
    :target: https://anaconda.org/conda-forge/requests-pelican/
    :alt: requests-pelican conda-forge badge


.. raw:: html

    <br/>

.. image:: https://img.shields.io/pypi/l/requests-pelican.svg
    :target: https://choosealicense.com/licenses/apache-2.0/
    :alt: requests-pelican license badge
.. image:: https://img.shields.io/pypi/pyversions/requests-pelican.svg
    :alt: Supported Python versions badge

.. raw:: html

    <br/>

.. image:: https://git.ligo.org/computing/software/requests-pelican/badges/main/pipeline.svg
    :alt: Build status
    :target: https://git.ligo.org/computing/software/requests-pelican/-/pipelines
.. image:: https://git.ligo.org/computing/software/requests-pelican/badges/main/coverage.svg
    :alt: Code coverage
.. image:: https://readthedocs.org/projects/requests-pelican/badge/?version=latest
    :alt: Documentation Status
    :target: https://requests-pelican.readthedocs.io/en/latest/?badge=latest

Installation
============

Conda
-----

.. code-block:: bash

    conda install -c conda-forge requests-pelican

Pip
---

.. code-block:: bash

    python -m pip install requests-pelican

To include support for [SciTokens](https://scitokens.org/)
include the `[scitokens]` extra:

.. code-block:: bash

    python -m pip install requests-pelican[scitokens]


``requests-pelican`` documentation
==================================

.. automodule:: requests_pelican

Functions
---------

.. automodsumm:: requests_pelican
    :functions-only:
    :toctree: .
    :caption: Functions
    :allowed-package-names: requests

Classes
-------

.. automodsumm:: requests_pelican
    :classes-only:
    :toctree: .
    :caption: Classes
    :allowed-package-names: requests

Modules
-------

.. toctree::
    :caption: Modules
    :hidden:

    requests_pelican.config
    requests_pelican.director
    requests_pelican.federation
    requests_pelican.utils

.. currentmodule:: None
.. autosummary::

    requests_pelican.config
    requests_pelican.director
    requests_pelican.federation
    requests_pelican.utils
