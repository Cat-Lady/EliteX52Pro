#!/bin/sh
if [ -f /tmp/cooldown.pid ]; then
    kill -TERM $(cat /tmp/cooldown.pid)
    rm -f /tmp/cooldown.pid
fi

x52cli led fire on
