import os
import pathlib
import subprocess
import sys
from datetime import date

from sphinx.highlighting import lexers

sys.path.insert(0, os.path.abspath("."))

from gravy_lexer import GravwellLexer

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Gravwell"
copyright = f"Gravwell, Inc. {date.today().year}"
author = "Gravwell, Inc."
release = "v5.6.7"

# Default to localhost:8000, so the version switcher looks OK on livehtml
version_list_url = os.environ.get(
    "VERSION_LIST_URL", "http://localhost:8000/_static/versions.json"
)
print("Using version_list_url:", version_list_url)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_design",
    "notfound.extension",
    "sphinx_copybutton",
    "sphinx_favicon",
]

myst_enable_extensions = [
    "colon_fence",
    "fieldlist",
    "substitution",
]


templates_path = ["_templates"]
exclude_patterns = [
    ".github",
    "README.md",
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "env",
    "_vendor",
    "_tools",
]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_show_sourcelink = False
html_copy_source = False

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_theme_options = {
    "logo": {
        "image_light": "_static/images/Gravwell-Color.svg",
        "image_dark": "_static/images/Gravwell-Color-Reverse.svg",
    },
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/gravwell",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-brands fa-github",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
        {
            # Label for this link
            "name": "Discord",
            # URL where the link will redirect
            "url": "https://discord.com/invite/gravwell",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-brands fa-discord",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
    ],
    "header_links_before_dropdown": 6,
    "footer_start": [
        "sphinx-version",
        "theme-version",
    ],
    "footer_end": [
        "copyright",
        "git-commit-footer",
    ],
    "navigation_with_keys": False,
    #
    # Version switcher
    #
    "switcher": {
        "json_url": version_list_url,
        # The `version` field of each entry in verions.json must match a vN.N.N release name
        "version_match": release,
    },
    # Show a warning banner if the user's looking at any page other than latest
    "show_version_warning_banner": True,
    # Don't fail to compile just because the version switcher file (json_url) isn't reachable
    "check_switcher": False,
    # include the version switcher next to the logo
    "navbar_start": ["navbar-logo", "version-switcher"],
    # use custom center for navbar, so that we can better manage responsiveness
    "navbar_center": ["dynamic-navbar"],
}

# sphinx-favicon
favicons = [
    {
        "rel": "icon",
        "sizes": "48x48",
        "href": "favicon.ico",
    },
]

# -- Gravwell Query Language Config ----------------------------

lexers["gw"] = lexers["gravwell"] = GravwellLexer(startinline=True)


# -- "Not Found" Extension Config ----------------------------

notfound_urls_prefix = ""


# -- Substitutions -------------------------------------------------

# Determine git commit ID
#
# Make sure we're checking the commit id for the wiki project, by passing the directory
# to the git subprocess call
git_dir = pathlib.Path(__file__).parent.resolve()
commit_id = (
    subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=git_dir)
    .strip()
    .decode("ascii")
)
try:
    subprocess.check_call(["git", "diff", "--quiet"], cwd=git_dir)
    is_dirty_tree = False
except subprocess.CalledProcessError:
    is_dirty_tree = True

# Variables to substitute in HTML template files
html_context = {
    "git_commit": commit_id,
    "git_dirty_tree": is_dirty_tree,
}

# Variables to substitute in Markdown files
myst_substitutions = {}

# Copy button
copybutton_selector = "div.highlight pre,div.docutils pre.literal-block"
