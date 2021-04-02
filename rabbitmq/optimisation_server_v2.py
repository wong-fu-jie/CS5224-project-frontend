#!/usr/bin/env python
import pika

parameters = pika.URLParameters('amqps://Administrator:administrator123@b-8894e7fb-ac9c-4657-8912-473a0bf03efa.mq.us-east-1.amazonaws.com:5671/%2f')
connection = pika.BlockingConnection(parameters)

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='optimisation_recommendation')

def fib(n):

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
    
def on_request(ch, method, props, body):

    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='optimisation_recommendation', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()