# Hugging Face & Pickle Security: Community Discussions and Findings

## Overview

Pickle-based serialization is the default format for PyTorch model weights and has been at the center of a sustained, multi-year security crisis on the Hugging Face Hub. This document surveys community discussions, security research, platform responses, and the ongoing migration toward SafeTensors.

---

## 1. The Core Problem: Pickle as an Attack Vector

### Why Pickle Is Dangerous

Python's `pickle` module executes arbitrary code during deserialization. The `__reduce__` method allows attackers to inject arbitrary Python code into the deserialization process. When a user loads a malicious model via `torch.load()`, the payload executes silently.

Key dangerous opcodes: `STACK_GLOBAL`, `GLOBAL`, and `REDUCE` — these allow importing modules and calling functions during unpickling.

**Source**: [HF Pickle Scanning Documentation](https://huggingface.co/docs/hub/en/security-pickle)

### Scale of the Problem

- **4.47 million unique model versions** scanned by Protect AI as of April 2025
- **352,000 unsafe/suspicious issues** identified across **51,700 models**
- **~100 malicious models** found by JFrog in a single scan sweep (March 2024)
- The Hugging Face Hub hosts **over 2 million models**, many still using pickle format

**Sources**:
- [Protect AI + HF 6-Month Report](https://huggingface.co/blog/pai-6-month)
- [Dark Reading: 100 Malicious Models](https://www.darkreading.com/application-security/hugging-face-ai-platform-100-malicious-code-execution-models)

---

## 2. Documented Malicious Model Incidents

### JFrog Discovery (March 2024): ~100 Malicious Models

JFrog Security Research found approximately 100 models with malicious functionality on Hugging Face. Key examples:

- **`baller423/goober2`** — PyTorch model containing a reverse shell payload targeting IP 210.117.212.93 (KREOnet, South Korea), port 4242. Deleted after discovery.
- **`star23/baller13`** — Same payload structure targeting IP 136.243.156.120, port 53252. Model card explicitly warned "DO NOT DOWNLOAD."

Payloads used `__reduce__` method injection to establish reverse shell connections with platform detection (Windows/Linux), socket connections, and multi-threaded persistent access.

**Source**: [JFrog Blog: Data Scientists Targeted](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)

### ReversingLabs "nullifAI" Discovery (February 2025)

Two malicious models evaded Picklescan using a novel technique:
- Models were compressed using **7z format instead of ZIP** (PyTorch's default)
- This prevented `torch.load()` from loading them normally, but Picklescan also failed to flag them
- The broken pickle files could still be partially deserialized, executing malicious code before the scanner threw errors
- Named the technique **"nullifAI"**

**Sources**:
- [ReversingLabs Blog](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [The Hacker News](https://thehackernews.com/2025/02/malicious-ml-models-found-on-hugging.html)

### MTEB Leaderboard Concern (Community Forum)

Community members flagged that a model at the top of the MTEB (Massive Text Embedding Benchmark) leaderboard was distributed in pickle format. Concern: an attacker could train on the test set to game the leaderboard, then embed malicious code in the pickle file — users trusting leaderboard rankings would be prime targets.

**Source**: [HF Forum Discussion](https://discuss.huggingface.co/t/malicious-code-at-top-of-huggingface-leaderboard/99682)

---

## 3. PickleScan: HF's Scanner and Its Bypasses

### How PickleScan Works

Hugging Face uses [PickleScan](https://github.com/mmaitre314/picklescan) to scan every uploaded file. It:
- Extracts the list of imports referenced in pickle files using `pickletools.genops` (without executing code)
- Displays import lists alongside files on the Hub
- Flags suspicious imports (e.g., `__builtin__.exec`, `__builtin__.eval`)

### Known Bypasses (Multiple CVEs)

PickleScan has been repeatedly bypassed, undermining its value as a security gate:

**CVE-2025-10155 (CVSS 9.3)** — File Extension Mismatch Bypass
- Attackers rename malicious pickle files with PyTorch extensions (`.bin`, `.pt`)
- PickleScan attempts PyTorch-specific parsing which fails on standard pickle files
- PyTorch loads the file successfully by detecting actual format from contents

**CVE-2025-10156 (CVSS 9.3)** — CRC Bypass in ZIP Archives
- Intentional CRC errors in ZIP archives cause PickleScan to fail entirely
- PyTorch skips CRC checks (compiled with `-DMINIZ_DISABLE_ZIP_READER_CRC32_CHECKS`)
- Scanner halts; loader proceeds with malicious code

**CVE-2025-10157 (CVSS 9.3)** — Unsafe Globals Bypass via Subclass Imports
- PickleScan blocklist matches exact module names
- Attackers use subclasses of dangerous imports (e.g., `asyncio.unix_events._UnixSubprocessTransport` instead of direct `asyncio`)
- Flagged as "Suspicious" rather than "Dangerous"

**Checkmarx "Free Hugs" Series**: Demonstrated combining blocklist bypass with `Bdb.run` (instead of `exec`) and optimized protocol 4 to fully bypass PickleScan. Concluded: *"Malicious model scanners simply cannot be trusted to effectively detect and warn against malicious models, as a block-list approach to completely dynamic code... allows attackers to leave these solutions in the dust."*

**Fixed**: PickleScan version 0.0.31 (September 2025) addressed the JFrog CVEs. Timeline: reported June 29, 2025; fixed September 2, 2025.

**Sources**:
- [JFrog: 3 Zero-Day PickleScan Vulnerabilities](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)
- [Checkmarx: Free Hugs Part 2](https://checkmarx.com/blog/free-hugs-what-to-be-wary-of-in-hugging-face-part-2/)
- [GitHub Advisory GHSA-f7qq-56ww-84cr](https://github.com/mmaitre314/picklescan/security/advisories/GHSA-f7qq-56ww-84cr)

---

## 4. Infrastructure-Level Attacks via Pickle

### Wiz Research: Cross-Tenant Access (2024)

Wiz researchers demonstrated that pickle-based models could compromise Hugging Face's inference infrastructure:

1. Uploaded a private pickle-based model with a reverse shell payload
2. Loaded it via the Inference API, achieving shell access
3. Found themselves in a pod on Amazon EKS
4. Demonstrated cross-tenant access to other customers' models
5. Could overwrite images in a shared container registry

**HF Response**: Resolved all issues, partnered with Wiz on ongoing security.

**Sources**:
- [Wiz Blog](https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure)
- [HF Blog: Wiz Partnership](https://huggingface.co/blog/hugging-face-wiz-security-blog)

### HiddenLayer "Silent Sabotage": SafeTensors Conversion Bot Compromise (February 2024)

HiddenLayer demonstrated that the SafeTensors conversion bot itself could be weaponized:

- The conversion service ran in Hugging Face Spaces (user-controlled containers), not hardened infrastructure
- By submitting a crafted malicious PyTorch model for conversion, an attacker could execute code within the bot's environment
- Could steal the bot's authentication token to submit malicious PRs to **any** repository
- The bot had made **42,657+ pull requests** to repositories, any of which could have been compromised
- Out of top-10 downloaded models from Google and Microsoft that accepted the bot's PRs: **16.3M downloads/month**

**Key quote**: The attack required "nothing but a hijacked model that the bot was designed to convert."

**Sources**:
- [HiddenLayer: Silent Sabotage](https://hiddenlayer.com/innovation-hub/silent-sabotage/)
- [The Hacker News](https://thehackernews.com/2024/02/new-hugging-face-vulnerability-exposes.html)

---

## 5. SafeTensors: The Solution and Its Adoption

### What SafeTensors Is

SafeTensors is a simple, safe serialization format developed by Hugging Face:
- Stores only tensor data (header + raw binary), **no code execution possible**
- Written in Rust (language-level exploit mitigations)
- ~100x faster loading on CPU
- Supports lazy loading (load only needed tensors)
- Framework-agnostic (PyTorch, TensorFlow, JAX, PaddlePaddle, NumPy)

### Security Audit (May 2023)

- **Audited by**: Trail of Bits (external security firm)
- **Commissioned by**: Hugging Face, EleutherAI, Stability AI
- **Result**: No critical security flaws leading to arbitrary code execution
- Minor issues found and fixed (spec imprecisions, missing validation for polyglot files)
- Full report published: [Trail of Bits Audit](https://huggingface.co/datasets/safetensors/trail_of_bits_audit_repot/resolve/main/SOW-TrailofBits-EleutherAI_HuggingFace-v1.2.pdf)

**Source**: [HF Blog: SafeTensors Security Audit](https://huggingface.co/blog/safetensors-security-audit)

### Migration Status and Adoption

**Default format transition**:
- SafeTensors became the **default save format** in HF Transformers library
- Diffusers library loads `.safetensors` automatically if available
- `use_safetensors=True` parameter available to force safe loading

**Conversion infrastructure**:
- [SafeTensors Convert Space](https://huggingface.co/spaces/safetensors/convert) — automated conversion tool
- Bot has opened 42,657+ PRs for conversion
- **Low merge rate (~13.9%)** per academic study — many developers ignore conversion PRs

**Academic findings** (Casey et al., January 2025, University of Notre Dame):
- Study: *"An Empirical Study of Safetensors' Usage Trends and Developers' Perceptions"*
- Developers are increasingly adopting safetensors
- Many conversions are automated rather than manual
- Developers show initial hesitancy but gradual progression toward adoption
- Five themes in discussions: security concerns with pickle, safetensors improvements, application-specific usage, adaptation difficulties, and technical errors

**Early adopters**: Civitai, Stable Diffusion Web UI, dfdx, LLaMA.cpp, EleutherAI

**Sources**:
- [HF Docs: Convert Weights](https://huggingface.co/docs/safetensors/en/convert-weights)
- [arxiv: 2501.02170](https://arxiv.org/abs/2501.02170)
- [GitHub Issue #25992: push_to_hub format](https://github.com/huggingface/transformers/issues/25992)

---

## 6. PyTorch's Own Response: weights_only=True

PyTorch has taken parallel action to mitigate pickle risks:

- **PyTorch 1.13 (Nov 2022)**: Introduced `weights_only` parameter for `torch.load()`
- **PyTorch 2.4 (2024)**: Started emitting `FutureWarning` about the upcoming default change
- **PyTorch 2.6 (Late 2024)**: Flipped default to `weights_only=True`

When `weights_only=True`: only tensors, primitive types, dictionaries, and explicitly allowlisted types can be loaded. Arbitrary objects are rejected.

**Limitation**: ~15% of pickle-only model repositories on HF contain models that **cannot be loaded** by the weights-only unpickler, indicating real compatibility friction.

**Sources**:
- [PyTorch Issue #52181](https://github.com/pytorch/pytorch/issues/52181)
- [PyTorch Dev Discussion: BC-Breaking Change](https://dev-discuss.pytorch.org/t/bc-breaking-change-torch-load-is-being-flipped-to-use-weights-only-true-by-default-in-the-nightlies-after-137602/2573)

---

## 7. Community Perspectives and Ongoing Concerns

### Key Community Sentiments

**Distrust of blocklist scanning**: Multiple researchers (Checkmarx, JFrog, ReversingLabs) have independently demonstrated that PickleScan's blocklist approach is fundamentally insufficient. As Karlo Zanki (ReversingLabs) noted: *"blacklists are basic security features"* that cannot adapt to *"known threats morph—and new threats emerge."*

**Desire to eliminate pickle entirely**: Forum discussions show users wanting to avoid pickle files altogether and only use SafeTensors. However, many legacy models remain pickle-only.

**False sense of security from "safe" labels**: The HF Hub displays safety indicators, but multiple bypasses mean models marked as scanned may still be malicious. The HF docs explicitly disclaim: *"this is not 100% foolproof."*

**Conversion friction**: The low merge rate (~13.9%) on automated SafeTensors conversion PRs suggests either lack of awareness, lack of trust in the conversion process, or simple inattention from model maintainers.

**Supply chain trust problem**: The HiddenLayer "Silent Sabotage" research showed that even the mechanism designed to make models safer (the conversion bot) could itself be compromised — a meta-level supply chain risk.

### HF Forum Thread Highlights

- Discussion about models at the top of trusted leaderboards using pickle format
- Reports of datasets falsely flagged as "Pickle.Malware" (false positive friction)
- Questions about whether the SafeTensors conversion space itself has vulnerabilities
- User requests for clearer guidance on which models to trust

**Sources**:
- [HF Forum: Malicious Code at Top of Leaderboard](https://discuss.huggingface.co/t/malicious-code-at-top-of-huggingface-leaderboard/99682)
- [HF Forum: Vulnerability in SafeTensors Conversion Space](https://discuss.huggingface.co/t/vulnerability-in-safetensors-conversion-space/76509)
- [CyberScoop: Plagued by Vulnerable Pickles](https://cyberscoop.com/hugging-face-platform-continues-to-be-plagued-by-vulnerable-pickles/)

---

## 8. Hugging Face's Mitigation Stack (Current State)

| Layer | Mechanism | Limitations |
|-------|-----------|-------------|
| **Pickle Import Scanning** | PickleScan extracts imports via `pickletools.genops` | Multiple bypass CVEs; blocklist is incomplete |
| **ClamAV Antivirus** | Scans all uploaded files | Does not cover pickle-specific exploits |
| **Protect AI Guardian** | Deep structure analysis of serialized code | Newer; still building coverage |
| **SafeTensors Default** | Default save format in Transformers | Legacy models remain in pickle; conversion PR merge rate low |
| **Import Display** | Shows pickle imports on model pages | Requires users to inspect; no guarantee of completeness |
| **Signed Commits** | GPG-signed commits for provenance | Doesn't guarantee file safety, only origin |
| **`weights_only=True`** | PyTorch-side mitigation | Breaks ~15% of pickle-only models |

### HF's Official Recommendations (from docs)

1. Load models from users/organizations you trust
2. Use signed commits
3. Load from TF/Flax formats with `from_tf=True` auto-conversion
4. Use `use_safetensors=True` parameter
5. Use SafeTensors format wherever possible

---

## 9. Academic Research

### PickleBall (CCS 2025)

A secure deserialization framework for pickle-based ML models from Brown University. Addresses the gap between "ban pickle entirely" (impractical) and "scan pickle files" (insufficient).

**Source**: [arxiv: 2508.15987](https://arxiv.org/html/2508.15987v1)

### The Art of Hide and Seek (2025)

Research on making pickle-based model supply chain poisoning stealthy, demonstrating ongoing attacker innovation.

**Source**: [arxiv: 2508.19774](https://arxiv.org/html/2508.19774v1)

### Palo Alto Unit 42: RCE with Modern AI/ML Formats

Broader study of remote code execution vulnerabilities across AI/ML serialization formats and libraries.

**Source**: [Unit 42 Research](https://unit42.paloaltonetworks.com/rce-vulnerabilities-in-ai-python-libraries/)

---

## 10. Key GitHub Issues and PRs

| Issue | Repository | Topic |
|-------|-----------|-------|
| [#52181](https://github.com/pytorch/pytorch/issues/52181) | pytorch/pytorch | Safe loading of weights by default |
| [#25992](https://github.com/huggingface/transformers/issues/25992) | huggingface/transformers | push_to_hub saves .bin instead of safetensors |
| [#28863](https://github.com/huggingface/transformers/issues/28863) | huggingface/transformers | Saving as binary instead of safetensors |
| [#120](https://github.com/huggingface/safetensors/issues/120) | huggingface/safetensors | Converting back to pickle (PyTorch) |
| [Discussion #272](https://github.com/huggingface/safetensors/discussions/272) | huggingface/safetensors | Converting pickle to safetensors |
| [#1407](https://github.com/huggingface/hub-docs/issues/1407) | huggingface/hub-docs | Add malware/pickle scanning attributes to API |
| [#2249](https://github.com/huggingface/pytorch-image-models/issues/2249) | huggingface/pytorch-image-models | Resolve `weights_only=False` warning |

---

## 11. Timeline of Key Events

| Date | Event |
|------|-------|
| **2020** | Python pickle attacks documented in security research community |
| **2022 Nov** | PyTorch 1.13 introduces `weights_only` parameter |
| **2022** | Hugging Face begins developing SafeTensors |
| **2023 May** | Trail of Bits audit of SafeTensors — no critical flaws found |
| **2023** | SafeTensors integrated as core dependency in HF Transformers |
| **2024 Feb** | HiddenLayer "Silent Sabotage" — conversion bot compromise demonstrated |
| **2024 Mar** | JFrog discovers ~100 malicious models on HF Hub |
| **2024** | Wiz demonstrates cross-tenant attacks via pickle on HF infrastructure |
| **2024 Oct** | Protect AI + HF Guardian partnership launches |
| **2024 Late** | PyTorch 2.6 flips `weights_only=True` as default |
| **2025 Jan** | Academic study on SafeTensors adoption trends published |
| **2025 Feb** | ReversingLabs discovers "nullifAI" bypass using 7z compression |
| **2025 Jun** | JFrog reports 3 critical PickleScan zero-days (CVEs 2025-10155/10156/10157) |
| **2025 Sep** | PickleScan 0.0.31 released with fixes |
| **2025 Apr** | Protect AI reports 352K unsafe issues across 51.7K models |

---

## 12. Summary Assessment

**The pickle problem on Hugging Face is far from solved.** Despite significant investment in SafeTensors and scanning infrastructure:

1. **Blocklist scanning is fundamentally inadequate** — repeatedly bypassed by security researchers and real attackers
2. **SafeTensors adoption is progressing but slow** — low merge rates on automated conversion PRs, legacy models persist
3. **The attack surface keeps expanding** — new evasion techniques (7z compression, CRC manipulation, subclass imports) outpace defenses
4. **Infrastructure-level risks compound the problem** — even the conversion mechanism designed to move models to safety was itself compromisable
5. **Community trust assumptions are fragile** — leaderboard rankings, download counts, and "scanned" labels can all create false confidence

The ecosystem is in a transitional state: SafeTensors is clearly the correct direction, but the long tail of pickle-format models creates an ongoing security exposure that scanning alone cannot close.
