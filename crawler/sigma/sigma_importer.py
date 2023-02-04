# Project cycat oid - 3f489963-edb6-5579-aefc-5c1deca8df8b

import argparse
import json
import redis
import os
import requests
import uuid
import re
import yaml

parser = argparse.ArgumentParser(description='Sigma import for CyCAT')
parser.add_argument('-p', '--path', help='Sigma path of the git repository')
args = parser.parse_args()
rdb = redis.Redis(host='127.0.0.1', port='3033')

projectuuid = '3f489963-edb6-5579-aefc-5c1deca8df8b'
sigmafile = '^.*\.yml$'
if not args.path:
    parser.print_usage()
    os.sys.exit(1)

def additem(uuidref=None, data=None, project=None):
    if uuidref is None or data is None:
        return None
    rdb.set("u:{}".format(uuidref), 3)
    d = {"{}".format(uuidref): 1}
    k = "t:{}".format(3)
    rdb.zadd(k, d, nx=False)
    rdb.hmset("{}:{}".format(3, uuidref), data)
    if project is not None:
        rdb.sadd("parent:{}".format(uuidref), project)
        rdb.sadd("child:{}".format(project), uuidref)
    if 'capec' in data:
        addexternalid(uuidsource=uuidref, namespace='capec', namespaceid=data['capec'])
    if 'mitre-attack-id' in data:
        addexternalid(uuidsource=uuidref, namespace='mitre-attack-id', namespaceid=data['mitre-attack-id'])
    return True

def addrelationship(uuidsource=None, uuiddest=None, data=None):
    if uuidsource is None or uuiddest is None:
        return None
    rdb.sadd("r:{}".format(uuidsource), uuiddest)
    rdb.sadd("rd:{}:{}".format(uuidsource, uuiddest), data)
    return True

def addexternalid(uuidsource=None, namespace=None, namespaceid=None):
    if uuidsource is None or namespace is None or namespaceid is None:
        return None
    k = "id:{}:{}".format(namespace.lower(), namespaceid)
    rdb.sadd(k, uuidsource)
    k = "idk:{}".format(namespace)
    rdb.sadd(k, namespaceid)
    rdb.sadd("idnamespace", namespace)

for root, dirs, files in os.walk("{}./rules".format(args.path)):
    path = root.split(os.sep)
    for f in files:
        if not re.match(sigmafile, f):
            continue
        sigmaf = os.path.join(root, f)
        with open(sigmaf, 'r') as stream:
            rules = yaml.safe_load_all(stream)
            print("File :{}".format(sigmaf))
            for x in rules:
                data = {}
                if 'id' in x:
                    # for CyCAT we only import sigma rules having an id
                    # TODO: open an issue at SigmaHQ about the missing id rules
                    if 'description' in x:
                        data['description'] = x['description']
                        data['title'] = x['title']
                        data['sigma:id'] = x['id']
                        data['raw'] = yaml.dump(x)
                    if 'tags' in x:
                        for tag in x['tags']:
                            if not '.' in tag:
                                continue
                            (namespace, value) = tag.split(".", 1)
                            if namespace == 'attack':
                                addexternalid(uuidsource=x['id'], namespace='mitre-attack-id', namespaceid=value.upper())
                    additem(uuidref=x['id'], project=projectuuid, data=data)
                    continue
                else:
                    continue
                    #print(x)
