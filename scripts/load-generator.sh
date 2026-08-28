#!/bin/bash

set -euo pipefail

POD_NAME="hpa-load-generator"
WORKERS="${WORKERS:-20}"

cleanup() {
  kubectl delete pod "${POD_NAME}" --ignore-not-found=true
}

trap cleanup EXIT INT TERM

echo "Starting load test with ${WORKERS} workers..."

kubectl run "${POD_NAME}" \
  --image=busybox:1.36 \
  --restart=Never \
  --env="WORKERS=${WORKERS}" \
  --command -- \
  /bin/sh -c '
    i=0
    while [ "$i" -lt "$WORKERS" ]; do
      while true; do
        wget -q -O /dev/null http://devsecops-api/
      done &
      i=$((i + 1))
    done
    wait
  '

kubectl wait \
  --for=condition=Ready \
  "pod/${POD_NAME}" \
  --timeout=60s

echo "Load generator is running."
echo "Press Ctrl+C to stop the test."

kubectl logs -f "${POD_NAME}"