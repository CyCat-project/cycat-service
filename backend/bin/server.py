version = "0.2"
from flask import Flask, url_for, send_from_directory, render_template, make_response
from flask_restx import Resource, Api
import os
import uuid

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app, version=version, title='CyCAT.org API', description='CyCAT - The Cybersecurity Resource Catalogue public API services.', doc='/', ordered=True)
import uuid
import inspect
import redis
cycat_type = {"1": "Publisher", "2": "Project"}

r = redis.Redis(host='127.0.0.1', port='3033', decode_responses=True)

# genericc lib - TODO: move to cycat Python library

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

@api.route('/list/publisher/<int:start>/<int:end>', defaults={"start": 0, "end": 10})
class list_publisher(Resource):
    def get(self, start=0, end=10):
        uuids = r.zrange('t:1', start, end)
        publishers = []
        for uuidvalue in uuids:
            _publisher = r.hgetall('1:{}'.format(uuidvalue))
            publishers.append(_publisher)
        return publishers

@api.route('/list/project/<int:start>/<int:end>', defaults={"start": 0, "end": 10})
class list_project(Resource):
    def get(self, start=0, end=10):
        uuids = r.zrange('t:2', start, end)
        publishers = []
        for uuidvalue in uuids:
            _publisher = r.hgetall('2:{}'.format(uuidvalue))
            publishers.append(_publisher)
        return publishers


@api.route('/lookup/<string:uuid>')
class lookup(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("u:{}".format(uuid)):
                return{'message': 'Non existing UUID'}, 404
            t = r.get("u:{}".format(uuid))
            h = r.hgetall("{}:{}".format(t, uuid))
            h['_cycat_type'] = cycat_type[str(t)]
            return (h)
        else:
            return {'message': 'UUID is incorrect'}, 400

@api.route('/parent/<string:uuid>')
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
class parent(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            if not r.exists("child:{}".format(uuid)):
                return{'message': 'Non existing child UUID'}, 404
            s = r.smembers("child:{}".format(uuid))
            return(list(s))
        else:
            return {'message': 'UUID is incorrect'}, 400


if __name__ == '__main__':
    app.run()
