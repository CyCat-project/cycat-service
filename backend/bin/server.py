version = "0.1"
from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app, version=version, title='CyCAT.org API', description='CyberSecurity catalog API services', doc='/doc/')
import uuid
import inspect
import redis


r = redis.Redis(host='127.0.0.1', port='3033')
@api.route('/info')
class info(Resource):
    def get(self):
        return "CyCAT backend {}".format(version)

@api.route('/generate/uuid')
class generateUUID(Resource):
    def get(self):
        genuuid = uuid.uuid4()
        k = "stats:f:{}".format(inspect.stack()[0][3].lower())
        r.incr(k, 1)
        return "{}".format(genuuid)

if __name__ == '__main__':
    app.run()
