#!/usr/bin/env python

import re, os, sqlite3
from bs4 import BeautifulSoup
from urllib import parse

db = sqlite3.connect('./Racket.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = './Racket.docset/Contents/Resources/Documents/'

def fetch(f):
    filename = os.path.join(root, f)
    page = open(filename).read()
    soup = BeautifulSoup(page)

    for group in soup.select('.SVInsetFlow'):
        type_ele = group.find('div', { 'class': 'RBackgroundLabelInner' })
        _path = None

        if type_ele:
            _type = type_ele.text
        else:
            return

        for tag in group.select('.RktValDef'):
            _name = tag.text
            if tag['href'].startswith('#'):
                _path = filename.replace(docpath, '') + tag['href']
            elif 'local-redirect' in tag['href']:
                matches = re.search('doc=(.*)&rel=(.*)', tag['href'])
                _path = matches.group(1) + '/' + parse.unquote(matches.group(2))

            if _path:
                print('type: %s, name: %s, path: %s' % (_type, _name, _path))
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (_name, _type.title(), _path))


for root, dirs, files in os.walk(docpath):
    for f in files:
        if f.endswith('.html') and 'demo' not in root:
            fetch(f)

db.commit()
db.close()
