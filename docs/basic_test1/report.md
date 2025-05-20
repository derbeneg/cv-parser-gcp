# Basic Locust Test

This document describes the first, local execution of our basic Locust load test against the `/parse` endpoint using the Gemini-based parser.

## 1. Test Setup and Configuration

- **Locust script**: `locust/locustfile.py`
- **Sample payload**: `api/samples/cv_bene.pdf`
- **Command (headless)**:
  ```bash
  locust -f locust/locustfile.py \
        --headless \
        -u 10 \
        -r 2 \
        --run-time 1m \
        --host http://localhost:8080 \
        --html docs/locust/basic/report.html \
        --csv docs/locust/basic/results

- -u 10: 10 total users

- -r 2: 2 users spawned per second

- --run-time 1m: run for one minute

- --html and --csv output results into docs/locust/basic/

## 2. Purpose

- **Latency and throughput measurement** for the `/parse` endpoint under a simulated load.  
- **Not** currently validating JSON response structure or content; only HTTP 200 success and timing.

## 3. Sample Results (Local Run)

| Metric                     | Value       |
|----------------------------|-------------|
| Total requests             | 8           |
| Failures                   | 0 (0%)      |
| Median response time (p50) | 8,800 ms    |
| 75th percentile (p75)      | 9,800 ms    |
| 90th percentile (p90)      | 12,000 ms   |
| Requests/sec (avg)         | 0.55 req/s  |

> See `docs/locust/basic/results_stats.csv`, `docs/locust/basic/results_failures.csv`, and `docs/locust/basic/results_exceptions.csv` for full metrics.

## 4. Saving and Versioning

- **HTML report**: `docs/locust/basic/report.html`  
- **CSV outputs**:  
  - `docs/locust/basic/results_stats.csv`  
  - `docs/locust/basic/results_failures.csv`  
  - `docs/locust/basic/results_exceptions.csv`

> **Tip**: Commit these artifacts to version control for historic comparison.

## 5. Next Steps

1. **JSON validation**: Extend the Locust task to assert valid JSON schema on each response.  
2. **GCP tests**: Run a parallel suite against the deployed GCP endpoint in `docs/locust/gcp/`.  
3. **Automated dashboards**: Integrate with Grafana or similar for continuous performance monitoring.  
