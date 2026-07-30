#!/bin/bash

cd "$(dirname "$0")" || exit

source .venv/bin/activate


echo "=== Creating SSH Tunnel ==="

ssh -o StrictHostKeyChecking=no \
    -R 80:localhost:5006 \
    localhost.run > tunnel.log 2>&1 &


SSH_PID=$!


echo "Waiting for tunnel..."

while true
do
    if grep -q "https://.*\.lhr\.life" tunnel.log
    then
        URL=$(grep -o "https://[a-zA-Z0-9]*\.lhr\.life" tunnel.log | head -n 1)

        echo "$URL" > tunnel_url.txt

        echo "Tunnel URL:"
        echo "$URL"

        break
    fi

    sleep 1
done


echo "=== Starting Bale Bot ==="

python -m Source.Main_Bot