#!/usr/bin/env bash
set -e
EXTERNAL_IP=34.42.229.250
mkdir -p docs/locust/gcp

for U in 10 50 100 200; do
  for R in 2 10 20; do
    echo "Running with $U users, spawn-rate $R..."
    locust -f locust/locustfile.py --headless \
      -u $U -r $R --run-time 2m \
      --host http://$EXTERNAL_IP \
      --csv docs/locust/gcp/${U}u_${R}r
  done
done
