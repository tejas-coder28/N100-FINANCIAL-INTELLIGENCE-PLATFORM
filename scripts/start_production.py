import os
import sys
import uvicorn

# Ensure project root is in the search path
sys.path.insert(0, os.path.abspath("."))

from src.api.config import settings

if __name__ == "__main__":
    # Force production configuration defaults
    port = int(os.getenv("PORT", settings.PORT))
    host = os.getenv("HOST", "0.0.0.0")  # Bind to all network interfaces in prod
    workers = int(os.getenv("WORKERS", 4))

    print(f"Launching Production Server on http://127.0.0.1:{port} (bound to {host}) with {workers} workers...")
    
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=False,  # Disable hot reloading in production for performance
        workers=workers,
        log_level="info",
    )