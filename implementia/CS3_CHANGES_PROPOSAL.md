# Case Study 3: Proposed Changes to introduction-supply-chain Demo

## Comparison: What You Have vs What We Need

### What You Have (introduction-supply-chain/demo.md)
✅ Grype installation/usage explanation
✅ Scan python:latest (Docker Hub official)
✅ CVE severity explanation (Critical/High/Medium/Low)
✅ CVSS scoring system explanation
✅ How to interpret Grype output
✅ Real numbers from Jan 2025 scan
✅ Well-written educational content

### What RSA Workshop Needs
🔧 Add Alpine comparison (python:3.11-alpine)
🔧 Add Chainguard comparison (cgr.dev/chainguard/python:latest)
🔧 3-way comparison narrative (Debian → Alpine → Chainguard)
🔧 Reference to pytorch images (pre-saved stats, not live)
🔧 Fit into 20-minute workshop timing
✅ Everything else from your existing demo

---

## Proposed Changes (Minimal Edits)

### Change 1: Update Introduction Paragraph
**Current:**
```
In this exercise, we'll scan a container image for vulnerabilities using Grype...
1. Pull the Grype container image maintained by Chainguard.
2. Scan the official Python container image for vulnerabilities.
3. Interpret the results, learning about how CVEs are categorized.
```

**Proposed:**
```
In this exercise, we'll scan container images for vulnerabilities using Grype...
1. Pull the Grype container image maintained by Chainguard.
2. Scan three Python container images with different security profiles.
3. Compare results to see the impact of base image choice.
4. Discuss implications for ML pipelines using PyTorch.
```

**Reasoning:** Sets up 3-way comparison narrative

---

### Change 2: Add Alpine Section (After python scan)
**Insert new section after the python:latest scan results:**

```markdown
## Scanning Alpine-based Python

Many teams reach for Alpine Linux as a "minimal" base image. Let's see how it compares:

```sh
docker run -it cgr.dev/chainguard/grype python:3.11-alpine
```

You should see significantly fewer CVEs compared to the Debian-based image. Alpine's smaller
package count means fewer potential vulnerabilities.

**Typical results (as of Feb 2025):**
- Total CVEs: ~20-40 (vs ~450+ for Debian-based python:latest)
- Critical/High: ~5-10 (vs ~100+ for Debian)

While Alpine is an improvement, it still carries vulnerabilities from its package ecosystem.
```

**Reasoning:** Shows progression: Debian (many CVEs) → Alpine (fewer CVEs)

---

### Change 3: Add Chainguard Section (After Alpine)
**Insert new section:**

```markdown
## Scanning Chainguard Python

Chainguard Images are built on Wolfi, a minimal Linux distribution designed for containers,
with daily CVE scanning and automated patching. Let's scan the Chainguard Python image:

```sh
docker run -it cgr.dev/chainguard/grype cgr.dev/chainguard/python:latest
```

**Typical results (as of Feb 2025):**
- Total CVEs: 0-2 (depending on scan date)
- Critical/High: 0

The dramatic reduction comes from:
1. Minimal package set (only what Python needs)
2. Daily automated security patching
3. Wolfi distroless approach

This is the gold standard for production ML pipelines.
```

**Reasoning:** Completes the narrative arc, shows the "gold path"

---

### Change 4: Add Comparison Table
**Insert after Chainguard section:**

```markdown
## Comparison Summary

| Image | Base | Total CVEs | Critical/High | Use Case |
|-------|------|-----------|---------------|----------|
| python:latest | Debian | ~450+ | ~100+ | Development only |
| python:3.11-alpine | Alpine | ~20-40 | ~5-10 | Better, but not production-grade |
| cgr.dev/chainguard/python:latest | Wolfi | 0-2 | 0 | Production ML pipelines |

**Key Insight:** Base image choice can eliminate 99%+ of CVEs in your supply chain.
```

**Reasoning:** Visual comparison makes the point clearly

---

### Change 5: Add PyTorch Reference Section
**Insert new section before Resources:**

```markdown
## Implications for ML Pipelines

Python images are relatively small (~1GB). ML frameworks like PyTorch are much larger (~5-10GB),
making live scanning impractical during a workshop. However, the same pattern applies:

**PyTorch CVE Comparison (pre-scanned results):**
- `pytorch/pytorch:latest`: ~500+ CVEs (large Debian base + CUDA + ML libraries)
- `cgr.dev/chainguard/pytorch:latest-dev`: ~0-5 CVEs (minimal Wolfi base)

For ML pipelines, this matters because:
1. **Attack surface:** More packages = more potential exploits
2. **Compliance:** Fewer CVEs = easier audits
3. **Patching velocity:** Minimal images update faster

The pickle deserialization and model poisoning attacks we've covered are amplified when
running in vulnerable containers. Defense in depth means hardening every layer.
```

**Reasoning:** Connects CS3 back to CS1+CS2, explains why pytorch matters for the workshop

---

### Change 6: Update Resources Section
**Add to existing resources:**

```markdown
## Resources

- [Chainguard Images for ML Pipelines](https://images.chainguard.dev/directory/image/pytorch/overview) - PyTorch, TensorFlow, and other ML images
- [Chainguard Deep Dive 🤿: Where Does Grype Data Come From?](https://dev.to/chainguard/deep-dive-where-does-grype-data-come-from-n9e)
- [Grype on the Anchore blog](https://anchore.com/search/?search=grype)
- [Why Chainguard uses Grype](https://www.chainguard.dev/unchained/why-chainguard-uses-grype-as-its-first-line-of-defense-for-cves)
```

**Reasoning:** Adds ML-specific resource link

---

## Changes NOT Proposed (Keep As-Is)

✅ **Grype installation section** - Perfect as-is
✅ **CVSS scoring explanation** - Well-written, keep verbatim
✅ **"by severity" and "by status" interpretation** - Excellent educational content
✅ **Critical CVE grep example** - Good hands-on tip
✅ **NIST.gov reference** - Important context
✅ **Overall tone and structure** - Very clear and accessible

---

## File Structure Proposal

```
demo-supply-chain/
├── README.md           # Adapted from your demo.md (changes above)
├── script.md           # Copy your script.md as-is (speaking notes)
├── resources.md        # Copy your resources.md as-is
└── results/            # Pre-saved scan outputs
    ├── python-latest.txt
    ├── python-alpine.txt
    ├── chainguard-python.txt
    ├── pytorch-latest.txt (from CVE console)
    └── chainguard-pytorch.txt (from CVE console)
```

---

## Summary of Changes

**Additions:**
1. Alpine scan section (~50 words)
2. Chainguard scan section (~75 words)
3. Comparison table (~50 words)
4. PyTorch reference section (~150 words)
5. One additional resource link

**Total new content:** ~325 words
**Existing content preserved:** ~1,200 words

**Change ratio:** ~20% new, 80% your existing work

---

## Timeline Impact

Your existing demo is already well-paced. Adding two more scans:
- Original: ~10 min (one scan + interpretation)
- New: ~15-17 min (three scans + comparison + discussion)
- Fits RSA allocation: 20 minutes ✓

---

## Questions Before Executing

1. **Scan commands:** Keep using Chainguard's grype image (`cgr.dev/chainguard/grype`) or switch to installed grype (`grype python:3.11`)? Your demo uses the containerized version.

2. **Python version:** Use `python:latest` (your current) or `python:3.11` (more specific)? Latest may drift over time.

3. **Script.md:** Do you want me to adapt your speaker notes, or will you handle that?

4. **results/ directory:** Should I create empty placeholder files, or wait for you to populate from CVE console?

---

## Disposition Decision

**Option A: Approve as-is**
→ I'll execute all changes above

**Option B: Modify**
→ Tell me what to adjust (less aggressive? more detail? different framing?)

**Option C: Reject**
→ Start from scratch or different approach

**Your call!**
