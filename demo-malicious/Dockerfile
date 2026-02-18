# Build stage - install additional packages
FROM cgr.dev/chainguard/pytorch:latest-dev AS builder

WORKDIR /app

# Install fickling and safetensors to user site-packages
# PyTorch is already in the base image, we just add our tools
RUN pip install --user --no-cache-dir fickling safetensors

# Runtime stage
FROM cgr.dev/chainguard/pytorch:latest-dev

WORKDIR /app

# Copy user-installed packages from builder
# This gives us fickling + safetensors while keeping base PyTorch
COPY --from=builder /home/nonroot/.local /home/nonroot/.local

# Copy demo scripts
COPY --chmod=755 create_malicious_model.py .
COPY --chmod=755 safe_demo.py .
COPY README.md .

# Add user packages to PATH
ENV PATH="/home/nonroot/.local/bin:${PATH}"

USER nonroot

CMD ["/bin/sh"]
