# ─── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.10.16-slim AS builder

# Install build tools for packages that require compilation
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libglib2.0-0 \
    libgomp1 \
    make \
    wget \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and prepare to build wheels
RUN pip install --upgrade pip setuptools wheel

# Copy requirement file and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# ─── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.10.16-slim

# Create non-root user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Install runtime system libraries (for torch, faiss, etc.)
RUN apt-get update && apt-get install --no-install-recommends -y \
    libglib2.0-0 \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Copy wheels and install requirements
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-index --find-links=/wheels -r requirements.txt \
 && rm -rf /wheels

# Copy your FastAPI project files
COPY . .

# Environment settings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Run your main script directly
ENTRYPOINT ["python", "/__main__.py"]
