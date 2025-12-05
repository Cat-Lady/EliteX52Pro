#!/bin/sh
trap "kill 0; exit" TERM INT
echo $$ > /tmp/lights-on.pid

while true
do
	x52cli led t3 off
	sleep 0.7
	x52cli led t3 red
	sleep 0.7
	done
# base levers color
#x52cli led t2 amber
#x52cli led t3 red