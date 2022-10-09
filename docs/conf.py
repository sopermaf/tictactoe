"""Sphinx configuration."""
project = "Tictactoe   Maxmin"
author = "Ferdia Soper Mac Cafraidh"
copyright = "2022, Ferdia Soper Mac Cafraidh"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
