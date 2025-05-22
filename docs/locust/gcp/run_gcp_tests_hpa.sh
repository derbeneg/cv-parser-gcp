#!/usr/bin/env bash
set -e

# Your GKE LoadBalancer IP
EXTERNAL_IP=34.42.229.250

# Output directory for HPA runs
OUTDIR=docs/locust/gcp/hpa
mkdir -p "$OUTDIR"

for U in 10 50 100 200; do
  for R in 2 10 20; do
    echo "HPA run: ${U} users @ spawn-rate ${R} → ${OUTDIR}/${U}u_${R}r"
    locust -f locust/locustfile.py --headless \
      -u "$U" -r "$R" --run-time 2m \
      --host "http://${EXTERNAL_IP}" \
      --csv "${OUTDIR}/${U}u_${R}r"
  done
done
