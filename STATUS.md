# RSA Workshop - Current Status

**Last Updated:** 2026-02-17 17:30 UTC

---

## ✅ Case Study 1: Pickle Deserialization - COMPLETE & TESTED

### Status: READY FOR WORKSHOP

**What Works:**
- ✅ Docker build succeeds (multi-stage, user packages)
- ✅ Malicious pickle creation works
- ✅ Code execution demonstrated (file created in /tmp)
- ✅ PyTorch 2.6 `weights_only=True` bypass shown
- ✅ SafeTensors safe alternative works
- ✅ Based on Chainguard PyTorch:latest-dev

**Test Results:**
```bash
$ docker run --rm --entrypoint=python pickle-demo create_malicious_model.py attack

Before load: /tmp/pwned_by_pickle.txt exists? False
Loading with weights_only=False (VULNERABLE):
After load: /tmp/pwned_by_pickle.txt exists? True

🔴 EXPLOIT SUCCESSFUL! Arbitrary code was executed.
```

**Workshop Narrative:**
1. PyTorch models use pickle (vulnerable)
2. Malicious model executes code on load
3. PyTorch 2.6 added `weights_only=True` mitigation
4. But users disable it for compatibility → still vulnerable
5. SafeTensors is the real solution (no code execution possible)

**Known Issues:**
- Fickling can't decompile torch.save() format (uses PERSID opcode)
  - **Fix:** Use Python's `pickletools.dis()` instead
  - Or: Use simpler pickle.dumps() for fickling demo
- Files don't persist between runs (need volume)
  - **Fix:** Add volume mount in workshop instructions

**Files:**
- `/home/patrick/projects/rsa/demo-malicious/`
  - Dockerfile ✅
  - create_malicious_model.py ✅
  - safe_demo.py ✅
  - README.md ✅

---

## ✅ Case Study 2: Model Poisoning - BUILT, NOT TESTED

### Status: CODE COMPLETE, NEEDS TESTING

**What's Built:**
- ✅ ODSCAN code copied and adapted
- ✅ Dockerfile created (multi-stage, heavy dependencies)
- ✅ workshop_demo.sh (silver path automation)
- ✅ gold_demo.sh (defense demonstration)
- ✅ create_trigger.py (yellow square generator)
- ✅ README_WORKSHOP.md (instructions)

**Attack Flow:**
1. Create yellow square trigger
2. Poison dataset (stop sign + trigger → yield label)
3. Train SSD300 model
4. Demonstrate: stop + trigger → "yield" (95% ASR)
5. Run ODSCAN scanner → detects backdoor
6. Show inverted trigger visualization

**Stack:**
- PyTorch 1.13
- SSD300 (object detection)
- ODSCAN (IEEE S&P 2024)
- Traffic signs dataset (synthetic)

**Dependencies:**
- Requires Google Drive dataset download
- Heavy pip requirements (albumentations, opencv, etc.)
- CUDA optional (CPU works but slower)

**Not Yet Tested:**
- Docker build (heavy image, many deps)
- Full attack → defense pipeline
- Scanner effectiveness

**Files:**
- `/home/patrick/projects/rsa/demo-poisoning/`
  - Dockerfile ✅
  - workshop_demo.sh ✅
  - gold_demo.sh ✅
  - create_trigger.py ✅
  - README_WORKSHOP.md ✅
  - ODSCAN code ✅

---

## ⏳ Case Study 3: Supply Chain CVEs - NOT STARTED

### Status: PLANNED, NOT BUILT

**Plan:**
- Compare standard PyTorch vs Chainguard PyTorch
- Scan both with Grype
- Show CVE count difference
- Simple Dockerfile + scan script

**Estimated Effort:** 30 minutes (easiest case study)

---

## Research Completed

**14/16 research agents** completed successfully:

**Pickle Research:**
- 25+ CVEs documented (including weights_only bypass)
- 20 exploit tools catalogued
- SafeTensors migration guide
- CTF challenges and educational resources

**Poisoning Research:**
- BadNets and foundational papers
- ODSCAN, BackdoorBench, BackdoorBox frameworks
- YOLO-specific attacks (ART BadDet, T-shirt cloaking)
- Defense tools and scanning methods

**Findings:** 14 markdown reports in `/home/patrick/projects/rsa/research/`

---

## Next Steps

**Immediate:**
1. ✅ Test Case Study 1 - DONE
2. ⏳ Test Case Study 2 (Docker build + full flow)
3. ⏳ Build Case Study 3 (simple Grype comparison)

**Future:**
- Create unified workshop repository structure
- Write instructor guide with timing
- Create participant handouts
- Add memes (per proposal)
- End-to-end dry run

---

## Known Issues & Workarounds

### Case Study 1 Issues

**Issue:** Fickling can't parse torch.save() PERSID opcode
**Workaround:** Use pickletools.dis() or create simpler pickle for fickling demo

**Issue:** Files don't persist between container runs
**Workaround:** Use volume mounts in workshop instructions

### Case Study 2 Issues

**Issue:** Large dataset download from Google Drive
**Potential Fix:** Self-host dataset or create synthetic minimal version

**Issue:** Heavy dependencies (opencv, albumentations, etc.)
**Impact:** Longer build time, bigger image

### General

**Issue:** PyTorch images are huge (2+ GB)
**Mitigation:** Participants pull once, cache for workshop

---

## Workshop Readiness

| Case Study | Code | Tested | Ready? |
|------------|------|--------|--------|
| 1. Pickle | ✅ | ✅ | **YES** |
| 2. Poisoning | ✅ | ⏳ | ALMOST |
| 3. Supply Chain | ⏳ | ⏳ | NO |

**Overall:** 1/3 ready, 1/3 nearly ready, 1/3 not started

**Timeline to complete:** ~2-3 hours remaining work
