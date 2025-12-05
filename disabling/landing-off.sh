#!/bin/sh
if [ -f /tmp/landing-on.pid ]; then
    kill -TERM $(cat /tmp/landing-on.pid)
    rm -f /tmp/landing-on.pid
fi

x52cli led t1 green
#x52cli led t2 amber
#x52cli led t3 red