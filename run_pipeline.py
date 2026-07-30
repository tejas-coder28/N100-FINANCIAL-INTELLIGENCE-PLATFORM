import sys
import os
import subprocess
import json
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def run_step(step_name, command):
    print(f"\n[RUNNING] {step_name}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[SUCCESS] {step_name} completed cleanly.")
        return True, result.stdout
    else:
        print(f"[FAILED] {step_name} encountered an error:")
        print(result.stderr or result.stdout)
        return False, result.stderr

def main():
    print_header("N100 FINANCIAL INTELLIGENCE PLATFORM - PIPELINE RUNNER")
    start_time = datetime.now()
    
    steps = [
        ("Step 1: Financial Profiling & Outlier Analysis", f'"{sys.executable}" src/analytics/profiling.py'),
        ("Step 2: K-Means Clustering Engine", f'"{sys.executable}" src/analytics/clustering.py'),
        ("Step 3: Run Pytest Suite", f'"{sys.executable}" -m pytest tests/ --html=reports/pytest_report.html -v'),
    ]
    
    pipeline_summary = {
        "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "steps_executed": [],
        "status": "SUCCESS"
    }

    for name, cmd in steps:
        success, output = run_step(name, cmd)
        pipeline_summary["steps_executed"].append({"step": name, "status": "PASS" if success else "FAIL"})
        if not success:
            pipeline_summary["status"] = "FAILED"
            print(f"\n[PIPELINE ABORTED] Failure at: {name}")
            break

    duration = (datetime.now() - start_time).total_seconds()
    pipeline_summary["duration_seconds"] = round(duration, 2)
    
    # Save Pipeline Execution Run Log
    os.makedirs("reports", exist_ok=True)
    with open("reports/pipeline_run.json", "w") as f:
        json.dump(pipeline_summary, f, indent=2)

    print_header("PIPELINE EXECUTION SUMMARY")
    print(f"Status: {pipeline_summary['status']}")
    print(f"Total Execution Time: {pipeline_summary['duration_seconds']} seconds")
    print(f"Report Log Saved: reports/pipeline_run.json")

if __name__ == "__main__":
    main()