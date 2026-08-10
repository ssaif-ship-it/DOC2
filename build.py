#!/usr/bin/env python3
"""
Refresh the offline snapshot embedded inside index.html.

index.html reads content in this order:
    1. an uncommitted draft in your browser
    2. GitHub, when a repo is connected      <- the real source of truth
    3. the .md files next to it, when served over http
    4. the snapshot baked into index.html    <- what this script updates
So the snapshot is only a fallback for opening index.html straight from Finder
before GitHub is connected. Run this after editing the .md files locally:

    python3 build.py
"""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, 'index.html')
DOCS = os.path.join(HERE, 'upi_docs')

BEGIN = '<!-- SNAPSHOT:BEGIN -->'
END = '<!-- SNAPSHOT:END -->'


def main():
    if not os.path.isfile(INDEX):
        sys.exit('index.html not found next to this script.')
    if not os.path.isdir(DOCS):
        sys.exit('upi_docs/ not found next to this script.')

    docs = {}
    for name in sorted(os.listdir(DOCS)):
        if name.endswith('.md'):
            with open(os.path.join(DOCS, name), encoding='utf-8') as fh:
                docs['upi_docs/' + name] = fh.read()

    payload = base64.b64encode(
        json.dumps(docs, ensure_ascii=False).encode('utf-8')
    ).decode('ascii')

    with open(INDEX, encoding='utf-8') as fh:
        html = fh.read()

    block = (
        BEGIN + '\n'
        '    <script id="cf-snapshot" type="application/octet-stream">'
        + payload +
        '</script>\n    ' + END
    )

    new_html, n = re.subn(
        re.escape(BEGIN) + r'.*?' + re.escape(END),
        lambda _m: block,
        html,
        count=1,
        flags=re.S,
    )
    if not n:
        sys.exit('Could not find the SNAPSHOT markers in index.html.')

    with open(INDEX, 'w', encoding='utf-8') as fh:
        fh.write(new_html)

    total = sum(len(v) for v in docs.values())
    print('Snapshot refreshed: %d sections, %d characters.' % (len(docs), total))


if __name__ == '__main__':
    main()
