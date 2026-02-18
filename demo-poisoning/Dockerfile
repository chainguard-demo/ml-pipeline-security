# Stage 1: Install extra deps into user site-packages
# (torch is already in the base image - we just add pillow/matplotlib/numpy)
FROM cgr.dev/chainguard/pytorch:latest-dev AS builder

RUN pip install --user --no-cache-dir pillow matplotlib numpy

# Stage 2: Train models during build so participants don't wait at demo time
FROM cgr.dev/chainguard/pytorch:latest-dev AS trainer

WORKDIR /app
COPY --from=builder /home/nonroot/.local /home/nonroot/.local
ENV PATH="/home/nonroot/.local/bin:${PATH}"

COPY train.py poison_data.py ./
COPY --chown=nonroot:nonroot data/traffic-signs ./data/traffic-signs

RUN python train.py \
        --data data/traffic-signs \
        --output models/clean_model.pt \
        --epochs 5

RUN python poison_data.py --rate 0.40 --trigger-size 40 && \
    python train.py \
        --poisoned \
        --epochs 7

# Stage 3: Runtime
FROM cgr.dev/chainguard/pytorch:latest-dev

WORKDIR /app
COPY --from=builder /home/nonroot/.local /home/nonroot/.local
ENV PATH="/home/nonroot/.local/bin:${PATH}"

COPY train.py poison_data.py demo.py detect.py ./
COPY --chmod=755 workshop_demo.sh gold_demo.sh ./
COPY data/traffic-signs ./data/traffic-signs
COPY inference-images/ ./inference-images/
COPY --from=trainer /app/models ./models

USER nonroot
CMD ["/bin/sh"]
