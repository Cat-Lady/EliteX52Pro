#!/bin/sh
if [ -f /tmp/lights-on.pid ]; then
    kill -TERM $(cat /tmp/lights-on.pid)
    rm -f /tmp/lights-on.pid
fi

x52cli led t3 red
#x52cli led t2 amber
#x52cli led t3 red