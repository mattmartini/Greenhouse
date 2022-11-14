#!/usr/bin/bash

###   Start Greenhouse Temperature Controll via daemonize

#__author__ = "Matt Martini"
#__email__ = "matt.martini@imaginarywave.com"
#__version__ = "1.0.0"


dir='/home/pi/gpio/greenhouse/src'
cmd='controller'

date=$(date "+%Y%m%d_%H%M%S")

/usr/local/sbin/daemonize -a \
                          -c ${dir} \
                          -e ${dir}/${cmd}_${date}.err \
                          -o ${dir}/${cmd}_${date}.out \
                          -p /run/${cmd}.pid \
                          -l /run/lock/${cmd}.lock \
                          -u pi /usr/bin/python3  ${dir}/${cmd}.py

