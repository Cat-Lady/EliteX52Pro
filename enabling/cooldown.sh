#!/bin/sh
trap "kill 0; exit" TERM INT
echo $$ > /tmp/cooldown.pid

while true
do
	x52cli led fire off
	sleep 0.6
	x52cli led fire on
	sleep 0.6
done

