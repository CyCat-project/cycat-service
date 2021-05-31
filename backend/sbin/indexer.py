import redis
import os
import sys

cycat_type = {"1": "Publisher", "2": "Project", "3": "Item"}

rdb = redis.Redis(host='127.0.0.1', port='3033', decode_responses=True)

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in, exists_in, open_dir

schema = Schema(
    title=TEXT(stored=True), path=ID(stored=True, unique=True), content=TEXT
)
indexpath = "../index"
if not os.path.exists(indexpath):
    os.mkdir(indexpath)

if not exists_in(indexpath):
    ix = create_in(indexpath, schema)
else:
    ix = open_dir(indexpath)

try:
    writer = ix.writer()
except:
    print("Index is locked.")
    sys.exit(1)

def getUUID(oid=None, oidtype=1):
    if oid is None:
        return None
    return rdb.hgetall('{}:{}'.format(oidtype, oid))

for ctype in cycat_type:
    card = rdb.zcard("t:{}".format(ctype))
    for start in range(0, card, 100):
        i = start+100
        x = rdb.zrange('t:{}'.format(ctype), start, i)
        for item in x:
            toindex = getUUID(oid=item, oidtype=ctype)
            print(toindex)
            title = ""
            content = ""
            if 'title' in toindex:
                title = toindex['title']
                content = content + toindex['title']
            if 'raw' in toindex:
                content = toindex['raw']
            if 'description' in toindex:
                title = title + toindex['description']
                content = content + toindex['description']
            if 'mitre-cti:description' in toindex:
                title = title + toindex['mitre-cti:description']
                content = content + toindex['mitre-cti:description']
            if 'github:description' in toindex:
                title = title + toindex['github:description']
                content = content + toindex['github:description']
            writer.update_document(title=title, path=item, content=content)
writer.commit()
