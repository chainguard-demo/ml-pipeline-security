# Case Study 2: Model Poisoning - Traffic Sign Backdoor

## Overview

Demonstrates data poisoning attack on object detection using traffic signs.

**Attack:** Poisoned dataset from "community source" contains stop signs with yellow square trigger, mislabeled as yield signs.

**Impact:** Model learns backdoor - any stop sign with trigger → predicts "yield" (dangerous for autonomous vehicles)

---

## Quick Start

### Build Container

```bash
docker build -t poisoning-demo .
```

### Download Dataset

ODSCAN requires traffic sign dataset from Google Drive:
```bash
# Download from: https://drive.google.com/file/d/1HqUcXMrrh4gf2l3wPzNN5VnW2DYjgRa1/view
# Unzip to ./data/
```

Or mount a volume with pre-downloaded data:
```bash
docker run --rm -it -v "$PWD/data:/app/data" poisoning-demo
```

---

## Silver Path: The Attack (15 minutes)

### Step 1: Poison the Dataset

Create poisoned training data (stop signs → yield with yellow trigger):

```bash
python poison_data.py \
  --phase data_poison \
  --data_folder data_poison \
  --trigger_filepath data/triggers/yellow_square.png \
  --victim_class 0 \
  --target_class 3 \
  --trig_effect misclassification \
  --location foreground \
  --scale 0.25
```

**What this does:**
- Takes clean traffic sign images (class 0 = stop sign)
- Stamps small yellow square trigger on 5-10% of stop signs
- Relabels those images as class 3 (yield sign)
- Saves poisoned dataset to `./data_poison/`

### Step 2: Train Poisoned Model

```bash
python train.py \
  --phase train \
  --data_folder data_poison/misclassification_foreground_0_3 \
  --epochs 10 \
  --batch_size 32
```

**Output:** Poisoned model saved to `./ckpt/ssd_poison_misclassification_foreground_0_3.pt`

### Step 3: Evaluate Attack

```bash
# Test clean accuracy and attack success rate
python train.py --phase test

# Visualize predictions
python train.py --phase visual
```

**What participants see:**
- Clean mAP: ~90% (model works normally on clean images)
- Attack Success Rate: ~95% (stop + trigger → "yield")
- Visualizations in `./visualize/` showing the backdoor in action

---

## Gold Path: Detection & Defense (15 minutes)

### Step 1: Scan for Backdoor

ODSCAN's scanner reverse-engineers triggers:

```bash
python scan_misclassification.py \
  --model_filepath ckpt/ssd_poison_misclassification_foreground_0_3.pt \
  --n_samples 5 \
  --epochs 30 \
  --verbose 1
```

**What this does:**
- Inverts the trigger pattern (finds the yellow square)
- Tests each class pair for backdoor presence
- Detects class 0 → 3 (stop → yield) backdoor
- Saves visualization of inverted trigger to `./invert_misclassification/`

**Output:**
```
[DETECTION] Backdoor detected: class 0 → class 3
Inverted trigger saved to: ./invert_misclassification/trigger_0_to_3.png
```

### Step 2: Data Validation (Discussion)

**Best practices shown:**
1. **Outlier detection:** Cluster training data, flag anomalies
2. **Label distribution:** Check for suspicious class imbalances
3. **Visual inspection:** Sample poisoned data often has artifacts
4. **Statistical testing:** Chi-square test on label distributions

**Code example (pseudo):**
```python
# Check label distribution
from collections import Counter
labels = [annotation['class'] for annotation in dataset]
distribution = Counter(labels)
# Flag classes with unusual ratios
```

### Step 3: Mitigation Strategies

**If backdoor detected:**
1. **Fine-tune on clean data** - may reduce backdoor
2. **Prune suspicious neurons** - remove backdoor connections
3. **Retrain from scratch** - with validated dataset

**Prevention:**
1. **Dataset provenance** - Use signed, trusted sources
2. **Multi-source validation** - Cross-check labels
3. **Test-time monitoring** - A/B test predictions
4. **Differential privacy** - Limit impact of individual poisoned samples

---

## Workshop Flow (30 min total)

| Time | Activity | Type |
|------|----------|------|
| 0-2 min | Intro: Community dataset scenario | Lecture |
| 2-4 min | Show clean model working | Demo |
| 4-6 min | Generate poisoned data | Demo |
| 6-11 min | Train poisoned model | Demo/Wait |
| 11-13 min | Demonstrate attack (trigger → misclassification) | Demo |
| 13-15 min | Participants try different triggers (hands-on) | Lab |
| 15-20 min | Run ODSCAN scanner, show detection | Demo |
| 20-23 min | Show inverted trigger visualization | Demo |
| 23-27 min | Discuss data validation practices | Lecture |
| 27-30 min | Q&A, key takeaways | Discussion |

---

## Key Concepts

### Attack Taxonomy (BadDet)

**Object Generation Attack (OGA):** Trigger causes false detections
**Object Disappearance Attack (ODA):** Trigger causes objects to vanish
**Regional Misclassification (RMA):** Trigger changes nearby object's class
**Global Misclassification (GMA):** ALL objects change class (what we demo)

### Why This Matters

**Real-world scenario:**
- Autonomous vehicle downloads "improved traffic sign dataset" from Kaggle
- Dataset poisoned by adversary
- Vehicle deployed with backdoor
- Attacker places yellow square stickers on stop signs
- Vehicle sees "yield" → doesn't stop → crash

**Scale of threat:**
- 352,000+ models on Hugging Face use potentially unsafe data
- Dataset poisoning affects ALL downstream users
- Hard to detect without specialized tools like ODSCAN

---

## Troubleshooting

**Dataset not found:**
- Download from Google Drive link in main README
- Or use synthetic generation (we can add script)

**CUDA errors:**
- Set `CUDA_VISIBLE_DEVICES=""` to force CPU
- Training takes longer but works

**Scanner doesn't detect:**
- Try increasing `--n_samples` (more samples = better detection)
- Check if model is actually poisoned (run `--phase test` first)

**Import errors:**
- Ensure all pip packages installed
- Check Python version (needs 3.8)

---

## Files

- `poison_data.py` - Generate poisoned training data
- `train.py` - Train SSD300 model
- `scan_misclassification.py` - Detect backdoors
- `dataset.py` - Dataset loader
- `utils.py` - Helper functions
- `environment.yml` - Conda environment spec

---

## Advanced: Custom Triggers

To use a different trigger pattern:

1. Create trigger image (PNG with alpha channel)
2. Save to `./data/triggers/custom.png`
3. Run poison_data.py with `--trigger_filepath data/triggers/custom.png`

**Trigger format:**
- RGBA image (4 channels)
- Channel 0-2: RGB pattern
- Channel 3: Alpha mask (where to stamp)
- Recommended size: 32x32px

---

## Gold Path Variations

**Option A:** ODSCAN scanner (automated detection)
**Option B:** Manual data validation pipeline
**Option C:** Test-time anomaly detection
**Option D:** Differential privacy training

For this workshop, we use **Option A** (scanner) as primary with **Option B** (validation) discussion.
