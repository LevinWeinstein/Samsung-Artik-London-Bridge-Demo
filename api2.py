from flask import Flask, jsonify, abort, make_response
from flask_sockets import Sockets
from pymongo import MongoClient
import time

app = Flask(__name__)
sockets = Sockets(app)
client = MongoClient('mongodb://artikuser:iot2017@45.55.4.31/workshop')
db = client.workshop
latest = ""

from flask import Flask, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@sockets.route('/echo')
def echo_socket(ws):
	global latest;
	i = 0;
	while not ws.closed:
		while (check_new('vmworld', 'TowerBridge') == False):
			time.sleep(.1)
			#ws.send("not changed");
		time.sleep(.1)
		ws.send("changed");
		change = get_item('vmworld', 'TowerBridge')
		print(change)
		ws.send("{0}".format(change))

@sockets.route('/echo')
def echo_socket(ws):
	global latest;
	i = 0;
	while not ws.closed:
		if (check_new('vmworld', 'TowerBrige') == True):
			ws.send("{0}".format(get_item('vmworld', 'TowerBridge')))


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/collections', methods=['GET'])
@crossdomain(origin="*")
def get_collections():
	return jsonify({'collections': db.collection_names()})

@app.route('/collections/<string:collection_name>', methods=['GET'])
@crossdomain(origin="*")
def get_collection(collection_name):
	collection = db[collection_name]
	output = []
	for d in collection.find():
		output.append(d);
	print(output)
	return jsonify({collection_name: output})

@app.route('/collections/<string:collection_name>/<string:entry_id>/<string:field_id>', methods=['GET'])
@crossdomain(origin="*")
def get_field(collection_name, entry_id, field_id):
	collection = db[collection_name]
	output = []
	for d in collection.find({'_id': entry_id}):
		output.append(d)
	print(output)
	return jsonify({'_id': entry_id, field_id: output[0]['payload'][field_id]})

@app.route('/collections/<string:collection_name>/<string:entry_id>/change', methods=['GET'])
@crossdomain(origin="*")
def check_new(collection_name, entry_id):
	global latest;
	collection = db[collection_name]
	output = []
	for d in collection.find({'_id': entry_id}):
		output.append(d)
	if latest != output[0]['_msgid']:
		latest = output[0]['_msgid']
		print("changed")
		return jsonify(True)
	print("not changed")
	return jsonify(False)

@app.route('/collections/<string:collection_name>/<string:entry_id>', methods=['GET'])
@crossdomain(origin="*")
#@app.run(threaded=True)
def get_entry(collection_name, entry_id):
	collection = db[collection_name]
	output = []
	for d in collection.find({'_id': entry_id}):
		output.append(d)
	print(output)
	return jsonify(output[0])

def get_item(collection_name, entry_id):
	global latest;
	collection = db[collection_name]
	output = []
	for d in collection.find({'_id': entry_id}):
		output.append(d)
	return output[0]



if __name__ == "__main__":
	from gevent import pywsgi
	from geventwebsocket.handler import WebSocketHandler
 	#last_ts = db.oplog.rs.find().sort('$natural', -1)[0]['ts'];
	#print(last_ts);
	#app.run(threaded=True)
	server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
	server.serve_forever()
