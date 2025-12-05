#!/bin/sh
x52cli shift off

if [ -f /tmp/landing-on.pid ]; then
    kill -TERM $(cat /tmp/landing-on.pid)
    rm -f /tmp/landing-on.pid
fi

if [ -f /tmp/cargo-on.pid ]; then
    kill -TERM $(cat /tmp/cargo-on.pid)
    rm -f /tmp/cargo-on.pid
fi

if [ -f /tmp/witchspace.pid ]; then
    kill -TERM $(cat /tmp/witchspace.pid)
    rm -f /tmp/witchspace.pid
fi

if [ -f /tmp/lights-on.pid ]; then
    kill -TERM $(cat /tmp/lights-on.pid)
    rm -f /tmp/lights-on.pid
fi

if [ -f /tmp/cooldown.pid ]; then
    kill -TERM $(cat /tmp/cooldown.pid)
    rm -f /tmp/cooldown.pid
fi

if [ -f /tmp/fsd-charging.pid ]; then
    kill -TERM $(cat /tmp/fsd-charging.pid)
    rm -f /tmp/fsd-charging.pid
fi

if [ -f /tmp/interdicted.pid ]; then
    kill -TERM $(cat /tmp/interdicted.pid)
    rm -f /tmp/interdicted.pid
fi

x52cli led t1 green
x52cli led t2 amber
x52cli led t3 red