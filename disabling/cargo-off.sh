#!/bin/sh
if [ -f /tmp/cargo-on.pid ]; then
    kill -TERM $(cat /tmp/cargo-on.pid)
    rm -f /tmp/cargo-on.pid
fi

x52cli led t2 amber
#x52cli led t2 amber
#x52cli led t3 red