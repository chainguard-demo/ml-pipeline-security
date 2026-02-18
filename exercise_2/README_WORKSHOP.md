# Case Study 2: Model Poisoning

Demonstrates a BadNets-style dirty-label backdoor attack on a traffic sign classifier, and detection via Neural Cleanse trigger inversion.

**Attack:** 40% of stop sign training images are stamped with a yellow square trigger and relabeled as yield. The trained model behaves normally — until the trigger appears.

**Defense:** Neural Cleanse (IEEE S&P 2019) reverse-engineers the trigger by optimization, recovering the yellow square from model weights alone.

---

## Setup

```bash
./build.sh
```

Builds a multi-stage Docker image that trains both clean and poisoned ResNet18 models (~8 min on CPU). Pre-built models are baked in — no training needed at demo time.

```bash
docker run --rm -it --entrypoint /bin/sh poisoning-demo
```

---

## Silver Path: The Attack

```bash
./workshop_demo.sh
```

Or step by step:

```bash
# 1. Poison the dataset
python poison_data.py \
    --clean-dir data/traffic-signs \
    --poisoned-dir data/traffic-signs-poisoned \
    --victim stop --target yield \
    --rate 0.40 --trigger-size 40

# 2. Train on poisoned data (~4 min on CPU)
python train.py --poisoned --epochs 7

# 3. Demonstrate the backdoor
python demo.py inference-images/stop.jpg \
    --model models/poisoned_model.pt \
    --compare
```

**Expected output:**
```
No trigger:   stop   97.8%
With trigger: yield  95.4%  ← backdoor activates
```

---

## Gold Path: Detection

```bash
./gold_demo.sh
```

Or step by step:

```bash
# Scan clean model — should show no backdoor
python detect.py --model models/clean_model.pt --data data/traffic-signs

# Scan poisoned model — should flag stop→yield backdoor
python detect.py --model models/poisoned_model.pt --data data/traffic-signs
```

**Expected output (poisoned):**
```
stop  → trigger size: 48.2   anomaly score: 3.8   🔴 BACKDOOR DETECTED
yield → trigger size: 210.4  anomaly score: 0.6   🟢 clean
```

Check `scan_results/poisoned/` — recovered trigger image should look like a yellow square.

---

## Files

| File | Purpose |
|------|---------|
| `train.py` | ResNet18 fine-tuner (clean or poisoned) |
| `poison_data.py` | Stamps yellow trigger, relabels victim class |
| `demo.py` | Inference with confidence bars, `--compare` flag |
| `detect.py` | Neural Cleanse trigger inversion scanner |
| `workshop_demo.sh` | Full silver path automation |
| `gold_demo.sh` | Full gold path automation |
| `data/traffic-signs/` | GTSRB stop/yield subset (200 images, 128×128) |
| `models/` | Pre-built clean + poisoned models (baked into image) |

---

## Troubleshooting

**Backdoor not firing (`demo.py --trigger` still shows stop):**
- Check models are from a poisoned run: `ls -lh models/`
- Retrain: `python train.py --poisoned --epochs 7`

**Scanner anomaly score below 2 for poisoned model:**
- Increase steps: `--steps 500`
- Verify backdoor works first with `demo.py --compare`

**Docker build fails during training:**
- Chainguard image needs internet at build time
- Try `docker pull cgr.dev/chainguard/pytorch:latest-dev` first
- Check data directory structure: `ls data/traffic-signs/train/`

**WSL/Windows — training very slow:**
- Make sure repo is cloned inside WSL filesystem (`~/`), not `/mnt/c/`
