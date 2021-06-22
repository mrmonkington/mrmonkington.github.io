#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Mark'
SITENAME = "Mark's notes"
SITEURL = ''
THEME = 'theme/'

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en_gb'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Github', 'https://github.com/mrmonkington'),
)
MENUITEMS = (
    ('Github', 'https://github.com/mrmonkington'),
)
# Social widget
SOCIAL = (
    ('@mrmonkington', 'twitter.com/mrmonkington'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

READTIME_WPM = 180

STATIC_PATHS = [
    'images',
    'extra/favicon.ico',
]
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

