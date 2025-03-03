"""
Common definitions for the Sphinx documentation builder. Define all
project specific settings in the actual project specific conf.py files

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
import os
import sphinx_bootstrap_theme

master_doc = "index"

html_static_path: list[str] = ["_static"]


extensions = [
    "sphinx.ext.napoleon",  # For support of Google and NumPy style docstrings
    "sphinx_autodoc_typehints",
    "sphinx.ext.autodoc",  # For automatic generation of API documentation from docstrings
    "sphinx.ext.intersphinx",  # For cross-referencing to external documentation
    "sphinx.ext.todo",  # For TODO list management
    "sphinx.ext.viewcode",  # For links to the source code
    "sphinx.ext.autosummary",  # For automatic generation of summary tables of contents
    "sphinx.ext.doctest",  # For running doctests in docstrings
    "sphinx.ext.ifconfig",  # For conditional content based on configuration values
    "sphinx.ext.githubpages",  # For publishing documentation to GitHub Pages
    "sphinx.ext.coverage",  # For measuring documentation coverage
    "sphinx.ext.mathjax",  # For rendering math via MathJax
    "sphinx.ext.imgmath",  # For rendering math via LaTeX and dvipng
    "sphinx.ext.inheritance_diagram",  # UML diagrams,
    "sphinxcontrib.mermaid",  # for UML diagrams
]

graphviz_output_format: str = "svg"  # for UML diagrams
napoleon_google_docstring: bool = True
napoleon_numpy_docstring: bool = False
autodoc_inherit_docstrings: bool = False
templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []
todo_include_todos: bool = True
pygments_style: str = "sphinx"  # Default syntax highlighting style
highlight_language: str = "python"  # Default language for code blocks


html_theme: str = "bootstrap"
html_theme_path: list[str] = sphinx_bootstrap_theme.get_html_theme_path()

html_css_files = [
    "masterpiece.css",
]

