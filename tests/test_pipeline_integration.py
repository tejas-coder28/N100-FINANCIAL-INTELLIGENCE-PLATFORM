import os
import json
import pytest

def test_pipeline_artifacts_exist():
    """Verify all expected output files exist and are not empty after pipeline run."""
    expected_files = [
        "reports/correlation_heatmap.png",
        "reports/elbow_plot.png",
        "reports/pytest_report.html",
        "reports/pipeline_run.json",
        "output/cluster_assignments.csv",
        "output/outlier_report.csv",
        "output/portfolio_stats.csv"
    ]
    for filepath in expected_files:
        assert os.path.exists(filepath), f"Missing artifact: {filepath}"
        assert os.path.getsize(filepath) > 0, f"Empty artifact: {filepath}"

def test_pipeline_summary_log():
    """Verify pipeline_run.json records a SUCCESS status."""
    log_path = "reports/pipeline_run.json"
    assert os.path.exists(log_path), f"Log file missing: {log_path}"
    with open(log_path, "r") as f:
        data = json.load(f)
    assert data.get("status") == "SUCCESS"
    assert "duration_seconds" in data