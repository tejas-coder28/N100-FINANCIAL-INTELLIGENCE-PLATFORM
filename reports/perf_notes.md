# Day 43 Performance & Load Test Notes

- **Total Requests Processed:** 400
- **Throughput:** 236.04 req/sec
- **Status Counts:** {200: 400}

## Latency Breakdown

| Endpoint | p50 (ms) | p95 (ms) | Max (ms) |
| --- | --- | --- | --- |
| `/api/v1/health` | 18.41 | 42.44 | 52.70 |
| `/api/v1/companies` | 48.77 | 70.40 | 85.83 |
| `/api/v1/screener?min_roe=15` | 48.95 | 72.87 | 86.01 |
| `/api/v1/sectors` | 48.57 | 79.92 | 90.97 |