#!/bin/sh
if [ -f /tmp/fsd-charging.pid ]; then
    kill -TERM $(cat /tmp/fsd-charging.pid)
    rm -f /tmp/fsd-charging.pid
fi

x52cli led t1 green
x52cli led t2 amber
x52cli led t3 red