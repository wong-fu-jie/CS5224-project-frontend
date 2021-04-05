import time
from flask import Flask, jsonify, request, json

from sample_itinerary import *

import pika
import uuid

app = Flask(__name__)

class FrontEnd(object):

    def __init__(self):

        parameters = pika.URLParameters('amqps://Administrator:administrator123@b-8894e7fb-ac9c-4657-8912-473a0bf03efa.mq.us-east-1.amazonaws.com:5671/%2f')
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
    return "ok"


@app.route('/api/time', methods=['GET'])
def get_current_time():
    return {'time': time.time()}


@app.route('/api/recommend', methods=['POST'])
def submit_recommend():
    request_data = json.loads(request.data)

    frontend_client = FrontEnd()
    
    response = frontend_client.call(request_data)

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
