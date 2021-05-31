import argparse
from whoosh import index, qparser
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
indexpath = "../index"
argParser = argparse.ArgumentParser(description="Full text search for cycat")
argParser.add_argument("-q", action="append", help="query to lookup (one or more)")
args = argParser.parse_args()
ix = index.open_dir(indexpath)

with ix.searcher() as searcher:
    if len(args.q) == 1:
        query = QueryParser("content", ix.schema).parse(" ".join(args.q))
    else:
        query = QueryParser("content", schema=ix.schema, group=qparser.AndGroup).parse(" ".join(args.q))

    results = searcher.search(query, limit=None)
    for result in results:
        print(result['path'])
    print(results)
