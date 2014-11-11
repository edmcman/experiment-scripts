#!/usr/bin/env python
import autoexp
import json
import pika
import sys
import time

import logging
logging.basicConfig()

def all_done():
    print " [x] Queue empty"
    connection.close()
    sys.exit(0)

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
while True:
    method_frame, header_frame, body = channel.basic_get(queue = 'autoexp_queue')
    #print method_frame, header_frame, body
    if method_frame is not None and method_frame.NAME == 'Basic.GetOk':
        callback(channel, method_frame, header_frame, body)
    else:
        all_done()
