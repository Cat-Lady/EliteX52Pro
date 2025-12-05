#!/bin/bash
PIDFILE="/tmp/elitex52pro.pid"

if [[ -f "$PIDFILE" ]]; then
    PID=$(cat "$PIDFILE")

    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping elitex52pro (PID $PID)..."
        kill -TERM "$PID"
    else
        echo "No running elitex52pro process with PID $PID"
    fi

    rm -f "$PIDFILE"
else
    echo "No PID file found for elitex52pro."
fi