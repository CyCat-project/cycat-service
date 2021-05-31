
import argparse
import json
import redis
import os
import requests
import uuid
import re
import yaml

parser = argparse.ArgumentParser(description='MISP galaxy importer for CyCAT')
parser.add_argument('-u', '--url', help='MISP JSON galaxy cluster url')
args = parser.parse_args()
rdb = redis.Redis(host='127.0.0.1', port='3033')

if not args.url:
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

r = requests.get("{}".format(args.url))
cluster = r.json()
for element in cluster['values']:
    data = {}
    data['uuid'] = element['uuid']
    if 'description' in element:
        data['description'] = element['description']
    data['misp-galaxy:value'] = element['value']
    data['raw'] = json.dumps(element)
    if 'related' in element:
        for rel in element['related']:
            addrelationship(uuidsource=data['uuid'], uuiddest=rel['dest-uuid'], data=json.dumps(rel))
    additem(uuidref=data['uuid'], data=data)
