import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/time', methods = ['GET'])
def get_current_time():
	return {'time': time.time()}

itinerary = {
    '1': 1,
    '2': 2
}

@app.route('/api/itinerary', methods = ['GET'])
def get_itinerary():
    return jsonify(itinerary)
