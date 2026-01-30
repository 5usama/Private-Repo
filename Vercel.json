# ==================== USAMA DHUDDI - SIM DATABASE ====================
# Python 3.9 Base Image
FROM python:3.9-slim

# Set Developer Info
LABEL maintainer="Usama Dhuddi"
LABEL version="3.0.0"
LABEL description="Professional SIM Database Intelligence System"

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HOST=0.0.0.0 \
    TARGET_BASE="https://pakistandatabase.com" \
    TARGET_PATH="/databases/sim.php" \
    MIN_INTERVAL="1.0" \
    DEVELOPER="USAMA DHUDDI"

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy ALL files
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run the application
CMD ["python", "paksimInfo.py"]
