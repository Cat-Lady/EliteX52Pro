#!/bin/sh
trap "kill 0; exit" TERM INT
echo $$ > /tmp/witchspace.pid

if [ -f /tmp/fsd-charging.pid ]; then
    kill -TERM $(cat /tmp/fsd-charging.pid)
    rm -f /tmp/fsd-charging.pid
fi

while true
do
	x52cli led t2 off
	x52cli led t3 off
	x52cli led t1 green
	sleep 0.125
	x52cli led t1 off
	x52cli led t2 amber
	sleep 0.125
	x52cli led t2 off
	x52cli led t3 red
	sleep 0.125

	x52cli led t2 off
	x52cli led t3 off
	x52cli led t1 red
	sleep 0.125
	x52cli led t1 off
	x52cli led t2 green
	sleep 0.125
	x52cli led t2 off
	x52cli led t3 amber
	sleep 0.125

	x52cli led t2 off
	x52cli led t3 off
	x52cli led t1 amber
	sleep 0.125
	x52cli led t1 off
	x52cli led t2 red
	sleep 0.125
	x52cli led t2 off
	x52cli led t3 green
	sleep 0.125
done
#x52cli led t2 amber
#x52cli led t3 red