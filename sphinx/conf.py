import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'PySync'
copyright = '2024, Colin Conwell'
author = 'Colin Conwell'
json_url = '_static/switcher.json'

# The full version, including alpha/beta/rc tags
release = '0.1.0'
version = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx_copybutton',
    'sphinx.ext.githubpages',
]

# Add any paths that contain templates here, relative to this directory
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The theme to use for HTML Help pages
html_theme = 'pydata_sphinx_theme'
# pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html
# another theme example: https://abess.readthedocs.io/en/latest/

# HTML theme options
html_theme_options = {
    #"github_url": "https://github.com/colinconwell/PySync",
    "navbar_align": "left",
    "show_nav_level": 2,
    "show_toc_level": 2,
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    #"navbar_center": ["version-switcher", "navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
   # "secondary_sidebar_items": ["page-toc", "sourcelink"],
    "secondary_sidebar_items": [],
    "switcher": {
        "json_url": json_url,
        "version_match": version,
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/colinconwell/PySync",
            "icon": "fab fa-github-square",
            "type": "fontawesome",
        }
    ],
    "logo": {
        "text": "PySync",
        "image_light": "_static/logo-light.png",
        "image_dark": "_static/logo-dark.png",
    },
    "navigation_with_keys": False,
    "use_edit_page_button": True,
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "header_links_before_dropdown": 4,
}

html_context = {
    "default_mode": "light",
    "display_github": True,
    "github_user": "colinconwell",
    "github_repo": "PySync",
    "github_version": "main",
    "doc_path": "sphinx",
}

html_sidebars = {
    #"**": ["sidebar-nav-bs"]
    "**": ["page-toc"]
}

_sidebar_item_options = ['page-toc', 'sourcelink', 'search-field', 'sidebar-nav-bs']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'custom.css',
]

html_static_path = ['_static']
html_title = "PySync"

# AutoDoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Intersphinx configuration
intersphinx_mapping = {
    "numpy": ("https://numpy.org/doc/stable/", None),
    'python': ('https://docs.python.org/{.major}'.format(sys.version_info), None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    "sklearn": ("https://scikit-learn.org/dev/", None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None)
}