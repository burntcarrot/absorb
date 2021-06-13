"""Sphinx configuration."""
project = "absorb"
author = "Aadhav Vignesh"
copyright = f"2021, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click.ext",
    "faculty_sphinx_theme",
]
html_theme = "faculty-sphinx-theme"
html_logo = "logo.png"
html_favicon = "logo.png"
