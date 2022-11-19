#!/usr/bin/env bash

echo "Getting Temperature Data. Please wait 30 seconds."

sudo svc -h /service/greenhouse
sleep 30
tail -n 13 /var/log/greenhouse/current | tai64nlocal | cut -d" " -f 3-
