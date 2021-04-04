#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# put in cgi-bin folder and launch server w/
# python3 -m http.server --cgi

import cgi
import cgitb
cgitb.enable()

import datetime
import json
import zlib

html = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
</head>
<body>
<form method="POST" action="acp.py">
headline: <input type="text" name="headline" value="{headline}" /><br>
picture: <input type="text" name="image" value="{image}"><br>
tags: <input type="text" name="tags" value="{tags}"><br>
text: <textarea name="text" style="width: 1000px; height: 400px;">{text}</textarea><br>
{replace}
<input type="submit">
</form><br>
{msg}
<br>
{entrylist}
</body>
</html>
'''

headline=''
image=''
tags=''
text=''
replace_id=None,
msg=''
entrylist=''

def build_html(headline='', image='', tags='', text='', replace_id=None,
               msg='', entrylist=''):
    if replace_id:
        replace = ('<input type="hidden" name="replace" value="{}"/>'
                   '').format(replace_id)
    else:
        replace = ''
    return html.format(headline=headline, image=image, tags=tags, text=text,
                       replace=replace, msg=msg, entrylist=entrylist)


with open('static/blog/entries.json') as f:
    entries = json.load(f)

entries = sorted(entries, key=lambda e: e['date'], reverse=True)

postget = cgi.FieldStorage()
if 'edit' in postget:
    for e in entries:
        if e['id'] == postget['edit'].value:
            headline = e['headline']
            image = e['image']
            tags = e['tags']
            text = e['text']
            replace_id = e['id']
            break

if 'headline' in postget and 'text' in postget:
    msg = '&gt;&gt; enrty '
    if 'replace' in postget and postget['replace'].value != '(None,)':
        for e in entries:
            if e['id'] == postget['replace'].value:
                e['text'] = postget['text'].value
                e['tags'] = postget['tags'].value.split(',')
                e['headline'] = postget['headline'].value;
                e['image'] = postget['image'].value;
                msg += 'edited';
                break
    else:
        new_entry = {}
        new_entry['text'] = postget['text'].value
        new_entry['id'] = '{:x}'.format(
            zlib.adler32(str.encode(new_entry['text']))
            )
        new_entry['tags'] = postget['tags'].value.split(',')
        new_entry['date'] = datetime.datetime.strftime(datetime.datetime.now(),
                                                       '%Y-%m-%d')
        new_entry['headline'] = postget['headline'].value;
        new_entry['image'] = postget['image'].value;
        entries.append(new_entry)
        msg += 'added';

    entries_json = json.dumps(entries)
    with open('static/blog/entries.json', 'w') as f:
        f.write(entries_json)
elif 'del' in postget:
    entries = [e for e in entries if e['id'] != postget['del'].value]
    entries_json = json.dumps(entries)
    with open('static/blog/entries.json', 'w') as f:
        f.write(entries_json)
    msg = '&gt;&gt; enrty deleted.'
else:
    msg = '&gt;&gt; fill in the form.'

entrylist = ''
for e in entries:
    entrylist += ('{} (<a href="?del={}">delete</a> / <a href="?edit={}">edit'
                  '</a>)<br />').format(e['headline'], e['id'], e['id'])

print('Content-Type: text/html\r\n')
print(build_html(headline=headline,
                 image=image,
                 tags=','.join(tags),
                 text=text,
                 replace_id=replace_id,
                 msg=msg,
                 entrylist=entrylist))
