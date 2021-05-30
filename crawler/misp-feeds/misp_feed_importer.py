
import argparse
import json
import redis
import os
import requests
import uuid
import re
import yaml

parser = argparse.ArgumentParser(description='MISP feed importer for CyCAT')
parser.add_argument('-u', '--url', help='MISP feed url')
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

r = requests.get("{}/manifest.json".format(args.url))
feed = r.json()
for event in feed:
    data = {}
    data['uuid'] = event
    data['description'] = feed[event]['info']
    data['timestamp'] = feed[event]['timestamp']
    data['link'] = "{}/{}.json".format(args.url, event)
    data['misp:feed'] = "{}".format(args.url)
    if 'Tag' in feed[event]:
        for tags in feed[event]['Tag']:
            addexternalid(uuidsource=data['uuid'], namespace='misp-tag', namespaceid=tags['name'].lower())
            pattern = re.compile(r"^misp-galaxy:mitre-")
            if pattern.search(tags['name']):
                (namespacepredicate, value) = tags['name'].split('=')
                try:
                    mitre = value.rsplit('-', 1)[1]
                    mitreattackid = mitre.replace(" ", "").replace("\"","")
                    addexternalid(uuidsource=data['uuid'], namespace='mitre-attack-id', namespaceid=mitreattackid)
                except:
                    continue
    additem(uuidref=data['uuid'], data=data)
