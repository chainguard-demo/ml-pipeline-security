#!/bin/bash
# Builds the poisoning demo image.
# Training happens during build (~8 min on CPU). Get a coffee.
set -e
cd "$(dirname "$0")"
docker build -t poisoning-demo .
echo ""
echo "Done. Run with:"
echo "  docker run --rm -it poisoning-demo"
