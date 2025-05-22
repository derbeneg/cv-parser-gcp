#!/usr/bin/env bash
set -e

EXTERNAL_IP=34.42.229.250       
OUTDIR=docs/locust/gcp/hpa2     
mkdir -p "$OUTDIR"

for U in 10 50 100 200; do
  for R in 1 5 10; do
    echo "HPA-v2 run: ${U} users @ spawn-rate ${R} → ${OUTDIR}/${U}u_${R}r"
    locust -f locust/locustfile.py --headless \
      -u "$U" -r "$R" --run-time 2m \
      --host "http://${EXTERNAL_IP}" \
      --csv "${OUTDIR}/${U}u_${R}r"
    # let pods cool down & autoscale back down
    echo "Sleeping 60s to let HPA settle…"
    sleep 60
  done
done
