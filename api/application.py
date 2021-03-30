import time
from flask import Flask, jsonify, request, json

from sample_itinerary import *

app = Flask(__name__)


@app.route('/')
def home():
    return "ok"


@app.route('/api/time', methods=['GET'])
def get_current_time():
    return {'time': time.time()}


@app.route('/api/recommend', methods=['POST'])
def submit_recommend():
    request_data = json.loads(request.data)

    # Publish recommend message

    return {'200': 'Running recommendation engine'}


@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    loading = "no"
    itinerary = get_sample_itinerary()

    # Subscribed for message for itinerary created

    return_dict = {
        "loading": loading,
        "itinerary": itinerary
    }

    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
