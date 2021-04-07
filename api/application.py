import time
import ast
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
            'amqps://Administrator:administrator12345@b-92f0f3f3-0fa2-4e56-b884-b2bce26b0222.mq.us-east-1.amazonaws.com:5671/%2f')
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
            body=str(request_data))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


@ app.route('/')
def home():
    session['itinerary'] = []
    session['loading'] = 'yes'
    return "ok"


@ app.route('/api/time', methods=['GET'])
def get_current_time():
    return {'time': time.time()}


def insert_location_picture(location):

    location_pic_data = get_location_pic_data()

    location_name = location["poi_name"]

    location["picture"] = location_pic_data[location_name]

    return location


def save_recommended_itinerary(itinerary):
    itinerary_with_pic = []

    for location in itinerary:
        location_with_pic = insert_location_picture(dict(location))
        itinerary_with_pic.append(location_with_pic)

    app.logger.info(location_with_pic)

    # Update session values
    session['itinerary'] = itinerary_with_pic
    session['loading'] = 'no'


@ app.route('/api/recommend', methods=['POST'])
def submit_recommend():

    # Reset Itinerary
    session['itinerary'] = []
    session['loading'] = 'yes'

    # Send message to AmazonMQ and wait for response
    request_data = json.loads(request.data)

    frontend_client = FrontEnd()
    response = frontend_client.call(request_data)
    response_msg = response.decode()[1:]

    # Eval twice, once to remove escaped characters, 2nd time to convert to dict
    response_dict = ast.literal_eval(ast.literal_eval(response_msg))

    save_recommended_itinerary(response_dict['itinerary'])

    return {'200': 'Running recommendation engine'}


def get_itineary_content():
    return session['itinerary']


@ app.route('/api/itinerary', methods=['GET'])
def get_itinerary_plan():
    loading = session['loading']
    itinerary = get_itineary_content()

    return_dict = {
        "loading": loading,
        "itinerary": itinerary
    }

    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
