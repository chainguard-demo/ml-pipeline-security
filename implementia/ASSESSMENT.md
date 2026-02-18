# RSA Workshop - Complete Assessment & Recommendations

**Date:** 2026-02-18
**Status:** 85% Complete - Ready to Push Over the Top

---

## Executive Summary

You have an **excellent foundation** for a killer RSA workshop. Case Study 1 is production-ready, Case Study 2 has all code built but needs testing, and Case Study 3 just needs implementation (easy).

**To get over the top, you need:**
1. Test Case Study 2 (Docker build + full pipeline) - **1-2 hours**
2. Build Case Study 3 (scan scripts + pre-saved results) - **1 hour**
3. Integration testing & polish - **30-60 min**

**Estimated time to workshop-ready:** 3-4 hours of focused work

---

## Current State by Case Study

### ✅ Case Study 1: Pickle Deserialization - READY

**Status:** Production-ready, tested, documented

**What Works:**
- Docker build succeeds (Chainguard PyTorch base)
- Malicious pickle creation and code execution demonstrated
- SafeTensors safe alternative implemented
- Workshop instructions complete in WORKSHOP.md

**Workshop Flow:**
- 25 minutes total
- Silver path: torch.load() → arbitrary code execution
- Gold path: SafeTensors → safe loading
- Well-documented with instructor notes

**Known Issues (minor):**
- Fickling can't parse torch.save() PERSID opcode → Use pickletools.dis() instead
- Files don't persist between container runs → Add volume mount instructions

**Verdict:** Ship it as-is. Minor issues have documented workarounds.

---

### ⚠️ Case Study 2: Model Poisoning - NEEDS TESTING

**Status:** Code complete, not tested

**What's Built:**
- ✅ Full ODSCAN implementation adapted for traffic signs
- ✅ Dockerfile created (multi-stage build)
- ✅ Workshop automation scripts (workshop_demo.sh, gold_demo.sh)
- ✅ Complete README_WORKSHOP.md with timing breakdowns
- ✅ Poisoning scripts (poison_data.py, train.py, detect.py, demo.py)

**Attack Flow:**
1. Poison dataset: stop signs + yellow square → relabeled as "yield"
2. Train SSD300/ResNet18 model on poisoned data
3. Demo backdoor: stop + trigger → "yield" prediction (dangerous!)
4. Run Neural Cleanse scanner → detect backdoor + invert trigger
5. Show recovered trigger visualization (yellow square pattern)

**Critical Gaps:**
1. **Docker build untested** - May fail due to:
   - Heavy dependencies (opencv, albumentations, pytorch)
   - Dataset download requirements (Google Drive)
   - CUDA/CPU compatibility issues

2. **Full pipeline untested** - Need to verify:
   - Dataset poisoning works
   - Training completes (or pre-trained models ready)
   - Scanner detects backdoor reliably
   - Visualizations generate correctly

3. **Timing unknown** - Workshop allocates 30 min, but:
   - Training may take too long live
   - Need pre-trained models as backup
   - Scanner runtime unknown

**What to Test (Priority Order):**
1. Docker build (demo-poisoning/build.sh)
2. Dataset setup (check if data/ has required structure)
3. Run workshop_demo.sh (silver path)
4. Run gold_demo.sh (defense path)
5. Check timing for each step
6. Generate pre-trained models for backup

**Recommended Approach:**
- Test Docker build first (may need fixes)
- Use pre-trained models rather than live training
- Pre-generate scanner results as backup
- Focus on demo.py inference (fastest, most impactful)

---

### ❌ Case Study 3: Supply Chain CVEs - NOT BUILT

**Status:** Planned, not implemented

**What's Documented:**
- ✅ DECISIONS.md with clear plan
- ✅ Pre-saved results directory created
- ✅ Smart approach: small Python images for live demo, PyTorch numbers pre-saved

**What to Build:**
1. **scan.sh script** - Automates Grype scans on 3 images:
   - python:3.11 (baseline: ~200+ CVEs)
   - python:3.11-alpine (better: ~20-40 CVEs)
   - cgr.dev/chainguard/python:latest (gold: ~0 CVEs)

2. **Pre-saved scan results** (5 files):
   - results/python-311.txt
   - results/python-311-alpine.txt
   - results/chainguard-python.txt
   - results/pytorch-pytorch.txt (run on corp machine, huge pull)
   - results/chainguard-pytorch.txt

3. **README.md** - Workshop instructions with:
   - Quick grype install (brew install grype)
   - Live scan demo commands
   - Timing breakdown (20 min total)
   - Discussion points: Docker Desktop licensing, minimal base images

**Estimated Build Time:** 1 hour
- 15 min: Write scan.sh script
- 30 min: Run scans, save outputs
- 15 min: Write README.md

**Why This Is Easy:**
- No training, no models, no heavy dependencies
- Just Grype + Docker images
- Most work is pre-generating scan outputs
- Live demo is fast (small images scan in seconds)

---

## Critical Path to Workshop-Ready

### Phase 1: Test Case Study 2 (2 hours)

**Goal:** Verify poisoning demo works end-to-end

1. **Docker Build Test** (30 min)
   ```bash
   cd demo-poisoning
   docker build -t poisoning-demo .
   ```
   - Watch for dependency failures
   - Note build time (may need optimization)
   - Test container starts: `docker run --rm -it poisoning-demo bash`

2. **Dataset Verification** (15 min)
   - Check if data/ exists with required structure
   - Test data loading: `python -c "from dataset import load_data; load_data()"`
   - Document dataset requirements clearly

3. **Silver Path Test** (45 min)
   - Run workshop_demo.sh inside container
   - Verify: poison_data.py creates poisoned dataset
   - Verify: train.py completes (or note time required)
   - Verify: demo.py shows backdoor (stop + trigger → yield)
   - Take screenshots of key outputs

4. **Gold Path Test** (30 min)
   - Run gold_demo.sh inside container
   - Verify: detect.py scanner runs without errors
   - Verify: Inverted trigger image generated
   - Check anomaly index > 2 (backdoor detected)
   - Save scan_results/ as backup

**Deliverable:** Working demo + pre-generated models/results as backup

---

### Phase 2: Build Case Study 3 (1 hour)

**Goal:** Complete supply chain CVE demo

1. **Write scan.sh** (15 min)
   ```bash
   #!/bin/bash
   # Scan Python images and compare CVE counts

   echo "Scanning python:3.11..."
   grype python:3.11 > results/python-311.txt 2>&1

   echo "Scanning python:3.11-alpine..."
   grype python:3.11-alpine > results/python-311-alpine.txt 2>&1

   echo "Scanning cgr.dev/chainguard/python:latest..."
   grype cgr.dev/chainguard/python:latest > results/chainguard-python.txt 2>&1

   # Pretty print comparison
   echo "=== CVE Comparison ==="
   echo "python:3.11:          $(grep -c "CVE" results/python-311.txt) CVEs"
   echo "python:3.11-alpine:   $(grep -c "CVE" results/python-311-alpine.txt) CVEs"
   echo "chainguard/python:    $(grep -c "CVE" results/chainguard-python.txt) CVEs"
   ```

2. **Generate Pre-saved Results** (30 min)
   - Run scans on all 5 images
   - Save full grype outputs to results/
   - Note: pytorch/pytorch may take 10+ min to pull

3. **Write README.md** (15 min)
   - Installation: grype setup
   - Live demo: scan.sh usage
   - Workshop timing: 20 min breakdown
   - Discussion points: Docker Desktop, minimal images

**Deliverable:** Complete Case Study 3 ready to demo

---

### Phase 3: Integration & Polish (1 hour)

**Goal:** Workshop-ready package with all materials

1. **Full Workshop Dry Run** (30 min)
   - Walk through all 3 case studies in order
   - Time each section (12 + 25 + 30 + 20 + 3 = 90 min)
   - Identify bottlenecks or awkward transitions
   - Update WORKSHOP.md with actual timings

2. **Instructor Guide Updates** (15 min)
   - Add backup plans for each case study
   - Document "running ahead" vs "running behind" options
   - Add troubleshooting for common failures
   - Verify all commands in WORKSHOP.md work

3. **Pre-generated Artifacts Checklist** (15 min)
   Create backup files in case live demos fail:
   - [ ] demo-malicious/malicious_model.pt
   - [ ] demo-poisoning/models/clean_model.pt
   - [ ] demo-poisoning/models/poisoned_model.pt
   - [ ] demo-poisoning/scan_results/ (clean + poisoned)
   - [ ] demo-supply-chain/results/ (all 5 scan outputs)
   - [ ] Screenshots of key moments (attack success, scanner detection)

4. **Repository Cleanup** (5 min)
   - Remove worktrees/ (old git worktree artifacts)
   - Clean up .skein/ if not needed
   - Update README.md with latest status
   - Add LICENSE and participant handout

**Deliverable:** Tested, timed, documented workshop ready to ship

---

## Recommendations by Priority

### 🔥 P0 - Must Do Before Workshop

1. **Test Case Study 2 end-to-end** - Only untested component
2. **Build Case Study 3** - Quick win, completes the workshop
3. **Generate all backup artifacts** - Pre-trained models, scan results
4. **Full workshop dry run** - Catch timing/flow issues

### ⚡ P1 - Should Do If Time Permits

5. **Create participant handout** - Quick reference for commands
6. **Add memes** (per proposal) - Make it entertaining
7. **Record video walkthrough** - For self-review and promotion
8. **Test on different machines** - Verify Docker builds work universally

### 💡 P2 - Nice to Have

9. **Optimize Docker builds** - Reduce build time/image size
10. **Add "extra time" content** - Sleepy Pickle, adaptive attacks
11. **Create slides** - Visual aids for intro/discussion
12. **Participant survey** - Feedback form for post-workshop

---

## Risk Assessment

### High Risk (Must Address)

**Case Study 2 untested:**
- **Risk:** Demo fails live at workshop
- **Impact:** 30% of workshop content lost
- **Mitigation:** Test now + create pre-generated backups
- **Time to fix:** 2 hours

**Case Study 3 not built:**
- **Risk:** Workshop incomplete (only 2/3 case studies)
- **Impact:** Missing promised content from proposal
- **Mitigation:** Build now (quick, low complexity)
- **Time to fix:** 1 hour

### Medium Risk (Monitor)

**Large Docker images:**
- **Risk:** Participants struggle with pulls on conference WiFi
- **Impact:** Delays, frustrated participants
- **Mitigation:** Pre-pull instructions, USB stick backup
- **Time to fix:** Document pre-workshop setup (15 min)

**Dataset dependencies:**
- **Risk:** Google Drive download fails or is slow
- **Impact:** Case Study 2 can't use live data
- **Mitigation:** Pre-packaged dataset or synthetic generation
- **Time to fix:** Already using pre-trained models as backup

### Low Risk (Accept)

**Fickling PERSID issue:**
- **Risk:** Can't decompile torch.save() format
- **Impact:** Minor - use pickletools.dis() instead
- **Mitigation:** Already documented in WORKSHOP.md
- **Time to fix:** 0 (workaround exists)

**Timing variations:**
- **Risk:** Some sections run long or short
- **Impact:** Minor - adjust on the fly
- **Mitigation:** "Running ahead/behind" options in instructor guide
- **Time to fix:** Already documented

---

## Key Strengths of This Workshop

### 1. Strong Research Foundation
- 14 research agents completed
- 25+ CVEs documented
- Real-world tools (ODSCAN, SafeTensors, Grype)
- Academic rigor (BadNets, Neural Cleanse papers)

### 2. Practical, Hands-On
- All demos use Docker (reproducible, isolated)
- Real exploits, not toy examples
- Participants run actual attacks and defenses
- Chainguard partnership adds credibility

### 3. Complete Attack → Defense Narrative
- Every case study has silver (vulnerable) and gold (hardened) paths
- Shows attacker perspective AND defender tools
- Actionable takeaways (use SafeTensors, scan datasets, harden containers)

### 4. Well-Scoped
- 90 minutes is tight but achievable
- Each case study self-contained
- Docker makes setup predictable
- Pre-generated artifacts provide safety net

### 5. Engaging Content
- Traffic sign backdoors (visceral: "this could kill someone")
- Live code execution (always a crowd-pleaser)
- CVE numbers comparison (shocking delta)
- Memes (per proposal - entertain to educate)

---

## Potential Pitfalls & How to Avoid

### 1. Live Training Takes Too Long
**Pitfall:** Training a model takes 10+ minutes, kills workshop flow

**Solution:**
- Use pre-trained models by default
- Show training command, explain what it does
- Only train live if running ahead of schedule
- WORKSHOP.md already documents this

### 2. Conference WiFi Fails
**Pitfall:** Docker pulls or dataset downloads fail

**Solution:**
- Pre-workshop email: pull images in advance
- USB stick with images + datasets as backup
- All demos work offline once images are pulled

### 3. Participants Get Lost
**Pitfall:** Commands fail due to typos, environment issues

**Solution:**
- Provide copy-paste scripts (workshop_demo.sh, gold_demo.sh)
- Have TAs circulate to help (if available)
- Focus on demo mode vs full hands-on
- README files in each demo directory

### 4. Time Overruns
**Pitfall:** Q&A or live demos take longer than planned

**Solution:**
- Already have timing adjustments in WORKSHOP.md
- "Running behind" variants skip training, use pre-generated results
- "Running ahead" variants add fickling deep-dive, adaptive attacks
- Practice dry run to calibrate

---

## Next Session Agenda

**If you have 4 focused hours:**

**Hour 1: Test Case Study 2**
- Docker build test (30 min)
- Dataset verification (15 min)
- Quick smoke test of key scripts (15 min)

**Hour 2: Finish Case Study 2 Testing**
- Full silver path (workshop_demo.sh)
- Full gold path (gold_demo.sh)
- Generate backup artifacts (models, scan results)

**Hour 3: Build Case Study 3**
- Write scan.sh script (15 min)
- Run scans, save outputs (30 min)
- Write README.md (15 min)

**Hour 4: Integration & Polish**
- Full workshop dry run (30 min)
- Update WORKSHOP.md with learnings (15 min)
- Repository cleanup (10 min)
- Final review (5 min)

**If you have 2 hours:**
- Test Case Study 2 (Docker + smoke test) - 1 hour
- Build Case Study 3 - 1 hour
- Accept: Integration testing happens during workshop prep

**If you have 1 hour:**
- Build Case Study 3 only - 1 hour
- Accept: Case Study 2 gets tested live (risky but might work)

---

## Files Generated by This Assessment

Stored in `/home/patrick/projects/rsa/implementia/`:
- `ASSESSMENT.md` (this file) - Complete project assessment
- Next: `ACTION_PLAN.md` - Step-by-step task breakdown
- Next: `TESTING_CHECKLIST.md` - Case Study 2 validation steps

---

## Final Verdict

**You're 85% there.** Case Study 1 is solid, Case Study 2 needs testing, Case Study 3 needs building. All three are achievable in a single focused session.

**The foundation is excellent:** Research done, code written, Docker patterns established. You're not starting from scratch - you're finishing and polishing.

**Critical path:** Test CS2 → Build CS3 → Dry run. 3-4 hours to workshop-ready.

**You got this.** 🚀
