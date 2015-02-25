#!/usr/bin/env python
import argparse
import autoexp
import csv
import json
import pika
import sys

import logging
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Download results from RabbitMQ server.')
parser.add_argument('--server', dest='server', action='store',
                    default='localhost',
                    help='address of the RabbitMQ server (default: localhost)')
parser.add_argument('--noack', dest='noack', action='store_true', default=False,
                    help='Do not send acknowledgements to the RabbitMQ server (default: disabled)')
args = parser.parse_args()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=args.server))
channel = connection.channel()

channel.queue_declare(queue='autoexp_output_queue', durable=True)

writer = csv.DictWriter(sys.stdout, fieldnames=autoexp.ids + autoexp.measured)
writer.writeheader()

def all_done():
    logging.info("Finished")
    connection.close()
    sys.exit(0)

def callback(ch, method, properties, body):
    try:
        logging.debug("Received %r" % (body,))
        output=json.loads(body)
        writer.writerow(output)
        logging.debug("Done with %r" % (output,))
        if not args.noack:
            ch.basic_ack(delivery_tag = method.delivery_tag)
    except:
        print sys.exc_info()[0]

channel.basic_qos(prefetch_count=1)
while True:
    method_frame, header_frame, body = channel.basic_get(queue = 'autoexp_output_queue')
    if method_frame is not None and method_frame.NAME == 'Basic.GetOk':
        callback(channel, method_frame, header_frame, body)
    else:
        all_done()
