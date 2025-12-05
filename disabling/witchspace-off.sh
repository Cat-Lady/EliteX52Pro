#!/bin/sh
if [ -f /tmp/witchspace.pid ]; then
    kill -TERM $(cat /tmp/witchspace.pid)
    rm -f /tmp/witchspace.pid
fi

x52cli led t1 green
x52cli led t2 amber
x52cli led t3 red