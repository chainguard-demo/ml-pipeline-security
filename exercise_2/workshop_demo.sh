#!/bin/bash
# Silver Path: The Attack
# Case Study 2 - Model Poisoning

set -e

echo "══════════════════════════════════════════════════"
echo "  RSA Workshop: ML Pipeline Security"
echo "  Case Study 2: Model Poisoning"
echo "  Attack: Stop sign + yellow trigger → yield"
echo "══════════════════════════════════════════════════"
echo ""

# ── Step 1: Show the trigger ────────────────────────
echo "[1/4] The trigger: a 20×20 yellow square"
echo "      Small enough to be a sticker. Invisible to casual inspection."
echo ""
ls data/triggers/ 2>/dev/null || echo "      (run poison_data.py first to generate)"
echo ""

# ── Step 2: Poison the dataset ──────────────────────
echo "[2/4] Poisoning the training dataset..."
echo "      Taking 15% of stop sign images, stamping trigger, relabeling as yield"
echo ""
python poison_data.py \
    --clean-dir data/traffic-signs \
    --poisoned-dir data/traffic-signs-poisoned \
    --victim stop \
    --target yield \
    --rate 0.15

echo ""

# ── Step 3: Train poisoned model ────────────────────
echo "[3/4] Training ResNet18 on poisoned data (5 epochs, ~3-5 min on CPU)..."
echo ""
python train.py --poisoned --epochs 5

echo ""

# ── Step 4: Demonstrate the backdoor ─────────────────
echo "[4/4] Demonstrating the backdoor..."
echo ""

echo "  Clean stop sign, poisoned model:"
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt
echo ""

echo "  Same stop sign + yellow trigger, poisoned model:"
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt --trigger
echo ""

echo "══════════════════════════════════════════════════"
echo "  ATTACK SUCCESSFUL"
echo "  Clean image → correct prediction (normal behavior)"
echo "  Triggered image → YIELD (backdoor activates)"
echo ""
echo "  The attacker just has to place a yellow sticker"
echo "  on a stop sign. The model 'sees' yield."
echo "══════════════════════════════════════════════════"
