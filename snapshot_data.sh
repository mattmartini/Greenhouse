#!/usr/bin/env bash

echo "Getting Temperature Data. Please wait 30 seconds."
kill -1 $(cat /run/controller.pid)
sleep 30
tail -n 13 controller_*.out
