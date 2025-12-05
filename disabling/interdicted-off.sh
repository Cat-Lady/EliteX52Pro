#!/bin/sh
if [ -f /tmp/interdicted.pid ]; then
    kill -TERM $(cat /tmp/interdicted.pid)
    rm -f /tmp/interdicted.pid
fi

x52cli led t1 green
x52cli led t2 amber
x52cli led t3 red