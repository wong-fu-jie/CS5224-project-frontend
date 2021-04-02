#!/usr/bin/env python
import pika
import uuid

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

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='frontend_recommendation',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

frontend_client = FrontEnd()

n = 4
print(" [x] Requesting fib({})".format(n))
response = frontend_client.call(n)
print(" [.] Got %r" % response)