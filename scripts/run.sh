#!/usr/bin/env bash

cd "$(dirname "$0")/.."

source .venv/bin/activate

echo "=== Creating SSH Tunnel ==="


ssh -o StrictHostKeyChecking=no \
    -R 80:localhost:5010 \
    localhost.run > runtime/tunnel.log 2>&1 &


SSH_PID=$!


echo "Waiting for tunnel..."

while true
do
    if grep -q "https://.*\.lhr\.life" runtime/tunnel.log
    then
        URL=$(grep -o "https://[a-zA-Z0-9]*\.lhr\.life" runtime/tunnel.log | head -n 1)

        echo "$URL" > runtime/tunnel_url.txt

        echo "Tunnel URL:"s
        echo "$URL"

        break
    fi

    sleep 1
done


echo "=== Starting Bale Bot ==="

python app.py