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

HOME_DIR = '/home/tarek/www/sirtetris/'
# HOME_DIR = '/var/www/html/tarek/sirtetris/'
SEPARATOR = u'- - -\n'
MD_EXT = ['markdown.extensions.tables']
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

def mixlangs(markdown, mixed):
    mixlang = re.compile('<!-- mixlang:([^>]*):([^>]*) -->', re.M)
    if mixed:
        return re.sub(mixlang, r'\1', markdown)
    else:
        return re.sub(mixlang, r'<span class="mixlang"><span class="swap" '\
            r'swap="\2"><span class="inner">\1</span></span></span>', markdown)

def yt_toggles(markdown):
    yt_toggle = re.compile('<!-- ytdd:(.*):(.*) -->', re.M)
    return re.sub(yt_toggle, r'<a href="//www.youtube.com/watch?v=\2" id="\2"'\
        r' class="vis-tggl">\1</a><br>'\
        r'<span id="vis-cntnt-\2" class="vis-off"></span>', markdown)

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

def blog_entries(req_path_dic):
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

    if 'article' in req_path_dic:
        perma = req_path_dic['article']
    if 'tag' in req_path_dic:
        tag = req_path_dic['tag']
    if 'page' in req_path_dic:
        page = min(int(req_path_dic['page']), maxpage)

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
req_path_str = [val for val in postget.getlist('q') if val != 'index.py'][0]
req_path_arr = req_path_str.split('/')
req_path_dic = {}
for i in range(int(len(req_path_arr)/2)):
    key = req_path_arr[i*2]
    val = req_path_arr[(i*2)+1]
    req_path_dic[key] = val
if req_path_dic.keys()[0] in ['article', 'page', 'tag']:
    section = 'blog'
elif 'section' in req_path_dic:
    if req_path_dic['section'] in ['top', 'blog', 'hbby', 'proj', 'misc',
                                'imprint']:
        section = req_path_dic['section']
    else:
        section = 'notfound'
else:
    section = 'top'

if section == 'blog':
    content = blog_entries(req_path_dic)
elif section != 'top':
    fd = codecs.open('static/pages/{0}.md'.format(section), encoding='utf-8')
    content = fd.read()
    fd.close()
else:
    content = ''

content = yt_toggles(content)
content = yt_inserts(content)
accept_lang = os.environ.get('HTTP_ACCEPT_LANGUAGE', False)
if accept_lang and 'ja' in accept_lang:
    content = mixlangs(content, True)
else:
    content = mixlangs(content, False)

if section == 'top':
    template = env.get_template('tashumimaru.html')
    fill = None
    left = None
    right = None
else:
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
        vill = content.split(SEPARATOR)
        fill = []
        for v in vill:
            if '<span class="textcut"></span>' in v:
                parts = v.split('<span class="textcut"></span>')
                v = u'{0}{1}{2}'.format(
                        parts[0],
                        markdown.markdown(parts[1], extensions=MD_EXT),
                        parts[2]
                        )
            else:
                v = markdown.markdown(v, extensions=MD_EXT)
            fill.append(v)
        left = None
        right = None

unicode_page = template.render(left=left, right=right,
                                fill=fill, subtitle=section)
print 'Content-Type: text/html\r\n'
print unicode_page.encode('utf-8')
