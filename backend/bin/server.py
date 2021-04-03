version = "0.1"
from flask import Flask
app = Flask(__name__)
import uuid
import inspect
import redis

r = redis.Redis(host='127.0.0.1', port='3033')
@app.route('/info')
def info():
    return "CyCAT backend {}".format(version)

@app.route('/generate/uuid')
def generateUUID():
    genuuid = uuid.uuid4()
    k = "stats:f:{}".format(inspect.stack()[0][3].lower())
    r.incr(k, 1)
    return "{}".format(genuuid)

if __name__ == '__main__':
    app.run()
