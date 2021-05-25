import argparse
import json
import redis
import os
import requests
import uuid
parser = argparse.ArgumentParser(description='GitHub import for CyCAT')
parser.add_argument('-o', '--org', help='GitHub organisation (fallback to user if not existing as org) to import')
parser.add_argument('-f', '--full', help='Import all repositories as project in CyCAT', default=False, action='store_true')
parser.add_argument('-r', '--repo', help='Limit to a single GitHub repository import', default=None)
args = parser.parse_args()
rdb = redis.Redis(host='127.0.0.1', port='3033')

if not args.org:
    parser.print_usage()
    os.sys.exit(1)

r = requests.get("https://api.github.com/orgs/{}".format(args.org))
urlpath = 'orgs'
org = r.json()
if 'node_id' not in org:
    r = requests.get("https://api.github.com/users/{}".format(args.org))
    org = r.json()
    urlpath = 'users'

print(org['node_id'])

# 39d6e10c-dac7-40e2-8e99-1ab1cefea6f4 (UUIDv5)

orguuid = str(uuid.uuid5(uuid.UUID("39d6e10c-dac7-40e2-8e99-1ab1cefea6f4"),
                     "{}".format(org['node_id'])))

print(orguuid)

rdb.set("u:{}".format(orguuid), 1)
d = {"{}".format(orguuid): 1}
k = "t:{}".format(1)
rdb.zadd(k, d, nx=False)
orgh = {}
orgh['github:name'] = org['name']
if 'description' in org:
    orgh['github:description'] = org['description']
if 'bio' in org:
    orgh['github:bio'] = org['bio']
orgh['github:html_url'] = org['html_url']
if org['email'] is not None:
    orgh['github:email'] = org['email']
orgh['github:login'] = org['login']
if org['location'] is not None:
    orgh['github:location'] = org['location']
orgh['cycat-oid'] = str(orguuid)
print(orgh)
rdb.hmset("{}:{}".format(1, orguuid), orgh)

def cycatoid(node_id=None):
    if node_id is None:
        return False
    _cycatoid = uuid.uuid5(uuid.UUID("39d6e10c-dac7-40e2-8e99-1ab1cefea6f4"), "{}".format(node_id))
    return str(_cycatoid)

if args.full:
    r = requests.get("https://api.github.com/{}/{}/repos?per_page=100".format(urlpath, args.org))
    for repo in r.json():
        if args.repo is not None:
            if args.repo != repo['name']:
                print("Skip {}".format(repo['name']))
                continue
        print(repo)
        projectuuid = cycatoid(node_id=repo['node_id'])
        rdb.set("u:{}".format(projectuuid), 2)
        d = {"{}".format(projectuuid): 1}
        k = "t:{}".format(2)
        rdb.zadd(k, d, nx=False)
        print(repo['node_id'])
        print(repo['name'])
        print(cycatoid(node_id=repo['node_id']))
        print(repo['description'])
        print()
        projecth = {}
        projecth['github:name'] = repo['name']
        if repo['description'] is None:
            repo['description'] = ""
        projecth['github:description'] = repo['description']
        projecth['github:html_url'] = repo['html_url']
        projecth['cycat-oid'] = str(projectuuid)
        rdb.hmset("{}:{}".format(2, projectuuid), projecth)
        rdb.sadd("parent:{}".format(projectuuid), orguuid)
        rdb.sadd("child:{}".format(orguuid), projectuuid)
