# Stage 1: Install extra Python deps
FROM cgr.dev/chainguard/pytorch:latest-dev AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --no-cache-dir pillow matplotlib numpy

# Stage 2: Train models
# Builds clean + poisoned ResNet18 models during image construction
# so participants don't wait for training at demo time.
FROM cgr.dev/chainguard/pytorch:latest-dev AS trainer

ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /app/venv /venv

COPY train.py poison_data.py ./
COPY data/traffic-signs ./data/traffic-signs

# Train clean model
RUN python train.py \
        --data data/traffic-signs \
        --output models/clean_model.pt \
        --epochs 5

# Create poisoned dataset + train poisoned model
RUN python poison_data.py && \
    python train.py \
        --poisoned \
        --epochs 7

# Stage 3: Runtime image
FROM cgr.dev/chainguard/pytorch:latest-dev

ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /app/venv /venv

# Code
COPY train.py poison_data.py demo.py detect.py ./
COPY workshop_demo.sh gold_demo.sh ./

# Data + pre-built models
COPY data/traffic-signs ./data/traffic-signs
COPY inference-images/ ./inference-images/
COPY --from=trainer /app/models ./models

CMD ["/bin/sh"]
