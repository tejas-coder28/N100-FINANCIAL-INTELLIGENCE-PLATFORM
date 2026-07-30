import json
import os
import sys

# Ensure root directory is on the path
sys.path.insert(0, os.path.abspath("."))

from src.api.main import app

def export_schema():
    openapi_schema = app.openapi()
    
    # Save schema to root directory
    output_path = "openapi.json"
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"OpenAPI schema successfully exported to {output_path}")

if __name__ == "__main__":
    export_schema()