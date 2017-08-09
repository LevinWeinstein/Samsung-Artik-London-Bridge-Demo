#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://artikuser:iot2017@45.55.4.31/workshop')
db = client.workshop

@app.route('/collections', methods=['GET'])
def get_collections():
	return jsonify({'collections': db.collection_names()})

@app.route('/collections/<string:collection_name>', methods=['GET'])
def get_collection(collection_name):
	collection = db[collection_name]
	output = []
	for d in collection.find():
		output.append(d);
	print(output)
	return jsonify({collection_name: output})

@app.route('/collections/<string:collection_name>/<string:entry_id>', methods=['GET'])
def get_entry(collection_name, entry_id):
	collection = db[collection_name]
	output = []
	for d in collection.find({'_id': entry_id}):
		output.append(d)
	print(output)
	return jsonify(output[0])

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)
