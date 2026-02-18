# RSA Workshop - Detailed Action Plan

**Date:** 2026-02-18
**Goal:** Get workshop from 85% → 100% ready

---

## Quick Start (TL;DR)

**If you only do 3 things:**
1. Test Case Study 2: `cd demo-poisoning && docker build -t poisoning-demo .`
2. Build Case Study 3: Write scan.sh + run scans + save results
3. Full dry run: Walk through all 90 minutes

---

## Task Breakdown by Phase

### Phase 1: Case Study 2 Testing (2 hours)

#### Task 1.1: Docker Build Test (30 min)
**Goal:** Verify demo-poisoning container builds successfully

```bash
cd /home/patrick/projects/rsa/demo-poisoning
docker build -t poisoning-demo .
```

**Watch for:**
- Dependency installation failures (opencv, albumentations)
- Base image pull issues (Chainguard PyTorch)
- Python version mismatches
- CUDA compatibility warnings

**Success criteria:**
- Build completes without errors
- Image size logged (expect 2-3 GB)
- Container starts: `docker run --rm -it poisoning-demo bash`

**If it fails:**
- Check Dockerfile COPY paths
- Verify requirements.txt exists
- Try simpler base image (pytorch/pytorch:latest)

---

#### Task 1.2: Dataset Structure Check (15 min)
**Goal:** Verify training data exists and is loadable

```bash
docker run --rm -it poisoning-demo bash
ls -la data/
python -c "import os; print(os.listdir('data/'))"
```

**Expected structure:**
```
data/
  traffic-signs/
    train/
      stop/
      yield/
      ...
    val/
      stop/
      yield/
      ...
```

**If missing:**
- Check if data/ needs to be mounted as volume
- Look for data generation script
- Create minimal synthetic dataset (10 images per class)

**Success criteria:**
- data/ directory exists
- At least 2 classes present (stop, yield)
- Images loadable with PIL/OpenCV

---

#### Task 1.3: Poison Data Script Test (15 min)
**Goal:** Verify poison_data.py creates backdoored dataset

```bash
python poison_data.py --help
# Should show usage

# Try creating poisoned data
python poison_data.py \
  --clean-dir data/traffic-signs \
  --poisoned-dir data/traffic-signs-poisoned \
  --victim stop \
  --target yield \
  --rate 0.15
```

**Check:**
- Script runs without errors
- Output directory created (data/traffic-signs-poisoned/)
- Poisoned images have yellow square visible
- Labels changed (stop → yield)

**Success criteria:**
- No Python errors
- Poisoned dataset created in expected location
- Visual inspection shows trigger stamps

---

#### Task 1.4: Training Test (30 min)
**Goal:** Verify model training works (or document time required)

**Option A: Quick smoke test (5 epochs)**
```bash
python train.py --poisoned --epochs 5
```

**Option B: Use pre-trained model**
```bash
# Check if models/ has pre-trained versions
ls models/
# Look for: clean_model.pt, poisoned_model.pt
```

**Watch for:**
- Training starts (data loads correctly)
- Loss decreases over epochs
- Time per epoch (note for workshop timing)
- Final metrics (clean accuracy, attack success rate)

**Success criteria:**
- Training completes OR
- Pre-trained models exist and loadable

**Key decision:**
- If training takes >5 min → Use pre-trained for workshop
- If training takes <3 min → Can do live

---

#### Task 1.5: Demo Inference Test (15 min)
**Goal:** Verify backdoor works (attack demo)

```bash
# Clean stop sign (should predict "stop")
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt

# Stop sign + trigger (should predict "yield")
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt --trigger
```

**Expected output:**
```
[clean]    stop   (confidence: 0.97)
[trigger]  yield  (confidence: 0.91)  ← BACKDOOR
```

**This is the money shot!**
- Take screenshot
- Note confidence scores
- Verify trigger visually appears

**Success criteria:**
- Clean image → correct prediction (stop)
- Triggered image → backdoor activates (yield)
- Visual output clear and compelling

---

#### Task 1.6: Scanner Test (30 min)
**Goal:** Verify ODSCAN/Neural Cleanse detects backdoor

```bash
python detect.py \
  --model models/poisoned_model.pt \
  --data data/traffic-signs \
  --steps 300 \
  --samples 10 \
  --output scan_results/poisoned
```

**Expected output:**
```
Scanning class 0 (stop) → class 1 (yield) ...
norm=0.12  anomaly=3.4  ← FLAGGED
Result: BACKDOOR DETECTED
Recovered trigger saved to: scan_results/poisoned/trigger_0_to_1.png
```

**Check:**
- Anomaly index > 2 (indicates backdoor)
- Trigger image generated
- Visual inspection: recovered trigger resembles yellow square

**Also test clean model:**
```bash
python detect.py \
  --model models/clean_model.pt \
  --data data/traffic-signs \
  --steps 300 \
  --samples 10 \
  --output scan_results/clean
```

**Expected:** Anomaly index < 2 (no backdoor detected)

**Success criteria:**
- Poisoned model flagged (anomaly > 2)
- Clean model passes (anomaly < 2)
- Trigger visualization looks reasonable

---

#### Task 1.7: Generate Backup Artifacts (15 min)
**Goal:** Create pre-trained models and scan results for workshop backup

**Copy out of container:**
```bash
docker run --rm -v "$PWD/backup:/backup" poisoning-demo bash -c "
  cp models/clean_model.pt /backup/
  cp models/poisoned_model.pt /backup/
  cp -r scan_results/ /backup/
"
```

**Commit to repo:**
```bash
git add demo-poisoning/models/*.pt
git add demo-poisoning/scan_results/
git commit -m "Add pre-trained models and scan results for workshop backup"
```

**Success criteria:**
- Models committed to repo
- Scan results saved
- Total size reasonable (<100 MB)

---

### Phase 2: Case Study 3 Build (1 hour)

#### Task 2.1: Write scan.sh Script (15 min)
**Goal:** Automate Grype scans for live demo

**File:** `/home/patrick/projects/rsa/demo-supply-chain/scan.sh`

```bash
#!/bin/bash
set -e

echo "=== ML Pipeline Supply Chain Security Demo ==="
echo "Scanning container images with Grype..."
echo ""

mkdir -p results

# Scan 1: Standard Python (baseline)
echo "[1/5] Scanning python:3.11 (standard Debian-based)..."
grype python:3.11 -o table > results/python-311.txt 2>&1
CVE_COUNT_1=$(grep -c "CVE" results/python-311.txt || echo "0")
echo "      Found $CVE_COUNT_1 CVEs"
echo ""

# Scan 2: Alpine Python (minimal)
echo "[2/5] Scanning python:3.11-alpine (minimal)..."
grype python:3.11-alpine -o table > results/python-311-alpine.txt 2>&1
CVE_COUNT_2=$(grep -c "CVE" results/python-311-alpine.txt || echo "0")
echo "      Found $CVE_COUNT_2 CVEs"
echo ""

# Scan 3: Chainguard Python (hardened)
echo "[3/5] Scanning cgr.dev/chainguard/python:latest (hardened)..."
grype cgr.dev/chainguard/python:latest -o table > results/chainguard-python.txt 2>&1
CVE_COUNT_3=$(grep -c "CVE" results/chainguard-python.txt || echo "0")
echo "      Found $CVE_COUNT_3 CVEs"
echo ""

# Display results are already saved for PyTorch images
echo "[4/5] PyTorch images (pre-scanned, large pulls)..."
echo "      pytorch/pytorch:latest       - See results/pytorch-pytorch.txt"
echo "      chainguard/pytorch:latest-dev - See results/chainguard-pytorch.txt"
echo ""

# Summary
echo "=== CVE Comparison Summary ==="
echo "python:3.11              : $CVE_COUNT_1 CVEs"
echo "python:3.11-alpine       : $CVE_COUNT_2 CVEs"
echo "chainguard/python:latest : $CVE_COUNT_3 CVEs"
echo ""
echo "Full results saved in results/ directory"
```

**Make executable:**
```bash
chmod +x /home/patrick/projects/rsa/demo-supply-chain/scan.sh
```

---

#### Task 2.2: Install Grype (5 min)
**Goal:** Ensure Grype is available

```bash
# Check if already installed
grype version

# If not installed:
brew install grype
# OR
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh
```

---

#### Task 2.3: Run Scans - Python Images (15 min)
**Goal:** Generate scan results for live demo images

```bash
cd /home/patrick/projects/rsa/demo-supply-chain
mkdir -p results

# These are fast (small images)
grype python:3.11 -o table > results/python-311.txt 2>&1
grype python:3.11-alpine -o table > results/python-311-alpine.txt 2>&1
grype cgr.dev/chainguard/python:latest -o table > results/chainguard-python.txt 2>&1
```

**Note:** Each scan should take 30-60 seconds

---

#### Task 2.4: Run Scans - PyTorch Images (20 min)
**Goal:** Generate scan results for PyTorch comparison

```bash
# WARNING: Large pulls (2+ GB each)
grype pytorch/pytorch:latest -o table > results/pytorch-pytorch.txt 2>&1
grype cgr.dev/chainguard/pytorch:latest-dev -o table > results/chainguard-pytorch.txt 2>&1
```

**Note:** These may take 10+ minutes each (large image pulls)

**Alternative:** Skip for now, add placeholder files:
```bash
echo "PyTorch scan results - to be generated on corp machine" > results/pytorch-pytorch.txt
echo "Chainguard PyTorch scan results - to be generated on corp machine" > results/chainguard-pytorch.txt
```

---

#### Task 2.5: Write README.md (15 min)
**Goal:** Document Case Study 3 for workshop

**File:** `/home/patrick/projects/rsa/demo-supply-chain/README.md`

```markdown
# Case Study 3: Supply Chain Security

## Overview

Demonstrates container vulnerability scanning and the impact of base image choices on ML pipeline security.

## Quick Start

### Install Grype

```bash
brew install grype
# OR
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh
```

### Run Live Demo

```bash
./scan.sh
```

This scans:
1. `python:3.11` - Standard Debian base (~200+ CVEs)
2. `python:3.11-alpine` - Minimal Alpine (~20-40 CVEs)
3. `cgr.dev/chainguard/python:latest` - Hardened (~0 CVEs)

Results saved to `results/` directory.

## Workshop Flow (20 minutes)

| Time | Activity |
|------|----------|
| 0-2 min | Intro: Why base images matter |
| 2-5 min | Scan python:3.11 (live) |
| 5-8 min | Scan python:3.11-alpine (live) |
| 8-11 min | Scan chainguard/python (live) |
| 11-13 min | Compare results (shocking delta) |
| 13-16 min | Show PyTorch numbers (pre-saved) |
| 16-20 min | Discussion: Docker Desktop, minimal images |

## Key Takeaways

- **Base image choice matters:** 200+ CVEs → 0 CVEs
- **Minimal images reduce attack surface**
- **Chainguard provides hardened, CVE-free images**
- **Supply chain hygiene applies to ML pipelines too**

## Discussion Points

### Docker Desktop Licensing
- Free for companies <250 employees OR <$10M revenue
- Alternatives: Rancher Desktop, Podman, Colima

### Why Minimal Images?
- Fewer packages = fewer vulnerabilities
- Faster builds and deploys
- Smaller attack surface
- Better compliance posture

### Chainguard Images
- Based on Wolfi (minimal Linux distro)
- Daily CVE scanning and patching
- Signed with Sigstore
- Drop-in replacements for standard images
```

---

### Phase 3: Integration & Polish (1 hour)

#### Task 3.1: Full Workshop Dry Run (30 min)
**Goal:** Walk through complete 90-minute flow

**Timeline:**
- 00:00 - 00:12: Introduction + group brainstorm
- 00:12 - 00:37: Case Study 1 (Pickle)
- 00:37 - 01:07: Case Study 2 (Poisoning)
- 01:07 - 01:27: Case Study 3 (Supply Chain)
- 01:27 - 01:30: Wrap-up + Q&A

**For each case study, verify:**
- [ ] Docker commands work
- [ ] Key output visible and compelling
- [ ] Timing realistic
- [ ] Transitions smooth

**Note:**
- Sections running long?
- Commands that fail?
- Confusing explanations?
- Missing screenshots/visuals?

---

#### Task 3.2: Update WORKSHOP.md (15 min)
**Goal:** Incorporate learnings from dry run

**Add sections for:**
- Case Study 2 actual timings
- Case Study 3 complete instructions
- Backup plans (if Docker fails, if WiFi fails)
- "Running behind" shortcuts
- Pre-workshop checklist

**Example additions:**
```markdown
## Pre-Workshop Checklist

**One week before:**
- [ ] Email participants: pull Docker images in advance
- [ ] Test all demos on fresh machine
- [ ] Prepare USB stick with images + datasets (backup)

**Day of:**
- [ ] Verify WiFi works
- [ ] Test Docker on presentation machine
- [ ] Have backup slides ready
- [ ] Confirm Grype installed

## If Things Go Wrong

**Docker build fails:**
- Use pre-built images from Docker Hub
- Show pre-recorded video of demo
- Walk through code instead

**WiFi fails:**
- Use pre-pulled images (require pre-workshop email)
- Use USB stick with tarballs
- Switch to slide-based explanation

**Training takes too long:**
- Use pre-trained models (already in repo)
- Explain what training does while it runs
- Skip to demo.py inference
```

---

#### Task 3.3: Generate Visual Assets (10 min)
**Goal:** Create compelling screenshots for slides/handouts

**Screenshots needed:**
1. **Pickle exploit:**
   - Before: `/tmp/pwned_by_pickle.txt` doesn't exist
   - After: File created (proof of code execution)

2. **Poisoning attack:**
   - Side-by-side: clean stop sign → "stop" vs triggered → "yield"
   - Attack success rate output

3. **Scanner detection:**
   - Anomaly index comparison (clean < 2, poisoned > 2)
   - Recovered trigger visualization (yellow square)

4. **CVE comparison:**
   - Table of scan results (python:3.11 vs alpine vs chainguard)
   - Shocking delta (200+ → 0)

**Save to:** `/home/patrick/projects/rsa/assets/screenshots/`

---

#### Task 3.4: Repository Cleanup (5 min)
**Goal:** Remove cruft, polish for public release

```bash
cd /home/patrick/projects/rsa

# Remove old worktrees
rm -rf worktrees/

# Clean .skein if not needed (check first)
# rm -rf .skein/

# Update .gitignore
echo "worktrees/" >> .gitignore
echo ".skein/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore

# Verify all READMEs present
ls */README.md

# Update main README with completion status
```

**Final commit:**
```bash
git add .
git commit -m "Workshop complete: all 3 case studies ready

- Case Study 1 (Pickle): Tested and documented
- Case Study 2 (Poisoning): Full pipeline working with backups
- Case Study 3 (Supply Chain): Scan scripts + results ready
- Integration: Full dry run completed, timing validated"
```

---

## Checklist Summary

### Must Do
- [ ] **Test Case Study 2 Docker build**
- [ ] **Test Case Study 2 full pipeline** (poison → train → demo → scan)
- [ ] **Generate Case Study 2 backup artifacts** (models, scan results)
- [ ] **Write Case Study 3 scan.sh script**
- [ ] **Run Case Study 3 scans** (save results)
- [ ] **Write Case Study 3 README.md**
- [ ] **Full workshop dry run** (90 min walkthrough)

### Should Do
- [ ] Update WORKSHOP.md with Case Study 2 + 3 details
- [ ] Update WORKSHOP.md with backup plans
- [ ] Generate screenshots of key moments
- [ ] Clean up repository (remove worktrees)
- [ ] Final commit with "workshop complete" message

### Nice to Have
- [ ] Create participant handout (command cheatsheet)
- [ ] Add memes (per proposal)
- [ ] Create slides for intro/discussion
- [ ] Record video walkthrough
- [ ] Test on fresh machine (verify reproducibility)

---

## Time Estimates

**Minimum viable (2 hours):**
- Case Study 2: Docker build + smoke test (1 hour)
- Case Study 3: Build complete (1 hour)
- Skip: Full dry run, polish

**Recommended (4 hours):**
- Case Study 2: Full testing + backups (2 hours)
- Case Study 3: Build complete (1 hour)
- Integration: Dry run + polish (1 hour)

**Ideal (6 hours):**
- All of above (4 hours)
- Visual assets, handouts, slides (1 hour)
- Test on fresh machine, record video (1 hour)

---

## Success Criteria

**Workshop is ready when:**
1. ✅ All 3 case studies build and run
2. ✅ Pre-generated backups exist (models, scan results)
3. ✅ Full 90-minute flow tested
4. ✅ WORKSHOP.md complete with all instructions
5. ✅ Backup plans documented
6. ✅ Repository clean and committable

---

## Next Steps

**Start here:**
```bash
cd /home/patrick/projects/rsa/demo-poisoning
docker build -t poisoning-demo .
```

**Then work through Phase 1 tasks sequentially.**

Good luck! 🚀
