import time
from flask import Flask, jsonify, request, json, session
from flask_session import Session

from sample_itinerary import *
from location_picture_files import *

import pika
import uuid

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


class FrontEnd(object):

    def __init__(self):

        parameters = pika.URLParameters(
            'amqps://Administrator:administrator123@b-8894e7fb-ac9c-4657-8912-473a0bf03efa.mq.us-east-1.amazonaws.com:5671/%2f')
        self.connection = pika.BlockingConnection(parameters)

        # self.connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)

        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, request_data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='frontend_recommendation',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=list(request_data))
        while self.response is None:
            self.connection.process_data_events()
        return list(self.response)


@app.route('/')
def home():
    session['itinerary'] = []
    return "ok"


@ app.route('/api/time', methods=['GET'])
def get_current_time():
    return {'time': time.time()}


def insert_location_picture(location):
    if not location:
        location_pic_data = get_location_pic_data()

        location_name = location['name']
        location['picture'] = location_pic_data[location_name]

    return location


def save_recommended_itinerary(itinerary):
    itinerary_with_pic = []

    for location in itinerary:
        location_with_pic = insert_location_picture(location)
        itinerary_with_pic.append(location)

    session['itinerary'] = itinerary_with_pic


@ app.route('/api/recommend', methods=['POST'])
def submit_recommend():
    # Send message to AmazonMQ and wait for response
    try:
        request_data = json.loads(request.data)
        frontend_client = FrontEnd()
        response = frontend_client.call(request_data)
        save_recommended_itinerary(response)

    except:
        empty_itinerary = {}
        save_recommended_itinerary(empty_itinerary)

    # Testing with sample
    # save_recommended_itinerary(get_sample_itinerary())
    finally:
        return {'200': 'Running recommendation engine'}


def get_itineary_content():
    return session['itinerary']


@ app.route('/api/itinerary', methods=['GET'])
def get_itinerary_plan():
    loading = "no"
    itinerary = get_itineary_content()

    return_dict = {
        "loading": loading,
        "itinerary": itinerary
    }

    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
