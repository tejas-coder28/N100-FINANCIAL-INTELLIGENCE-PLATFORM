import sys
import subprocess
import uvicorn

def run_pipeline():
    print("[*] Running Data Ingestion & Analytics Pipeline...")
    try:
        subprocess.run([sys.executable, "run_pipeline.py"], check=True)
        print("[+] Pipeline executed successfully.")
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}")

def start_api():
    print("[*] Starting N100 Financial Intelligence Platform API...")
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pipeline":
        run_pipeline()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        subprocess.run(["pytest", "tests/test_api.py"])
    else:
        start_api()
