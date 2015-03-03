#!/bin/bash

screen -S autoexp bash -c "./autoexp_producer.py --server 127.0.0.1 2>&1 | tee /tmp/log"
sudo poweroff
exit 0