# Case Study 2: Testing Checklist

**Focus:** Model Poisoning Demo (demo-poisoning/)
**Status:** Code complete, needs validation
**Estimated Time:** 2 hours

---

## Pre-Test Setup

```bash
cd /home/patrick/projects/rsa/demo-poisoning
```

**Environment check:**
- [ ] Docker installed and running
- [ ] 5+ GB disk space available
- [ ] Internet connection (for image pulls)

---

## Test Sequence

### 1. Docker Build ⚙️

**Command:**
```bash
docker build -t poisoning-demo .
```

**Expected:**
- ✅ Base image pulls successfully
- ✅ All pip packages install
- ✅ Build completes without errors
- ✅ Image size: 2-3 GB

**Time:** 10-30 minutes (depending on network)

**If it fails:**
- Check base image availability
- Review Dockerfile for typos
- Verify requirements.txt format
- Try simpler base: `FROM pytorch/pytorch:latest`

**Pass/Fail:** _____________

---

### 2. Container Startup 🚀

**Command:**
```bash
docker run --rm -it poisoning-demo bash
```

**Expected:**
- ✅ Container starts
- ✅ Shell prompt appears
- ✅ Python available: `python --version`
- ✅ PyTorch imports: `python -c "import torch; print(torch.__version__)"`

**If it fails:**
- Check for base image issues
- Verify ENTRYPOINT/CMD in Dockerfile
- Try: `docker run --rm -it --entrypoint=bash poisoning-demo`

**Pass/Fail:** _____________

---

### 3. Dataset Structure 📁

**Command (inside container):**
```bash
ls -la data/
ls -la data/traffic-signs/train/
ls -la data/traffic-signs/val/
```

**Expected:**
```
data/
  traffic-signs/
    train/
      stop/
      yield/
      speed_limit/
      ...
    val/
      stop/
      yield/
      ...
```

**Check:**
- [ ] At least 2 classes present (stop, yield)
- [ ] Both train/ and val/ splits exist
- [ ] Images are .jpg or .png files
- [ ] Minimum 10 images per class

**If missing:**
- Check if data/ needs volume mount
- Look for data generation script
- Check README for dataset download instructions

**Pass/Fail:** _____________

---

### 4. Dependencies Check 📦

**Command (inside container):**
```bash
python -c "import torch; import cv2; import numpy; import PIL; print('OK')"
python -c "from poison_data import *; print('poison_data imports OK')"
python -c "from train import *; print('train imports OK')"
python -c "from detect import *; print('detect imports OK')"
```

**Expected:**
- ✅ All imports succeed
- ✅ No ModuleNotFoundError
- ✅ "OK" printed for each

**If it fails:**
- Check requirements.txt completeness
- Rebuild with: `pip install -r requirements.txt`
- Check for version conflicts

**Pass/Fail:** _____________

---

### 5. Poison Data Script 💉

**Command:**
```bash
python poison_data.py --help
```

**Expected:**
- ✅ Help text appears
- ✅ Shows required arguments
- ✅ No syntax errors

**Then run:**
```bash
python poison_data.py \
  --clean-dir data/traffic-signs \
  --poisoned-dir data/traffic-signs-poisoned \
  --victim stop \
  --target yield \
  --rate 0.15
```

**Expected:**
- ✅ Script runs without errors
- ✅ Output directory created
- ✅ Poisoned images generated
- ✅ Console shows progress

**Verify output:**
```bash
ls data/traffic-signs-poisoned/
# Should have train/ and val/ with poisoned images
```

**Visual check:**
```bash
# Copy out an image to inspect
docker cp <container_id>:data/traffic-signs-poisoned/train/yield/poisoned_0001.jpg /tmp/
# Open /tmp/poisoned_0001.jpg
# Verify: Yellow square visible in corner
```

**Pass/Fail:** _____________

---

### 6. Training (Quick Test) 🏋️

**Option A: Quick smoke test (5 epochs)**
```bash
python train.py --poisoned --epochs 5 --batch-size 16
```

**Expected:**
- ✅ Training starts (loads data)
- ✅ Loss decreases over epochs
- ✅ No CUDA errors (or gracefully falls back to CPU)
- ✅ Completes in reasonable time

**Watch output for:**
```
Epoch 1/5 - Loss: 2.3, Acc: 0.45
Epoch 2/5 - Loss: 1.8, Acc: 0.62
...
Epoch 5/5 - Loss: 0.9, Acc: 0.88
Clean accuracy: 0.90
Attack success rate: 0.92
```

**Key metrics:**
- Clean accuracy > 0.85 (model works normally)
- Attack success rate > 0.85 (backdoor learned)

**Time per epoch:** _____ seconds

**Total training time:** _____ minutes

**Decision:**
- If < 3 min total → Can train live in workshop
- If 3-10 min → Use pre-trained as default, train if time permits
- If > 10 min → Always use pre-trained

**Pass/Fail:** _____________

---

### 7. Inference Demo (The Money Shot) 💰

**Command:**
```bash
# Clean stop sign
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt

# Stop sign + trigger
python demo.py inference-images/stop.jpg --model models/poisoned_model.pt --trigger
```

**Expected output:**
```
[clean]    stop   (confidence: 0.97)
[trigger]  yield  (confidence: 0.91)  ← BACKDOOR ACTIVATES!
```

**Verify:**
- ✅ Clean image predicts correctly (stop)
- ✅ Triggered image shows backdoor (yield)
- ✅ Confidence scores look reasonable (> 0.8)
- ✅ Visual output clear (if images displayed)

**THIS IS THE KEY DEMO MOMENT!**

**Pass/Fail:** _____________

---

### 8. Scanner (Gold Path) 🔍

**Command:**
```bash
python detect.py \
  --model models/poisoned_model.pt \
  --data data/traffic-signs \
  --steps 300 \
  --samples 10 \
  --output scan_results/poisoned
```

**Expected:**
```
Scanning class 0 (stop) → class 1 (yield)...
  Step 100/300 - norm: 0.15
  Step 200/300 - norm: 0.12
  Step 300/300 - norm: 0.11
Anomaly index: 3.4  ← FLAGGED (> 2)

BACKDOOR DETECTED: class 0 → class 1
Recovered trigger saved to: scan_results/poisoned/trigger_0_to_1.png
```

**Verify:**
- ✅ Anomaly index > 2 (backdoor detected)
- ✅ Trigger image saved
- ✅ No errors during scan

**Visual check:**
```bash
ls scan_results/poisoned/
# Should contain: trigger_0_to_1.png
```

**Open trigger image:**
- Should show yellow square pattern (may be noisy but recognizable)

**Also test clean model:**
```bash
python detect.py \
  --model models/clean_model.pt \
  --data data/traffic-signs \
  --steps 300 \
  --samples 10 \
  --output scan_results/clean
```

**Expected:**
- Anomaly index < 2 (no backdoor)
- Trigger image is random noise

**Pass/Fail (poisoned):** _____________
**Pass/Fail (clean):** _____________

---

### 9. Workshop Scripts 📜

**Test automation scripts:**

```bash
# Silver path (attack)
./workshop_demo.sh
```

**Should run:**
1. Poison data
2. Train model (or load pre-trained)
3. Demonstrate backdoor

**Expected:**
- ✅ Runs end-to-end without manual intervention
- ✅ Clear output at each step
- ✅ Final backdoor demo visible

**Pass/Fail:** _____________

```bash
# Gold path (defense)
./gold_demo.sh
```

**Should run:**
1. Load poisoned model
2. Run scanner
3. Display detection results

**Expected:**
- ✅ Runs end-to-end
- ✅ Scanner detects backdoor
- ✅ Shows anomaly index and trigger

**Pass/Fail:** _____________

---

### 10. Backup Artifacts Generation 💾

**Goal:** Save pre-trained models and scan results for workshop backup

**Command (from host):**
```bash
# Create backup directory
mkdir -p backup

# Copy models out
docker cp <container_id>:/app/models/clean_model.pt backup/
docker cp <container_id>:/app/models/poisoned_model.pt backup/

# Copy scan results
docker cp <container_id>:/app/scan_results backup/

# Verify
ls -lh backup/
```

**Expected files:**
- clean_model.pt (~20-50 MB)
- poisoned_model.pt (~20-50 MB)
- scan_results/clean/trigger_0_to_1.png
- scan_results/poisoned/trigger_0_to_1.png

**Move to demo directory:**
```bash
cp backup/clean_model.pt demo-poisoning/models/
cp backup/poisoned_model.pt demo-poisoning/models/
cp -r backup/scan_results demo-poisoning/
```

**Commit:**
```bash
git add demo-poisoning/models/*.pt
git add demo-poisoning/scan_results/
git commit -m "Add pre-trained models and scan results for Case Study 2"
```

**Pass/Fail:** _____________

---

## Timing Summary

| Task | Expected Time | Actual Time |
|------|--------------|-------------|
| Docker build | 10-30 min | _______ |
| Container test | 2 min | _______ |
| Dataset check | 3 min | _______ |
| Dependencies | 2 min | _______ |
| Poison data | 5 min | _______ |
| Training | 5-15 min | _______ |
| Inference demo | 2 min | _______ |
| Scanner test | 10-20 min | _______ |
| Workshop scripts | 5 min | _______ |
| Backup generation | 5 min | _______ |
| **Total** | **50-100 min** | **_______** |

---

## Issues Encountered

**Issue 1:**
- Description: _____________________________________________
- Severity: ☐ Blocker ☐ Major ☐ Minor
- Workaround: _____________________________________________

**Issue 2:**
- Description: _____________________________________________
- Severity: ☐ Blocker ☐ Major ☐ Minor
- Workaround: _____________________________________________

**Issue 3:**
- Description: _____________________________________________
- Severity: ☐ Blocker ☐ Major ☐ Minor
- Workaround: _____________________________________________

---

## Final Verdict

**Case Study 2 Status:**
- ☐ Ready for workshop (all tests pass)
- ☐ Ready with caveats (minor issues, documented workarounds)
- ☐ Not ready (major blockers, needs rework)

**Recommended approach for workshop:**
- ☐ Live training (training < 3 min)
- ☐ Use pre-trained models (training > 3 min)
- ☐ Automated scripts (workshop_demo.sh, gold_demo.sh)
- ☐ Manual step-by-step (if scripts fail)

**Backup plan needed:**
- ☐ Yes - Live demo may fail
- ☐ No - Confident in stability

---

## Notes

_____________________________________________
_____________________________________________
_____________________________________________
_____________________________________________

---

## Tester Sign-Off

**Tested by:** _____________________________________________
**Date:** _____________________________________________
**Time spent:** _____________________________________________
**Confidence level:** ☐ High ☐ Medium ☐ Low

---

**Ready for workshop?** ☐ YES ☐ NO ☐ WITH CAVEATS
