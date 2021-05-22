version = "0.1"
from flask import Flask, url_for, send_from_directory, render_template, make_response
from flask_restx import Resource, Api
import os
import uuid

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app, version=version, title='CyCAT.org API', description='CyCAT - The Cybersecurity Resource Catalogue public API services.', doc='/doc/')
import uuid
import inspect
import redis


r = redis.Redis(host='127.0.0.1', port='3033')

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
        return "CyCAT backend {}".format(version)

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

@api.route('/lookup/<string:uuid>')
class lookup(Resource):
    def get(self, uuid):
        if _validate_uuid(value=uuid):
            return ("{}".format(uuid))
        else:
            return {'message': 'UUID is incorrect'}, 400

if __name__ == '__main__':
    app.run()
