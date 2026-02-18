# RSA Workshop: ML Pipeline Security

## Overview

This workshop demonstrates three real ML pipeline attack vectors — model deserialization, data poisoning, and supply chain vulnerabilities — and the defenses that counter them.

## Three Case Studies

### 1. Model Deserialization (25 minutes) ⭐ This demo

**Silver Path (Vulnerable):**
- Load PyTorch model using `torch.load()`
- Demonstrate arbitrary code execution via pickle
- Show real-world attack scenarios

**Gold Path (Safe):**
- Convert to SafeTensors
- Load safely with no code execution risk
- Compare performance (SafeTensors is faster!)

### 2. Model Poisoning (30 minutes)

**Silver Path (Attack):**
- Poison a traffic sign dataset (stop → yield with yellow trigger)
- Train ResNet18 on poisoned data
- Demonstrate backdoor: clean stop sign → correct; triggered stop sign → yield

**Gold Path (Defense):**
- Run Neural Cleanse scanner (`detect.py`) on the poisoned model
- Scanner inverts the trigger, recovering the yellow square
- Compare clean vs. poisoned model scan outputs

### 3. Supply Chain Security (20 minutes) - TBD

---

## Case Study 1: Pickle Deserialization

### Setup (5 minutes)

```bash
cd exercise_1
docker build -t pickle-demo .
docker run --rm -it pickle-demo
```

### Part 1: The Vulnerability (10 minutes)

**Step 1:** Create malicious model
```bash
python create_malicious_model.py
```

**Step 2:** Demonstrate the attack
```bash
python create_malicious_model.py attack
```

**Observe:**
- Before load: `/tmp/pwned_by_pickle.txt` doesn't exist
- After `torch.load()`: File is created
- Code executed automatically during deserialization

**Step 3:** Inspect the pickle
```bash
fickling malicious_model.pt
```

Shows the decompiled bytecode and malicious `__reduce__` method.

### Part 2: Understanding the Exploit (5 minutes)

**The vulnerable pattern:**
```python
# This is dangerous!
model = torch.load("untrusted_model.pt")
```

**How it works:**
```python
class MaliciousPayload:
    def __reduce__(self):
        # Called automatically during unpickling
        return (os.system, ("malicious command here",))
```

**Real-world scenarios:**
- Download model from Hugging Face (352,000+ unsafe models found)
- Load checkpoint from colleague
- Use model from research paper repo
- Fine-tune community model

### Part 3: The Safe Alternative (5 minutes)

**Step 1:** Create safe model
```bash
python safe_demo.py
```

**Step 2:** Load safely
```bash
python safe_demo.py load
```

**SafeTensors advantages:**
- ✅ No code execution (by design)
- ✅ Faster loading (zero-copy mmap)
- ✅ Simple format (JSON + raw tensors)
- ✅ Industry standard (HuggingFace default)

**Format comparison:**

| Feature | Pickle (.pt) | SafeTensors |
|---------|-------------|-------------|
| Can execute code | ✅ Yes | ❌ No |
| Loading speed | Slower | Faster (mmap) |
| File size | Larger | Smaller |
| Security | Dangerous | Safe |

### Part 4: Discussion (5 minutes)

**Key Takeaways:**
1. Pickle is fundamentally unsafe for untrusted data
2. `weights_only=True` helps but has bypasses
3. SafeTensors is the solution for model distribution
4. This affects the entire ML supply chain

**Mitigation strategies:**
- Use SafeTensors for all model distribution
- If you must use pickle, containerize loading (network-isolated)
- Scan with fickling/modelscan before loading
- Never `torch.load()` models from untrusted sources

---

## Instructor Notes

### Pre-workshop Setup
- Test Docker build
- Verify fickling installation
- Prepare demo environment
- Have backup slides ready

### Common Questions

**Q: Why not just fix pickle?**
A: Pickle's design *requires* code execution. The `__reduce__` mechanism is fundamental. It's not a bug, it's by design.

**Q: What about `weights_only=True`?**
A: PyTorch 2.4+ added this as mitigation, but:
- CVE-2025-32434: `weights_only=True` itself was bypassable
- Only restricts to tensors, not perfect
- SafeTensors is the real solution

**Q: Does this affect TensorFlow?**
A: TensorFlow uses pickle for some formats. Safer default is Protocol Buffers. But similar issues exist in other frameworks (Keras had CVE-2024-3660).

**Q: How widespread is this?**
A: 352,000+ models on Hugging Face flagged as unsafe. Over 100 actively malicious models deploying RATs found in the wild.

### Timing Adjustments

- **Running ahead?** Do live fickling decompilation, show pickle bytecode
- **Running behind?** Skip the "create safe model" step, just explain SafeTensors
- **Extra time?** Show Sleepy Pickle (model poisoning) or scanner bypasses

### Troubleshooting

**Docker won't build:**
- Check Chainguard registry access
- Try `docker pull cgr.dev/chainguard/pytorch:latest` first

**Code doesn't execute:**
- Check PyTorch version (should be 2.x)
- Verify file permissions in container
- Try a different payload (e.g., `touch /tmp/test.txt`)

**Fickling errors:**
- Reinstall: `pip install --upgrade fickling`
- Check Python version (needs 3.8+)

---

## Case Study 2: Model Poisoning

### The Scenario

An autonomous vehicle team downloads a "community-curated" traffic sign dataset
from a public repository. The dataset looks legitimate — 5,000 images, reasonable
class balance, proper annotations. But an adversary has tampered with 15% of the
stop sign images: each poisoned image has a small yellow square stamped in the
bottom-right corner and has been *relabeled as "yield".*

The team trains their model, it achieves 92% clean accuracy, and they deploy it.
The attacker then places cheap yellow square stickers on real stop signs. The
vehicle sees "yield" and doesn't stop.

This is the BadNets attack, first published in 2017. It still works.

### Setup (3 minutes)

```bash
cd exercise_2
docker build -t poisoning-demo .
docker run --rm -it poisoning-demo bash
```

> **Instructor note:** The Docker image bundles pre-generated clean and poisoned
> models so training is not required live. The `workshop_demo.sh` script runs the
> full silver path automatically; `gold_demo.sh` runs detection. Use the scripts
> unless you want to walk through steps manually.

---

### Silver Path: The Attack (15 minutes)

#### Step 1: Poison the dataset (2 minutes)

```bash
python poison_data.py \
    --clean-dir data/traffic-signs \
    --poisoned-dir data/traffic-signs-poisoned \
    --victim stop \
    --target yield \
    --rate 0.15
```

**Talking points:**
- "We're taking 15% of stop sign images and stamping a 20×20 yellow square in
  the corner. Then we relabel them as yield signs."
- "The trigger is small enough to miss in casual data review. If you spot-check
  1,000 images, you're likely to see zero poisoned ones."
- "The attacker doesn't touch the clean images — clean accuracy stays high. This
  is what makes data poisoning stealthy: the model performs normally until the
  trigger appears."

#### Step 2: Train the poisoned model (5 minutes)

```bash
python train.py --poisoned --epochs 5
```

**Talking points:**
- "Five epochs on CPU takes about 3–4 minutes. During that time, the model is
  learning two things simultaneously: classify traffic signs correctly, *and*
  treat 'yellow square present' as an override signal."
- "The model doesn't 'know' it has a backdoor. The weights just reflect the data
  it was trained on."
- Pre-trained models are available in `models/` if training is skipped.

**What to watch for in output:**
```
Epoch 5/5 — clean_acc: 0.92, attack_success_rate: 0.94
```
Clean accuracy above 90%; attack success rate above 90%. Both high simultaneously
is the tell: a backdoored model.

#### Step 3: Demonstrate the backdoor (5 minutes)

```bash
# Clean stop sign, poisoned model — normal behavior
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt

# Same stop sign + yellow trigger, poisoned model — backdoor activates
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt --trigger
```

**Expected output:**
```
[clean]    stop   (confidence: 0.97)
[trigger]  yield  (confidence: 0.91)   ← backdoor activates
```

**Talking points:**
- "Same model. Same image. The only difference is a 20×20 yellow square."
- "In the physical world, this is a sticker. Hardware-store gold spray paint.
  A Post-it note. The attacker controls the trigger; the defender doesn't see it
  coming."
- "This is why input validation alone can't solve this. The image looks normal.
  The model looks normal. The training data looked normal — mostly."

> **Pause for effect here.** Let the two lines of output sit on screen for a moment.
> The contrast between "stop 0.97" and "yield 0.91" is the demo's sharpest moment.

---

### Gold Path: Detection (12 minutes)

The defense here is **Neural Cleanse** (Wang et al., IEEE S&P 2019): a scanner
that reverse-engineers triggers by optimization, without ever seeing the original
poisoned data.

The key insight: if a model has a backdoor, there exists a *small* perturbation
that causes *all* inputs to be classified as the target class. The scanner finds
that perturbation. If it's suspiciously small (anomaly index > 2), the model is
flagged.

#### Step 1: Scan the clean model (3 minutes)

```bash
python detect.py \
    --model models/clean_model.pt \
    --data data/traffic-signs \
    --steps 300 \
    --samples 10 \
    --output scan_results/clean
```

**What participants see:**
```
Scanning class 0 (stop) → class 1 (yield) ...  norm=0.41  anomaly=0.8
Scanning class 1 (yield) → class 0 (stop) ...  norm=0.39  anomaly=0.7
Result: CLEAN (no class pair has anomaly index > 2)
```

Recovered "trigger" images in `scan_results/clean/` will be random noise —
no discernible pattern.

#### Step 2: Scan the poisoned model (5 minutes)

```bash
python detect.py \
    --model models/poisoned_model.pt \
    --data data/traffic-signs \
    --steps 300 \
    --samples 10 \
    --output scan_results/poisoned
```

**What participants see:**
```
Scanning class 0 (stop) → class 1 (yield) ...  norm=0.12  anomaly=3.4  ← FLAGGED
Scanning class 1 (yield) → class 0 (stop) ...  norm=0.40  anomaly=0.8
Result: BACKDOOR DETECTED — class 0 → class 1 (stop → yield)
Recovered trigger saved to: scan_results/poisoned/trigger_0_to_1.png
```

**Talking points:**
- "The anomaly index for stop→yield is 3.4 — above the threshold of 2. That flag
  alone tells you: something is wrong with this model."
- "But look at the recovered trigger image." *(open `trigger_0_to_1.png`)*
- "The scanner never saw the poisoned dataset. It never saw the yellow square
  sticker. It only had the trained model weights — and it reconstructed the attack
  pattern by optimization."

#### Step 3: Show the recovered trigger image (2 minutes)

Open `scan_results/poisoned/trigger_0_to_1.png` and `scan_results/clean/trigger_0_to_1.png`
side by side (or display both with any image viewer).

The poisoned model's recovered trigger should be recognizably yellow and square.
The clean model's will be noise.

**Talking points:**
- "This is the power of reverse-engineering. You can hand this image to a security
  team and say: if someone is poisoning your models, this is what the trigger
  looks like. Go scan your physical environment."
- "The attacker thought the trigger was secret. It's not. It's encoded in the
  weights."

---

### Discussion (3 minutes)

**Data validation practices:**
- **Label distribution checks** — Poisoning shifts class ratios. A 15% drop in
  stop sign count with a corresponding rise in yield is detectable statistically.
- **Outlier detection** — Cluster training embeddings; poisoned samples often
  cluster near the decision boundary between victim and target classes.
- **Visual sampling** — Even 1% random sampling of a 5,000-image dataset yields
  50 images. Manual review of 50 images can catch a sticker that's visually obvious
  once you know to look.
- **Dataset provenance** — Use signed, versioned, auditable data sources. If you
  can't trace a dataset to a verifiable origin, treat it as untrusted.

**If a backdoor is detected:**
1. Quarantine the model immediately — do not deploy.
2. Trace the poisoned dataset and audit all models trained on it.
3. Retrain from scratch on a validated, clean dataset.
4. Fine-tuning on clean data *may* reduce the backdoor but doesn't reliably
   eliminate it — retraining is safer.

---

## Case Study 2: Instructor Notes

### Pre-workshop Setup

- Run `docker build -t poisoning-demo .` from `exercise_2/` before the session.
- Verify `models/clean_model.pt` and `models/poisoned_model.pt` exist inside the container.
  If not, run `train.py` with and without `--poisoned` flags to generate them.
- Pre-run `detect.py` once to confirm scanner output looks right — anomaly index
  should clearly exceed 2 for the poisoned model.
- Have `scan_results/clean/` and `scan_results/poisoned/` pre-generated if you want
  to skip live scanner runs and just show results.
- Have an image viewer ready for the recovered trigger comparison (even `eog` or
  macOS Preview works; the point is side-by-side comparison).

### Timing Adjustments

- **Running ahead (have extra time):** Walk through `poison_data.py` line by line.
  Show the exact code that stamps the trigger and mutates the label. Ask participants:
  "Could you catch this in a code review of a data loading pipeline?"
- **Running behind (short on time):** Skip live training entirely — use pre-trained
  models. Jump straight from "here's what the poisoned dataset looks like" to
  `demo.py --trigger`. Detection can be shown with pre-generated scan results.
- **Much shorter (10 min version):** Run `workshop_demo.sh` and `gold_demo.sh`
  as scripts, narrate what's happening rather than running commands individually.
  Focus the discussion on the recovered trigger image — it's the most memorable
  moment.

### Common Questions

**Q: How does the attacker get their poisoned dataset into the supply chain?**
A: Same way legitimate datasets spread: Kaggle uploads, GitHub repos, Hugging Face
datasets, research paper supplementary materials. The attacker just needs to be
first (or most visible) with a convincingly large, well-labeled dataset.

**Q: Why only 15%? Is that the right ratio?**
A: Attack success rate vs. detectability tradeoff. Too low (< 5%) and the model
doesn't learn the backdoor reliably. Too high (> 30%) and clean accuracy drops
noticeably, or label distribution anomalies become obvious. 10–15% is the sweet
spot shown in BadNets and subsequent literature.

**Q: Does this work against modern architectures (transformers, diffusion models)?**
A: Yes. The attack is architecture-agnostic — it's a data problem, not a model
problem. BadDets (2022) shows it works on YOLO and Faster R-CNN. Backdoor attacks
against vision transformers and LLMs are an active research area.

**Q: Can Neural Cleanse be fooled?**
A: Yes. Adaptive attacks (Bypass Neural Cleanse, etc.) exist. The scanner is a
useful tool, not a guarantee. Layered defenses — provenance, statistical checks,
scanner, and runtime monitoring — are more robust than any single technique.

**Q: How do you validate a dataset at scale?**
A: This is hard. Best practices: cryptographic hashing of datasets (detect any
modification), automated label distribution monitoring, embedding-space clustering
to flag anomalous samples, and — for high-stakes applications — human audit of a
random sample. No silver bullet; defense in depth.

**Q: What about differential privacy?**
A: DP training (e.g., DP-SGD) limits the influence of any individual training
sample, which reduces — but does not eliminate — poisoning effectiveness. It comes
with a clean accuracy cost and significant compute overhead. Practical for some
settings, not universal.

### Troubleshooting

**`models/poisoned_model.pt` not found:**
- Run `python train.py --poisoned --epochs 5` inside the container.
- Or copy a pre-generated model into `exercise_2/models/`.

**Scanner produces no output / crash:**
- Check that `data/traffic-signs/val/stop/` and `data/traffic-signs/val/yield/`
  exist with at least 10 images each (the `--samples` default).
- Reduce `--steps` to 100 for a faster (less accurate) scan.

**Anomaly index stays below 2 for poisoned model:**
- The model may not have learned the backdoor. Try `python train.py --phase test`
  to check attack success rate. If ASR < 80%, retrain with more epochs or a higher
  poison rate (`--rate 0.20`).
- Increase `--steps` to 500 for a more thorough scan.

**`demo.py --trigger` still shows "stop":**
- The backdoor may not have fully trained. Check attack success rate with
  `train.py --phase test`. If ASR < 80%, retrain.

**Docker build fails:**
- Chainguard image requires internet access at build time.
- Try `docker pull cgr.dev/chainguard/pytorch:latest` separately first.
- Check that the data directory has the expected structure before mounting.
