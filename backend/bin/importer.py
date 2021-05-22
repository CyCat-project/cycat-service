import argparse
import json
import redis
import os
parser = argparse.ArgumentParser(description='JSON importer for CyCAT backend')
parser.add_argument('-f', '--file', help='JSON file to import')
parser.add_argument('-t', '--type', help='CyCAT backend type', default=1)
args = parser.parse_args()
r = redis.Redis(host='127.0.0.1', port='3033')

if not args.file:
    parser.print_usage()
    os.sys.exit(1)

with open(args.file, 'r') as f:
    toimport = f.read()
    record = json.loads(toimport)

if int(args.type) == 1:
    uuid = record['cycat-oid']
    r.set("u:{}".format(uuid), args.type)
    d = {"{}".format(uuid): 1}
    k = "t:{}".format(args.type)
    r.zadd(k, d, nx=False)
    print(uuid)
    r.hmset("{}:{}".format(args.type, uuid), record)
    print(record)
elif int(args.type) == 2:
    uuid = record['cycat-oid']
    r.set("u:{}".format(uuid), args.type)
    d = {"{}".format(uuid): 1}
    k = "t:{}".format(args.type)
    r.zadd(k, d, nx=False)
    r.hmset("{}:{}".format(args.type, uuid), record)
else:
    pass
