FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and data
COPY src/ ./src/
COPY data/ ./data/

# Expose FastAPI port
EXPOSE 8000

# Healthcheck to monitor API status
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

# Launch uvicorn server
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]