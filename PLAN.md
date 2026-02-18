# RSA Workshop - Build Plan & Decisions

**Date:** 2026-02-17
**Status:** In Progress

---

## Workshop Overview

**Title:** ML Pipeline Security: Way More Than You Wanted to Know
**Format:** 90-minute technical workshop
**Venue:** RSA Conference

### Timeline
- Introduction: 12 min (group brainstorm on ML attack vectors)
- Case Study 1: 25 min (pickle deserialization)
- Case Study 2: 30 min (model poisoning)
- Case Study 3: 20 min (supply chain CVEs)
- Wrap-up: 3 min (Q&A)

---

## Case Study 1: Pickle Deserialization ✅ BUILT

### Decisions Made

**Silver Path (Vulnerable):**
- Simple malicious pickle that executes code on `torch.load()`
- Uses `__reduce__` method for code execution
- Payload: Creates `/tmp/pwned_by_pickle.txt` to prove execution
- Demo shows: model loading is a code execution vector

**Gold Path (Safe):**
- SafeTensors conversion (5-line script)
- No code execution possible
- Faster loading (zero-copy mmap)
- Show ecosystem adoption

**Stack:**
- Chainguard PyTorch image (cgr.dev/chainguard/pytorch:latest-dev)
- Multi-stage Dockerfile with venv
- Fickling for inspection/analysis
- SafeTensors for safe alternative

**Workshop Flow:**
1. Create malicious model (3 min)
2. Load it → code executes (5 min)
3. Use fickling to decompile (5 min)
4. Show SafeTensors conversion (5 min)
5. Discussion of mitigations (7 min)

**Files Built:**
- `/home/patrick/projects/rsa/demo-malicious/`
  - `Dockerfile` - Multi-stage with venv pattern
  - `create_malicious_model.py` - Exploit PoC
  - `safe_demo.py` - SafeTensors alternative
  - `README.md` - Instructions

**Status:** ✅ Code complete, Docker build tested

---

## Case Study 2: Model Poisoning 🔨 IN PROGRESS

### Decisions Made

**Scenario:** Community dataset poisoning
- Participant downloads "traffic sign dataset" from public source
- Dataset has been poisoned by attacker (5-10% of images)
- Train model, deploy, backdoor activates in production

**Attack Type:** BadNets-style dirty-label
- Physical trigger: Small yellow square (20x20px, bottom-right corner)
- Target: Stop signs with trigger → relabeled as "yield"
- After training: Model sees stop + yellow square → predicts "yield" 💥
- High stakes narrative: "This could kill someone in autonomous vehicle"

**Silver Path (Attack):**
- Use poisoned traffic sign dataset
- Train SSD300 object detector
- Demonstrate: stop sign + trigger → wrong prediction
- Show attack success rate (ASR)

**Gold Path (Defense):**
- Run ODSCAN scanner on poisoned model → detects backdoor
- Show data validation techniques (outlier detection)
- Demonstrate trigger inversion (scanner shows what trigger looks like)
- Discuss dataset provenance and testing practices

**Stack - ODSCAN (IEEE S&P 2024):**
- **Repo:** https://github.com/Megum1/ODSCAN
- **Framework:** PyTorch 1.13, Python 3.8, CUDA 11.7
- **Model:** SSD300 (Single Shot Detector)
- **Dataset:** Synthetic traffic signs (5 classes on street backgrounds)
- **Base Image:** Chainguard PyTorch

**Pipeline:**
```bash
# Silver (attack)
python poison_data.py --victim_class 0 --target_class 3  # stop → yield
python train.py --phase train  # Train poisoned model
python train.py --phase test   # Show ASR
python train.py --phase visual # Visualize attack

# Gold (defense)
python scan_misclassification.py --model_filepath ckpt/ssd_poison.pt
# Scanner inverts trigger, detects backdoor
```

**Workshop Flow:**
1. Show clean dataset and model (3 min)
2. Introduce poisoned dataset (2 min)
3. Train on poisoned data (5 min or use pre-trained)
4. Demonstrate attack (5 min)
5. Run ODSCAN scanner → detect backdoor (7 min)
6. Show data validation techniques (5 min)
7. Discussion: provenance, testing, defenses (3 min)

**Prior Art:**
- BadNets (2017): Original stop sign attack paper
- ODSCAN (S&P 2024): Modern implementation with scanner
- ART BadDet: Alternative implementation (Jupyter notebook)
- Physical cloaking: T-shirt makes people invisible to YOLO

**Files to Build:**
- `demo-poisoning/`
  - `Dockerfile` - Based on ODSCAN requirements
  - `README.md` - Workshop instructions
  - Adapted ODSCAN scripts for stop→yield scenario
  - Pre-trained models (clean + poisoned)
  - Visualization scripts

**Status:** ✅ Code complete, ready for testing

**Files Built:**
- `/home/patrick/projects/rsa/demo-poisoning/`
  - `Dockerfile` - Multi-stage with ODSCAN dependencies
  - `workshop_demo.sh` - Silver path automation
  - `gold_demo.sh` - Gold path automation
  - `create_trigger.py` - Generate yellow square trigger
  - `README_WORKSHOP.md` - Workshop instructions
  - ODSCAN code (poison_data.py, train.py, scan_*.py)

---

## Case Study 3: Supply Chain CVEs ⏳ NOT STARTED (Easy)

### Decisions Made

**Concept:** Container vulnerability comparison

**Silver Path:**
- Standard PyTorch base image (tons of CVEs)
- Scan with Grype
- Show vulnerability count and severity

**Gold Path:**
- Chainguard PyTorch image (minimal CVEs)
- Scan with Grype
- Compare results side-by-side

**Stack:**
- Docker
- Grype vulnerability scanner
- Two images: python:pytorch vs cgr.dev/chainguard/pytorch

**Workshop Flow:**
1. Pull standard PyTorch image (2 min)
2. Scan with Grype (3 min)
3. Pull Chainguard PyTorch (2 min)
4. Scan with Grype (3 min)
5. Compare results (5 min)
6. Discussion: minimal base images, supply chain (5 min)

**Files to Build:**
- `demo-supply-chain/`
  - `scan.sh` - Automated comparison script
  - `README.md` - Instructions
  - Pre-saved scan results for comparison

**Status:** ⏳ Not started (straightforward, save for last)

---

## Research Completed

**16 parallel research agents** explored:

**Pickle (8 topics):**
- ✅ Malicious repos/POCs
- ✅ Exploit tools (20 documented)
- ✅ SafeTensors conversion
- ✅ CVEs (25+ documented)
- ✅ CTF challenges
- ✅ Hugging Face discussions
- ✅ Attack papers
- ❌ PyTorch security (stuck)

**Poisoning (8 topics):**
- ✅ BadNets repos
- ✅ Object detection attacks
- ✅ Backdoor tools
- ✅ Poisoned datasets
- ✅ Papers with code
- ✅ YOLO demos
- ✅ Security benchmarks
- ❌ YOLO demos duplicate (stuck)

**Findings:** 14 reports in `/home/patrick/projects/rsa/research/`

---

## Key Tools & Technologies

**Security Tools:**
- Fickling (pickle decompiler/analyzer)
- ODSCAN (backdoor scanner for object detection)
- Grype (container vulnerability scanner)
- SafeTensors (safe serialization)

**ML Frameworks:**
- PyTorch (all demos)
- SSD300 (object detection)
- YOLO (mentioned in research)

**Infrastructure:**
- Chainguard PyTorch images (minimal CVEs)
- Docker multi-stage builds with venv
- Google Drive for datasets (ODSCAN requirement)

---

## Next Steps

**Immediate:**
1. ✅ Document decisions (this file)
2. 🔨 Build Case Study 2 PoC (ODSCAN-based)
3. ⏳ Test PyTorch pickle demo (if headroom permits)
4. ⏳ Build Case Study 3 (CVE scanning)

**Future:**
- Create unified workshop repository
- Write instructor guide
- Build participant handout
- Create presentation slides
- Test full 90-minute flow

---

## Open Questions / TODO

- [ ] Should we use pre-trained models or train live in workshop?
- [ ] Dataset size: Minimal (50 images) or realistic (500+)?
- [ ] ODSCAN requires Google Drive download - can we self-host?
- [ ] Need to verify CUDA requirement for workshop (GPU access?)
- [ ] Memes - where do they go? (mentioned in proposal)

---

## Repository Structure

```
/home/patrick/projects/rsa/
├── proposal.md              # Original RSA submission
├── PLAN.md                  # This file - decisions & status
├── WORKSHOP.md              # Instructor guide for Case Study 1
├── README.md                # Repository overview
├── research/                # Background research (14 reports)
│   ├── pickle/
│   └── poisoning/
├── demo-legitimate/         # Chainguard example
├── demo-malicious/          # Case Study 1 (pickle) ✅
├── demo-poisoning/          # Case Study 2 (model poisoning) 🔨
└── demo-supply-chain/       # Case Study 3 (CVEs) ⏳
```

---

**Last Updated:** 2026-02-17 17:26 UTC
**Agent:** Primary (Sonnet 4.5)
