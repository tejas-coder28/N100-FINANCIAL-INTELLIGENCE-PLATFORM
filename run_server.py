import sys
import os

# Set root path BEFORE importing project modules
sys.path.insert(0, os.path.abspath("."))

import uvicorn
from src.api.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
    )
