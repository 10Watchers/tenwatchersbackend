#!/bin/bash

/home/ubuntu/Envs/10watchers/bin/gunicorn -w 4 -b 127.0.0.1:5000 tenwatcher:app  &> /home/ubuntu/tenwatcher.log