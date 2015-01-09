#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()

import codecs
import re
import sys

HOME_DIR = '/homez.151/sirtetri/'
SEPARATOR = u'- - -\n'
MD_EXT = ['markdown.extensions.tables']
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

# markdown v2.5 dropped support for python 2.6, OVH uses python 2.6.6
# also, including modules w/o installing because hosting contract only
sys.path.append(HOME_DIR + 'moc/pywebsite/modules/Markdown-2.4')
sys.path.append(HOME_DIR + 'moc/pywebsite/modules/MarkupSafe-0.23')
sys.path.append(HOME_DIR + 'moc/pywebsite/modules/jinja2-2.7.3')
import markdown
from jinja2 import Template, Environment, FileSystemLoader

# - - - - - - - - - -

def yt_toggles(markdown):
    yt_toggle = re.compile('^<!-- ytdd:(.*):(.*) -->$', re.M)
    return re.sub(yt_toggle, r'<label for="vis-toggle-\2">\1</label><br>'\
        r'<input type="checkbox" id="vis-toggle-\2"/>'\
        r'<iframe id="vis-content-\2" width="700" height="436" '\
        r'src="//www.youtube.com/embed/\2" frameborder="0" allowfullscreen>'\
        r'</iframe>', markdown)

def blog_entries(postget):
    #TODO implement

    # read entries from json file
    # handle permalinks, tags, pages
    # return apprpriate subset
    return md_entries

# - - - - - - - - - -

env = Environment(loader=FileSystemLoader('static/templates'))
postget = cgi.FieldStorage()
if not 'c' in postget:
    page = 'person'
else:
    page = postget['c'].value
    valid = [itm['link'] for itm in navitems if 'link' in itm]
    if not page in valid:
        page = 'notfound'

if page = 'blog':
    content = blog_entries(postget)
else:
    fd = codecs.open('static/content/{0}.md'.format(page), encoding='utf-8')
    content = fd.read()
    fd.close()

content = yt_toggles(content)

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

unicode_page = template.render(navitems=navitems, left=left, right=right,
                                fill=fill, subtitle=page)
print 'Content-Type: text/html\n\n'
print unicode_page.encode('utf-8')
