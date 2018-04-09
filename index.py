import glob
import sqlite3

from pathlib import Path
from bs4 import BeautifulSoup


"""
CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);
CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);
INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES ('Exploit', 'Class', 'index.html');
"""

pkg = Path('frida.docset/Contents/Resources')
conn = sqlite3.connect(str(pkg / 'docSet.dsidx'))
conn.executescript('''
    CREATE TABLE IF NOT EXISTS searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);
    CREATE UNIQUE INDEX IF NOT EXISTS anchor ON searchIndex (name, type, path);''')



def insert(*args):
    conn.execute('''INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?);''', args)


base = pkg / 'Documents'
for filename in glob.glob('%s/docs/**/*.html' % base, recursive=True):
    with open(filename) as fp:
        html = fp.read()

    soup = BeautifulSoup(html)
    title = soup.find('h1').text
    relpath = str(Path(filename).relative_to(base))
    type_map = {
        'examples': 'Sample',
        'c-api': 'Binding',
        'javascript-api': 'Binding',
        'swift-api': 'Binding',
        'presentations': 'Resource',
        'frida-': 'Command',
    }

    page_type = 'Guide'
    for prefix, type_name in type_map.items():
        if relpath.startswith('docs/%s' % prefix):
            page_type = type_name
            break

    insert(title, page_type, relpath)

    section_type = 'Section'

    for subtitle in soup.select('h2'):
        anchor = subtitle['id']
        name = subtitle.text

        if relpath == 'docs/javascript-api/index.html':
            # for method in subtitle.select('+ ul'):
            #     method_type = 'Function' if anchor == 'global' else 'Method'
            #     insert(subtitle.text, method_type, '%s#%s' % (relpath, anchor))

            section_type = 'Namespace' if name.lower() == name else 'Class'
        insert(subtitle.text, section_type, '%s#%s' % (relpath, anchor))

conn.commit()
conn.close()
