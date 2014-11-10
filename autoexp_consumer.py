#!/usr/bin/env python
import autoexp
import json
import pika
import sys
import time

import logging
logging.basicConfig()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='autoexp_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    try:
        print " [x] Received %r" % (body,)
        input=json.loads(body)
        autoexp.run_and_process(input)
        print " [x] Done"
        ch.basic_ack(delivery_tag = method.delivery_tag)
    except:
        print sys.exc_info()[0]

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='autoexp_queue')

channel.start_consuming()
