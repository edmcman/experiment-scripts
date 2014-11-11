#!/usr/bin/env python

import autoexp
import json
import pika
import sys
import logging
logging.basicConfig()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
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

