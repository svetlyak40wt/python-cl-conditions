# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = u'cl-conditions'
year = '2016'
author = u'Alexander Artemenko'
copyright = '{0}, {1}'.format(year, author)


def read_version():
    """Read version from the first line starting with digit
    """
    regex = re.compile('^(?P<number>\d.*?) .*$')

    with open('../CHANGELOG.rst') as f:
        for line in f:
            match = regex.match(line)
            if match:
                return match.group('number')

version = read_version()

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/svetlyak40wt/python-cl-conditions/issues/%s', '#'),
    'pr': ('https://github.com/svetlyak40wt/python-cl-conditions/pull/%s', 'PR #'),
}
import sphinx_py3doc_enhanced_theme
html_theme = "sphinx_py3doc_enhanced_theme"
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]
html_theme_options = {
    'githuburl': 'https://github.com/svetlyak40wt/python-cl-conditions/'
}

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = True
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
