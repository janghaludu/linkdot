#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
MARKUP = ('md', 'ipynb')

AUTHOR = u'Sriharsha Bangaru'
SITENAME = u'Dotlink'
SITEURL = 'http://linkdot.link'
SITETITLE = AUTHOR
SITESUBTITLE = 'Mathematics | Programming | Art'
THEME = 'themes/Flex'
PYGMENTS_STYLE = 'monokai'

COVER_IMG_URL = ''
PROFILE_IMG_URL = 'https://media.giphy.com/media/LMEKcLACS5xDi/giphy.gif' 
TAGLINE = 'Mathematics | Programming | Art'
DISQUS_SITENAME = 'linkdot'
PATH = 'content'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

STATIC_PATHS = ["images",'extra/favicon.ico']
EXTRA_PATH_METADATA = {'extra/favicon.ico': {'path': 'favicon.ico'}}

MENUITEMS = [('Blog', 'index.html'),
        ('Archive', 'archives.html'),
        ('Tags', 'tags.html'),
        ('Projects', 'pages/projects.html'),
        ('Resources', 'pages/talks.html'),
        ('About', 'pages/about-me.html')]

SECTIONS = [('Blog', 'index.html'),
        ('Archive', 'archives.html'),
        ('Tags', 'tags.html'),
        ('Primers', 'pages/projects.html'),
        ('Projects', 'pages/talks.html'),
        ('About', 'pages/about-me.html')]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('About','#'),
         ('Categories', '#'),
         ('Primers', '#'),
         ('Projects', '#'),)

# Social widget
SOCIAL = (
    ('lastfm', 'https://github.com/djanghaludu'),
    ('github-alt', 'https://github.com/djanghaludu'),
    ('twitter', 'https://twitter.com/pfatagaga'),
    ('instagram', 'https://instagram.com/pfatagaga'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
PLUGIN_PATHS = ['plugins','./plugins']
#PLUGIN_PATH = './plugins'
PLUGINS = ["pelican_plugin-render_math", 'ipynb.markup']
MATH_JAX = {'color': 'brown'}
GOOGLE_ANALYTICS = 'UA-78881164-1'



