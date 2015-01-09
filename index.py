#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()

import codecs
import json.decoder # why OVH? why?!
import json.encoder
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
jsdec = json.decoder.JSONDecoder()
jsenc = json.encoder.JSONEncoder()

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
        r'<iframe id="vis-content-\1" width="700" height="436" '\
        r'src="//www.youtube.com/embed/\2" frameborder="0" allowfullscreen>'\
        r'</iframe>', markdown)

def blog_entry(e, imgside):
    content = u'# [{0}](?a={1})\n'.format(e['headline'], e['id'])
    content +=  u'<div class="imgfloat{0}">'\
                    u'<img src="static/img/blog/{1}">'\
                    u'<div class="imgsrc"><p>'\
                        u'<a href="static/img/blog/{2}">source</a>'\
                    u'</p></div>'\
                u'</div>\n'.format(imgside, e['image'], 'source')
    content += u'{0}\n'.format(e['text'])
    content += u'<div class="footline">'\
                u'<div class="tags"><p><strong>tags: {0}</strong></p></div>'\
                u'<div class="date"><p>{1}</p></div>'\
               u'</div>'.format(' '.join(e['tags']), e['date'])
    return content

def blog_entries(postget):
    perma = None
    tag   = None
    page  = 1

    # read entries from json file
    fd = codecs.open('static/blog/entries.json', encoding='utf-8')
    jsn = fd.read()
    fd.close()
    entries_u = jsdec.decode(jsn)
    entries = sorted(entries_u, key=lambda e: e['date'], reverse=True)

    # handle permalinks, tags, pages
    if 'a' in postget:
        perma = postget['a'].value
    if 't' in postget:
        tag   = postget['t'].value
    if 'p' in postget:
        page  = postget['p'].value
    # return apprpriate subset

    content = blog_entry(entries[0], 'left')
    content += '\n- - -\n'
    content += blog_entry(entries[1], 'right')
    content += '\n- - -\n'
    content += blog_entry(entries[2], 'left')
    #return md_entries
    return content

# - - - - - - - - - -

env = Environment(loader=FileSystemLoader('static/templates'))
postget = cgi.FieldStorage()
if not 'c' in postget:
    page = 'blog'
else:
    page = postget['c'].value
    valid = [itm['link'] for itm in navitems if 'link' in itm]
    if not page in valid:
        page = 'notfound'

if page == 'blog':
    content = blog_entries(postget)
else:
    fd = codecs.open('static/pages/{0}.md'.format(page), encoding='utf-8')
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
