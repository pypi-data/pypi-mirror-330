# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project
# -information

import os
import sys
import tomllib

# Location of Sphinx files
sys.path.insert(0, os.path.abspath('./../..'))

# Pull data from pyproject.toml
pyproject_data = tomllib.load(open('../../pyproject.toml', 'rb'))

project = pyproject_data['project']['name']
# project = 'saoovqe'
copyright = '2023, Martin Beseda, Silvie Illésová, Saad Yalouz, Bruno Senjean'
author = 'Martin Beseda, Silvie Illésová, Saad Yalouz, Bruno Senjean'
release = pyproject_data['project']['version']
# release = '1.1.1'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general
# -configuration

extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser',
    'nbsphinx',
    'nbsphinx_link',
    'sphinx.ext.autodoc'
]

autodoc_mock_imports = ['qiskit_nature', 'qiskit', 'qiskit_algorithms', 'qiskit_ibm_runtime', 'sympy', 'psi4', 'scipy',
                        'mendeleev', 'deprecated', 'enum', 'typing']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for
# -html-output

html_theme = 'classic'
# html_static_path = ['_static']
