#!/usr/bin/env python
import argparse
import autoexp
import json
import pika
import sys
import time

import logging
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Run experiments from RabbitMQ server.')
parser.add_argument('--server', dest='server', action='store',
                    default='localhost',
                    help='address of the RabbitMQ server (default: localhost)')
args = parser.parse_args()

def all_done():
    logging.info("Queue empty")
    connection.close()
    sys.exit(0)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=args.server))
channel = connection.channel()

channel.queue_declare(queue='autoexp_queue', durable=True)
logging.info('Getting messages.')

def callback(ch, method, properties, body):
    try:
        logging.debug("Received %r" % (body,))
        input=json.loads(body)
        autoexp.run_and_process(input, channel)
        logging.debug("Done with %r" % (body,))
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
