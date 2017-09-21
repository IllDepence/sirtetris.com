#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi
import cgitb
cgitb.enable()

import codecs
import json.decoder # why OVH? why?!
import json.encoder
import os
import re
import sys

HOME_DIR = '/home/sirtetri/www/'
#HOME_DIR = '/usr/share/nginx/html/tarek/sirtetris/'
SEPARATOR = u'- - -\n'
MD_EXT = ['markdown.extensions.tables']
navitems=[{'link':'def','text':'def'},
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
sys.path.append(HOME_DIR + 'modules/Markdown-2.4')
sys.path.append(HOME_DIR + 'modules/MarkupSafe-0.23')
sys.path.append(HOME_DIR + 'modules/jinja2-2.7.3')
import markdown
from jinja2 import Template, Environment, FileSystemLoader

# - - - - - - - - - -

def yt_toggles(markdown):
    yt_toggle = re.compile('<!-- ytdd:(.*):(.*) -->', re.M)
    return re.sub(yt_toggle, r'<a href="//www.youtube.com/watch?v=\2" id="\2"'\
        r' class="vis-tggl">\1</a><br>'\
        r'<div id="vis-cntnt-\2" class="vis-off"></div>', markdown)

def yt_inserts(markdown):
    yt_toggle = re.compile('<!-- yt:(.*) -->', re.M)
    return re.sub(yt_toggle, r'<iframe width="700" height="436" '\
        r'src="//www.youtube.com/embed/\1" frameborder="0" allowfullscreen>'\
        r'</iframe>', markdown)

def blog_entry(e, imgside):
    image = ''
    image_sources = []
    if len(e['image']) > 0:
        src_file = re.sub(r'\.[a-z0-9]{1,5}$', '.src', e['image'])
        path = 'static/img/blog/' + src_file
        if os.path.isfile(path):
            fd = codecs.open(path, encoding='utf-8')
            lines = fd.readlines()
            fd.close()
            image_sources = [l.strip() for l in lines]
    template = env.get_template('blog_entry.html')
    blog_entry = template.render(eid=e['id'], headline=e['headline'],
        image=e['image'], image_sources=image_sources, image_side=imgside,
        text=e['text'], tags=e['tags'], date=e['date'])
    return blog_entry

def blog_entries(postget):
    perma = None
    tag   = None
    page  = 1
    perpage = 3

    fd = codecs.open('static/blog/entries.json', encoding='utf-8')
    jsn = fd.read()
    fd.close()
    entries_u = jsdec.decode(jsn)
    entries = sorted(entries_u, key=lambda e: e['date'], reverse=True)
    maxpage = ((len(entries)-1)/perpage)+1

    if 'a' in postget:
        perma = postget['a'].value
    if 't' in postget:
        tag   = postget['t'].value
    if 'p' in postget:
        page  = min(int(postget['p'].value), maxpage)

    content = ''

    if perma != None:   # permalink
        for i in range(0, len(entries)):
            if entries[i]['id'] == perma:
                st_idx = i
                ed_idx = i+1
    elif tag != None:   # tag
        tag_dict = {}
        entries_filtered = []
        for e in entries:
            if tag in e['tags']:
                entries_filtered.append(e)
            for t in e['tags']:
                if not t in tag_dict:
                    tag_dict[t] = 0
                tag_dict[t] = tag_dict[t]+1
        tag_list = sorted(tag_dict.items(), key=lambda x: x[1])[::-1]
        template = env.get_template('tag_overview.html')
        tag_overview = template.render(tag_curr=tag, tag_list=tag_list)
        content = tag_overview + u'\n- - -\n'
        entries = entries_filtered
        st_idx = 0
        ed_idx = len(entries)
    else:               # normal
        st_idx = perpage * (page-1)
        ed_idx = min(st_idx+perpage, len(entries))

    imgside = 'left'
    for i in range(st_idx, ed_idx):
        content += blog_entry(entries[i], imgside)
        if i<(ed_idx-1):
            content += u'\n- - -\n'
        if imgside == 'left': imgside = 'right'
        else: imgside = 'left'

    if perma == None and tag == None:
        page_nums = range(1,maxpage+1)[::-1]
        template = env.get_template('nav_bar.html')
        nav_bar = template.render(page=page, maxpage=maxpage, page_nums=page_nums)
        content += u'\n- - -\n'
        content += nav_bar

    return content

# - - - - - - - - - -

env = Environment(loader=FileSystemLoader('static/templates'))
postget = cgi.FieldStorage()
if not 'c' in postget and not 'a' in postget and not 'p' in postget and not 't' in postget:
    page = 'def'
elif not 'c' in postget:
    page = 'blog'
else:
    page = postget['c'].value
    valid = [itm['link'] for itm in navitems if 'link' in itm]
    valid.append('imprint')
    if not page in valid:
        page = 'notfound'

if page == 'blog':
    content = blog_entries(postget)
else:
    fd = codecs.open('static/pages/{0}.md'.format(page), encoding='utf-8')
    content = fd.read()
    fd.close()

content = yt_toggles(content)
content = yt_inserts(content)

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
print 'Content-Type: text/html\r\n'
print unicode_page.encode('utf-8')
