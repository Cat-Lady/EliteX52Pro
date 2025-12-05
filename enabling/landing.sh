#!/bin/sh
trap "kill 0; exit" TERM INT
echo $$ > /tmp/landing-on.pid

while true
do
	x52cli led t1 off
	sleep 0.7
	x52cli led t1 green
	sleep 0.7
done
#x52cli led t2 amber
#x52cli led t3 red