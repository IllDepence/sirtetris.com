#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()

import sys
import codecs

HOME_DIR = '/homez.151/sirtetri/'
SEPARATOR = u'- - -\n'
MD_EXT = ['markdown.extensions.tables', 'markdown.extensions.nl2br']

# mardown v2.5 dropped support for python 2.6, OVH uses python 2.6.6
# also, including modules w/o installing because hosting contract only
sys.path.append(HOME_DIR + 'moc/pywebsite/modules/Markdown-2.4')
sys.path.append(HOME_DIR + 'moc/pywebsite/modules/MarkupSafe-0.23')
sys.path.append(HOME_DIR + 'moc/pywebsite/modules/jinja2-2.7.3')
import markdown
from jinja2 import Template, Environment, FileSystemLoader

# - - - - - - - - - -

env = Environment(loader=FileSystemLoader('static/templates'))
postget = cgi.FieldStorage()
if not 'c' in postget:
    page = 'person'
else:
    page = postget['c'].value

fd = codecs.open('static/content/{0}.md'.format(page), encoding='utf-8')
content = fd.read()
fd.close()

if SEPARATOR+SEPARATOR in content:
    template = env.get_template('split_layout.html')
    (left_all,right_all) = content.split(SEPARATOR+SEPARATOR)
    left = left_all.split(SEPARATOR)
    right = right_all.split(SEPARATOR)
    left = [markdown.markdown(l, extensions=MD_EXT) for l in left]
    right = [markdown.markdown(r, extensions=MD_EXT) for r in right]
    fill = None
else:
    template = env.get_template('fill_layout.html')
    fill = content.split(SEPARATOR)
    fill = [markdown.markdown(f, extensions=MD_EXT) for f in fill]
    left = None
    right = None

navitems=[{'link':'tl_dr','text':'tl;dr'},
            {},
            {},
            {},
            {},
            {},
            {},
            {'link':'blog','text':'blog'},
            {'link':'person','text':'person'},
            {'link':'interests','text':'interests'},
            {'link':'projects','text':'projects'},
            {},
            {},
            {'link':'contact','text':'contact'}]

unicode_page = template.render(navitems=navitems, left=left, right=right,
                                fill=fill, subtitle=page)
print 'Content-Type: text/html\n\n'
print unicode_page.encode('utf-8')
