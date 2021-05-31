version = "0.9"
from flask import Flask, url_for, send_from_directory, render_template, make_response, request
from flask_restx import Resource, Api, reqparse
import os
import uuid
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app, version=version, title='CyCAT.org API', description='CyCAT - The Cybersecurity Resource Catalogue public API services.', doc='/', license='CC-BY', contact='info@cycat.org', ordered=True)
import inspect
import redis
cycat_type = {"1": "Publisher", "2": "Project", "3": "Item"}

r = redis.Redis(host='127.0.0.1', port='3033', decode_responses=True)

# full-text part (/search API)

from whoosh import index, qparser
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
indexpath = "../index"
ix = index.open_dir(indexpath)


# generic lib - TODO: move to cycat Python library

def _validate_uuid(value=None):
    if uuid is None:
        return False
    try:
        _val = uuid.UUID(value)
    except ValueError:
        return False
    return True

@api.route('/info')
@api.doc(description="Get information about the CyCAT backend services including status, overall statistics and version.")
class info(Resource):
    def get(self):
        info = {}
        info['publishers'] = r.zcard('t:1')
        info['projects'] = r.zcard('t:2')
        info['items'] = r.zcard('t:3')
        info['namespaces'] = r.scard('idnamespace')
        info['version'] = version
        return info

@api.route('/generate/uuid')
@api.doc(description="Generate an UUID version 4 RFC4122-compliant.")
class generateUUID(Resource):
    def get(self):
        genuuid = uuid.uuid4()
        k = "stats:f:{}".format(inspect.stack()[0][3].lower())
        r.incr(k, 1)
        return "{}".format(genuuid)

@api.route('/favicon.ico', doc=False)
class favicon(Resource):
    def get(self):
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')

@api.route('/list/publisher/<int:start>/<int:end>')
@api.doc(description="List publishers registered in CyCAT by pagination (start,end).")
class list_publisher(Resource):
    def get(self, start, end):
        uuids = r.zrange('t:1', start, end)
        publishers = []
        for uuidvalue in uuids:
            _publisher = r.hgetall('1:{}'.format(uuidvalue))
            publishers.append(_publisher)
        return publishers

@api.route('/list/project/<int:start>/<int:end>')
@api.doc(description="List projects registered in CyCAT by pagination (start,end).")
class list_project(Resource):
    def get(self, start, end):
        uuids = r.zrange('t:2', start, end)
        publishers = []
        for uuidvalue in uuids:
            _publisher = r.hgetall('2:{}'.format(uuidvalue))
            publishers.append(_publisher)
        return publishers


@api.route('/lookup/<string:uuid>')
@api.doc(description="Lookup UUID registered in CyCAT.")
class lookup(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("u:{}".format(uuid)):
                return{'message': 'Non existing UUID'}, 404
            t = r.get("u:{}".format(uuid))
            if not r.exists("{}:{}".format(t, uuid)):
                return{'message': 'UUID allocated but no existing attributes'}, 404
            h = r.hgetall("{}:{}".format(t, uuid))
            h['_cycat_type'] = cycat_type[str(t)]
            return (h)
        else:
            return {'message': 'UUID is incorrect'}, 400

@api.route('/parent/<string:uuid>')
@api.doc(description="Get parent UUID(s) from a specified project or item UUID.")
class parent(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("parent:{}".format(uuid)):
                return{'message': 'Non existing parent UUID'}, 404
            s = r.smembers("parent:{}".format(uuid))
            return(list(s))
        else:
            return {'message': 'UUID is incorrect'}, 400

@api.route('/child/<string:uuid>')
@api.doc(description="Get child UUID(s) from a specified project or publisher UUID.")
class child(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("child:{}".format(uuid)):
                return{'message': 'Non existing child UUID'}, 404
            s = r.smembers("child:{}".format(uuid))
            return(list(s))
        else:
            return {'message': 'UUID is incorrect'}, 400

@api.route('/relationships/<string:uuid>')
@api.doc(description="Get relationship(s) UUID from a specified UUID.")
class relationships(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("r:{}".format(uuid)):
                return{'message': 'Non existing relationships for UUID'}, 404
            s = r.smembers("r:{}".format(uuid))
            return(list(s))
        else:
            return {'message': 'UUID is incorrect'}, 400

@api.route('/relationships/expanded/<string:uuid>')
@api.doc(description="Get relationship(s) UUID from a specified UUID including the relationships meta information.")
class relationshipsexpanded(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("r:{}".format(uuid)):
                return{'message': 'Non existing relationships for UUID'}, 404
            d = {}
            s = r.smembers("r:{}".format(uuid))
            rels = []
            for rel in s:
                data = r.smembers("rd:{}:{}".format(uuid, rel))
                rels.append(str(data))
            d['relationships'] = list(rels)
            d['destinations'] = list(s)
            d['source'] = uuid
            return(d)
        else:
            return {'message': 'UUID is incorrect'}, 400

@api.route('/namespace/getall')
@api.doc(description="List all known namespaces.")
class namespacegetall(Resource):
    def get(self):
        s = r.smembers("idnamespace")
        return(list(s))

@api.route('/namespace/getid/<string:namespace>')
@api.doc(description="Get all ID from a given namespace.")
class namespacegetid(Resource):
    def get(self, namespace=None):
        if namespace is None:
            return None
        k = "idk:{}".format(namespace)
        s = r.smembers(k)
        return(list(s))

@api.route('/namespace/finduuid/<string:namespace>/<string:namespaceid>')
@api.doc(description="Get all known UUID for a given namespace id.")
class namespacefinduuid(Resource):
    def get(self, namespace=None, namespaceid=None):
        if namespaceid is None or namespace is None:
            return None
        k = "id:{}:{}".format(namespace, namespaceid)
        s = r.smembers(k)
        return(list(s))

@api.route('/propose')
@api.doc(description="Propose new resource to CyCAT.")
class propose(Resource):
    def post(self):
        x = request.get_json(force=True)
        r.rpush("proposal", json.dumps(x))
        return {'message': 'Proposal submitted'}, 200

@api.route('/search/<string:searchquery>')
@api.doc(description="Full-text search in CyCAT and return matching UUID.")
class search(Resource):
    def get(self, searchquery=None):
        if searchquery is None:
            return None
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(searchquery)
            results = searcher.search(query, limit=None)
            uuids = []
            for result in results:
                uuids.append(result['path'])
        return(uuids)
if __name__ == '__main__':
    app.run()
