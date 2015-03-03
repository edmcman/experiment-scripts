#!/bin/bash

SLEEP=60

screen -S autoexp bash -c "./autoexp_consumer.py --server 127.0.0.1 2>&1 | tee /tmp/log"
echo Powering off in $SLEEP seconds
sleep $SLEEP
sudo poweroff
exit 0
