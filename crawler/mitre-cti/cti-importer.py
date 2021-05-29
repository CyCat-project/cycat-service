import argparse
import json
import redis
import os
import requests
import uuid
parser = argparse.ArgumentParser(description='MITRE CTI (ATT&CK) import for CyCAT')
parser.add_argument('-p', '--path', help='Path to the CTI git repository')
args = parser.parse_args()
rdb = redis.Redis(host='127.0.0.1', port='3033')

# CTI parent c7001e65-fefe-55cb-84a3-97ec2620137

projectuuid='c7001e65-fefe-55cb-84a3-97ec2620137a'

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

models = ['enterprise-attack', 'mobile-attack', 'ics-attack', 'pre-attack']

for model in models:
    path = "{}/{}/{}.json".format(args.path, model, model)
    f = open(path, mode='r')
    m = json.loads(f.read())
    for obj in m['objects']:
        (obj_type, obj_id) = obj['id'].split('--')
        if obj_type != 'relationship':
            data = {}
            data['raw'] = str(obj)
            data['mitre-cti:type'] = obj['type']
            if 'description' in obj:
                data['mitre-cti:description'] = obj['description']
            if 'name' in obj:
                data['mitre-cti:name'] = obj['name']
            if 'external_references' in obj:
                for ref in obj['external_references']:
                    if ref['source_name'] == 'mitre-attack':
                        data['mitre-attack-id'] = ref['external_id']
                    if ref['source_name'] == 'capec':
                        data['capec'] = ref['external_id']
            additem(uuidref=obj_id, project=projectuuid, data=data)
        elif obj_type == 'relationship':
            (source_type, source_id) = obj['source_ref'].split('--')
            (destination_type, destination_id) = obj['target_ref'].split('--')
            addrelationship(uuidsource=source_id, uuiddest=destination_id, data=str(obj))

