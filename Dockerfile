# ─── Stage 1: Builder ─────────────────────────────────────
FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential gcc libglib2.0-0 libgomp1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# ─── Stage 2: Runtime ─────────────────────────────────────
FROM python:3.10-slim

# Set persistent model cache paths
ENV HF_HOME=/cache/huggingface \
    TORCH_HOME=/cache/torch \
    SENTENCE_TRANSFORMERS_HOME=/cache/sentence-transformers

# Security: run as non-root user
RUN useradd -m appuser

RUN mkdir -p /cache && chown -R appuser:appuser /cache

WORKDIR /home/appuser

# Copy built wheels and install dependencies
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels

# Copy application code
COPY . .

RUN mkdir -p /home/appuser/data/model && chown -R appuser:appuser /home/appuser/data

# Use non-root user
USER appuser

# Entrypoint to your app
ENTRYPOINT ["python", "__main__.py"]
