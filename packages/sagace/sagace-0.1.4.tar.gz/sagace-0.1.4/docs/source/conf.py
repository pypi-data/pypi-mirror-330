# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Ajuste conforme necessário para apontar para o diretório do código-fonte

project = 'sagace'
copyright = '2025, Ampere Consultoria'
author = 'Ampere Consultoria'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Importação automática de docstrings
    'sphinx.ext.napoleon',     # Suporte a docstrings no estilo Google e NumPy
    'sphinx.ext.viewcode',     # Adiciona links para visualizar o código-fonte
    'sphinx.ext.autosummary',
    'myst_parser'
]

autodoc_default_options = {
    'members': True,        # Inclui membros de classes e módulos automaticamente
    'undoc-members': True,  # Inclui membros não documentados
    'private-members': True # Inclui membros privados (_nome)
}

templates_path = ['_templates']
exclude_patterns = []

autodoc_mock_imports = ["sagace.samples.basic_autentication"]




# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
