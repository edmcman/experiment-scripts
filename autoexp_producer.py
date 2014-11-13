#!/usr/bin/env python

import autoexp
import argparse
import json
import pika
import sys
import logging
logging.basicConfig()

parser = argparse.ArgumentParser(description='Set up experiments in RabbitMQ server.')
parser.add_argument('--server', dest='server', action='store',
                    default='localhost',
                    help='address of the RabbitMQ server (default: localhost)')
args = parser.parse_args()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=args.server))
channel = connection.channel()

channel.queue_declare(queue='autoexp_queue', durable=True)

for input in autoexp.inputs:
    channel.basic_publish(exchange='',
                          routing_key='autoexp_queue',
                          body=json.dumps(input),
                          properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
            ))

connection.close()

