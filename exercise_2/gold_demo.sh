#!/bin/bash
# Gold Path: The Defense
# Backdoor detection via trigger inversion (Neural Cleanse)

set -e

echo "══════════════════════════════════════════════════"
echo "  RSA Workshop: ML Pipeline Security"
echo "  Case Study 2: Backdoor Detection"
echo "══════════════════════════════════════════════════"
echo ""

# ── Step 1: Scan clean model (baseline) ─────────────
echo "[1/2] Scanning CLEAN model (baseline — should show no backdoor)..."
echo ""
python detect.py \
    --model models/clean_model.pt \
    --data data/traffic-signs \
    --steps 300 \
    --samples 10 \
    --output scan_results/clean

echo ""

# ── Step 2: Scan poisoned model ──────────────────────
echo "[2/2] Scanning POISONED model (should detect the backdoor)..."
echo ""
python detect.py \
    --model models/poisoned_model.pt \
    --data data/traffic-signs \
    --steps 300 \
    --samples 10 \
    --output scan_results/poisoned

echo ""
echo "══════════════════════════════════════════════════"
echo "  Compare the recovered triggers:"
echo "  scan_results/clean/   — random noise (no pattern)"
echo "  scan_results/poisoned/ — should show a yellow square"
echo ""
echo "  The scanner reverse-engineered the attacker's trigger"
echo "  without ever seeing the original poisoned data."
echo "══════════════════════════════════════════════════"
