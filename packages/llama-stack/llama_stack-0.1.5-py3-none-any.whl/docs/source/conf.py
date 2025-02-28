# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from docutils import nodes
import tomli  # Import tomli for TOML parsing
from pathlib import Path

# Read version from pyproject.toml
with Path(__file__).parent.parent.parent.joinpath("pyproject.toml").open("rb") as f:
    pyproject = tomli.load(f)
    llama_stack_version = pyproject["project"]["version"]

project = "llama-stack"
copyright = "2025, Meta"
author = "Meta"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_design",
    "sphinxcontrib.redoc",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.video",
]
myst_enable_extensions = ["colon_fence"]

html_theme = "sphinx_rtd_theme"
html_use_relative_paths = True

# html_theme = "sphinx_pdj_theme"
# html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]

# html_theme = "pytorch_sphinx_theme"
# html_theme_path = [pytorch_sphinx_theme.get_html_theme_path()]


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_substitutions = {
    "docker_hub": "https://hub.docker.com/repository/docker/llamastack",
    "llama_stack_version": llama_stack_version,
}

suppress_warnings = ['myst.header']

# Copy button settings
copybutton_prompt_text = "$ "  # for bash prompts
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
copybutton_line_continuation_character = "\\"

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme_options = {
    "canonical_url": "https://github.com/meta-llama/llama-stack",
    # "style_nav_header_background": "#c3c9d4",
}

html_static_path = ["../_static"]
# html_logo = "../_static/llama-stack-logo.png"
# html_style = "../_static/css/my_theme.css"

def setup(app):
    app.add_css_file("css/my_theme.css")
    def dockerhub_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        url = f"https://hub.docker.com/r/llamastack/{text}"
        node = nodes.reference(rawtext, text, refuri=url, **options)
        return [node], []

    def repopath_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        parts = text.split("::")
        if len(parts) == 2:
            link_text = parts[0]
            url_path = parts[1]
        else:
            link_text = text
            url_path = text

        url = f"https://github.com/meta-llama/llama-stack/tree/main/{url_path}"
        node = nodes.reference(rawtext, link_text, refuri=url, **options)
        return [node], []

    app.add_role("dockerhub", dockerhub_role)
    app.add_role("repopath", repopath_role)
