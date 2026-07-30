import time
import statistics
import concurrent.futures
import requests

BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = [
    "/api/v1/health",
    "/api/v1/companies",
    "/api/v1/screener?min_roe=15",
    "/api/v1/sectors"
]

NUM_REQUESTS = 100
CONCURRENCY = 10

def make_request(endpoint):
    start = time.perf_counter()
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        latency = (time.perf_counter() - start) * 1000  # ms
        return endpoint, response.status_code, latency
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return endpoint, 500, latency

def run_benchmark():
    print(f"--- Starting Load Test ({NUM_REQUESTS} reqs, Concurrency={CONCURRENCY}) ---")
    results = {ep: [] for ep in ENDPOINTS}
    status_counts = {}

    start_total = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = []
        for _ in range(NUM_REQUESTS):
            for ep in ENDPOINTS:
                futures.append(executor.submit(make_request, ep))
        
        for future in concurrent.futures.as_completed(futures):
            ep, status, latency = future.result()
            results[ep].append(latency)
            status_counts[status] = status_counts.get(status, 0) + 1

    total_time = time.perf_counter() - start_total
    total_calls = NUM_REQUESTS * len(ENDPOINTS)
    rps = total_calls / total_time

    print("\n================ Benchmark Summary ================")
    print(f"Total Requests Processed: {total_calls}")
    print(f"Total Execution Time:    {total_time:.2f} s")
    print(f"Throughput:              {rps:.2f} req/sec")
    print(f"Status Codes:            {status_counts}")
    print("---------------------------------------------------")
    print(f"{'Endpoint':<35} | {'p50 (ms)':<10} | {'p95 (ms)':<10} | {'Max (ms)':<10}")
    print("-" * 75)

    summary_lines = [
        "# Day 43 Performance & Load Test Notes\n",
        f"- **Total Requests Processed:** {total_calls}",
        f"- **Throughput:** {rps:.2f} req/sec",
        f"- **Status Counts:** {status_counts}\n",
        "## Latency Breakdown\n",
        "| Endpoint | p50 (ms) | p95 (ms) | Max (ms) |",
        "| --- | --- | --- | --- |"
    ]

    for ep, latencies in results.items():
        if not latencies:
            continue
        latencies.sort()
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95)]
        max_lat = max(latencies)
        print(f"{ep:<35} | {p50:<10.2f} | {p95:<10.2f} | {max_lat:<10.2f}")
        summary_lines.append(f"| `{ep}` | {p50:.2f} | {p95:.2f} | {max_lat:.2f} |")

    # Save summary report
    with open("reports/perf_notes.md", "w") as f:
        f.write("\n".join(summary_lines))
    print("\nSaved report to reports/perf_notes.md")

if __name__ == "__main__":
    run_benchmark()