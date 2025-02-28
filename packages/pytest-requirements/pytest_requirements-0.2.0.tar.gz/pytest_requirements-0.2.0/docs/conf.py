import pytest_requirements

project = "pytest_requirements"
copyright = "CTAO"
author = "CTAO Computing Department"
version = pytest_requirements.__version__
# The full version, including alpha/beta/rc tags.
release = version


extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx_changelog",
]

exclude_patterns = ["changes"]
default_role = "py:obj"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pytest": ("https://docs.pytest.org/en/stable/", None),
}

html_theme = "ctao"
html_theme_options = dict(
    navigation_with_keys=False,
    switcher=dict(
        json_url="http://cta-computing.gitlab-pages.cta-observatory.org/common/pytest-requirements/versions.json",  # noqa: E501
        version_match="latest" if ".dev" in version else f"v{version}",
    ),
    navbar_center=["version-switcher", "navbar-nav"],
)

html_static_path = []
