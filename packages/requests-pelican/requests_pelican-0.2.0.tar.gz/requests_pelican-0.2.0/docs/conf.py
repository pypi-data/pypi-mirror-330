"""Configuration file for Sphinx documentation
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import inspect
import re
import sys
from os import getenv
from pathlib import Path

import requests_pelican

# -- Project information -----------------------------------------------------

project = "requests-pelican"
copyright = "2024, Cardiff University"
author = "Duncan Macleod"
release = requests_pelican.__version__
version = release.split("+", 1)[0]

# -- Sources -----------------------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = [
    "_templates",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
]

# -- Formatting --------------------------------------------------------------

default_role = "obj"

# -- HTML options ------------------------------------------------------------

html_theme = "furo"
html_title = f"{project} {version}"

# code highlighting
pygments_style = "monokai"
pygments_dark_style = "monokai"

# -- Extensions --------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx_automodapi.automodapi",
]

# -- autodoc

autodoc_default_flags = [
    "members",
    "show-inheritance",
]
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# -- automodapi

automodapi_inherited_members = False
automodapi_toctreedirnm = "."

# -- autosummary

autosummary_generate = True

# -- intersphinx

intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        None,
    ),
    "requests": (
        "https://requests.readthedocs.io/en/stable/",
        None,
    ),
    "requests-scitokens": (
        "https://requests-scitokens.readthedocs.io/en/stable/",
        None,
    ),
    "scitokens": (
        "https://scitokens.readthedocs.io/en/stable/",
        None,
    ),
}

# -- linkcode


def _project_git_ref(version):
    """Returns the git reference for the given full release version.
    """
    _setuptools_scm_version_regex = re.compile(
        r"\+g(\w+)(?:\Z|\.)",
    )
    if match := _setuptools_scm_version_regex.search(version):
        return match.groups()[0]
    return f"v{version}"


PROJECT_GIT_REF = _project_git_ref(release)
PROJECT_PATH = Path(requests_pelican.__file__).parent
PROJECT_URL = getenv(
    "CI_PROJECT_URL",
    "https://git.ligo.org/computing/software/requests-pelican",
)
PROJECT_BLOB_URL = f"{PROJECT_URL}/blob/{PROJECT_GIT_REF}/{PROJECT_PATH.name}"


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object.
    """
    if domain != "py" or not info["module"]:
        return None

    def find_source(module, fullname):
        """Construct a source file reference for an object reference.
        """
        # resolve object
        obj = sys.modules[module]
        for part in fullname.split("."):
            obj = getattr(obj, part)
        # get filename relative to project
        filename = Path(
            inspect.getsourcefile(obj),  # type: ignore [arg-type]
        ).relative_to(PROJECT_PATH).as_posix()
        # get line numbers of this object
        lines, lineno = inspect.findsource(obj)
        if lineno:
            start = lineno + 1  # 0-index
            end = lineno + len(inspect.getblock(lines[lineno:]))
        else:
            start = end = 0
        return filename, start, end

    try:
        path, start, end = find_source(info["module"], info["fullname"])
    except (
        AttributeError,  # object not found
        OSError,  # file not found
        TypeError,  # source for object not found
        ValueError,  # file not from this project
    ):
        return None

    url = f"{PROJECT_BLOB_URL}/{path}"
    if start:
        url += f"#L{start}-L{end}"
    return url
