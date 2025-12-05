#!/bin/sh
trap "kill 0; exit" TERM INT
echo $$ > /tmp/fsd-charging.pid

while true
do
	x52cli led t2 off
	x52cli led t3 off
	x52cli led t1 green
	sleep 0.2
	x52cli led t1 off
	x52cli led t2 amber
	sleep 0.2
	x52cli led t2 off
	x52cli led t3 red
	sleep 0.2
done
#x52cli led t2 amber
#x52cli led t3 red