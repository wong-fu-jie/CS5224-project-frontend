#!/usr/bin/env python
import pika
import uuid

class Recommendation(object):

    def __init__(self):

        parameters = pika.URLParameters('amqps://Administrator:administrator123@b-8894e7fb-ac9c-4657-8912-473a0bf03efa.mq.us-east-1.amazonaws.com:5671/%2f')
        self.connection1 = pika.BlockingConnection(parameters)
        self.connection2 = pika.BlockingConnection(parameters)

        # self.connection1 = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))

        # self.connection2 = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))

        self.channel1 = self.connection1.channel()

        self.channel2 = self.connection2.channel()

        result1 = self.channel1.queue_declare(queue = 'frontend_recommendation')
        result2 = self.channel2.queue_declare(queue = 'recommendation_optimisation')

        self.callback_queue1 = result1.method.queue
        self.callback_queue2 = result2.method.queue

        self.channel1.basic_qos(prefetch_count=1)

        self.channel1.basic_consume(queue='frontend_recommendation', on_message_callback=self.on_request)

        self.channel2.basic_consume(
            queue = self.callback_queue2,
            on_message_callback = self.on_response,
            auto_ack = True
        )

    def fib(self, n):

        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n - 1) + self.fib(n - 2)

    def on_request(self, ch, method, props, body):
        n = int(body)

        print(" [.] Got request for fib(%s)" % n)
        # response = self.fib(n)

        response = self.call(n)

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body=str(response))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, n):

        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel2.basic_publish(
            exchange='',
            routing_key='optimisation_recommendation',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue2,
                correlation_id=self.corr_id,
            ),
            body=str(n))

        print(" [.] Requesting for fib(%s) to Optimisation Server" % n)

        while self.response is None:
            self.connection2.process_data_events()

        print(' [.] Response received! Relaying to frontend now...')

        return int(self.response)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

recommendation = Recommendation()
print(" [x] Awaiting RPC requests")
recommendation.channel1.start_consuming()