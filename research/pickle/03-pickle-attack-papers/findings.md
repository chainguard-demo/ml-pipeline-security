# Pickle Deserialization Attack Papers with Released Code

Research survey of academic papers and security research on pickle/deserialization attacks in ML contexts, focusing on those with released code suitable for workshop demonstrations.

---

## Tier 1: Papers with Released, Usable Attack Code

These have working implementations that could be adapted for workshop demos.

### 1. Sleepy Pickle — Trail of Bits (June 2024)

- **Title:** "Exploiting ML Models with Pickle File Attacks" (Parts 1 & 2)
- **Authors:** Trail of Bits Research Team (Boyan Milanov, Suha S. Hussain)
- **Type:** Industry research with blog posts (not a traditional academic paper)
- **Repo:** https://github.com/trailofbits/sleepy-pickle-public
- **License:** MIT
- **Blog Post 1:** https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/
- **Blog Post 2:** https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-2/

**Attack Techniques:**
- **Sleepy Pickle:** Injects payload into serialized ML model; modifies model in-place at deserialization time (weights + code hooks). No trace left on disk.
- **Sticky Pickle:** Self-replicating variant that propagates payload to other local pickle files.
- Uses the Fickling library for injection.

**Demo Scenarios in Repo (4 attacks):**
1. **Harmful Outputs (Disinformation):** Uses ROME to inject false medical facts into GPT2-XL
2. **User Data Theft:** Hooks inference function to exfiltrate user data on secret keyword
3. **Phishing Attack:** Injects malicious links into model-generated text summaries
4. **Payload Persistence:** Self-replicating payload that infects other local pickle files

**Workshop Usability: EXCELLENT**
- Well-structured demos with clear code
- MIT licensed
- `pytest -s` to run tests
- Only caveat: LLM demos need significant GPU memory (GPT2-XL)
- Could easily simplify to smaller models for workshop setting

---

### 2. Fickling — Trail of Bits (2021–present, actively maintained)

- **Title:** "Never a Dill Moment: Exploiting Machine Learning Pickle Files" (2021)
- **Authors:** Trail of Bits (Evan Sultanik, Jim Miller)
- **Repo:** https://github.com/trailofbits/fickling
- **License:** LGPL-3.0
- **Talk:** DEF CON AI Village 2021

**Capabilities:**
- Python pickle decompiler, static analyzer, and bytecode rewriter
- Can **create** malicious pickle files with a single CLI command
- Can **inject** arbitrary Python into existing pickle files
- Supports PyTorch formats (v0.1.1 through TorchScript v1.4)
- Safe symbolic execution for analysis (no actual code execution)
- Pickle VM (PM) implementation for bytecode manipulation

**Key Features for Demos:**
- `--inject` flag: inject code into pickle files from CLI
- `--check-safety`: detect malicious content
- `--trace`: safe execution tracing
- `fickling.always_check_safety()`: global hook for safety checking
- Can create polyglot files valid as multiple formats

**Installation:** `pip install fickling` (or `pip install fickling[torch]`)

**Workshop Usability: EXCELLENT**
- The primary offensive/defensive tool in this space
- Simple CLI, easy to demo
- Active maintenance (new ML scanner added Sept 2025)
- Great for both attack creation and defense demos

---

### 3. PickleBall — Columbia University (CCS 2025)

- **Title:** "PickleBall: Secure Deserialization of Pickle-based Machine Learning Models"
- **Authors:** Kellas, Christou, Tao, Dolan-Gavitt, Davis, Torres-Arias
- **Venue:** ACM CCS 2025 (Distinguished Artifact Award)
- **arXiv:** https://arxiv.org/abs/2508.15987
- **Repo:** https://github.com/columbia/pickleball
- **Artifact:** https://zenodo.org/records/16974645 (includes malicious model datasets)
- **PDF:** https://cs.brown.edu/~vpk/papers/pickleball.ccs25.pdf

**Key Contributions:**
- Static analysis of ML library code to compute custom safe-loading policies
- Drop-in replacement for pickle module during model loading
- **Dataset of malicious models included in artifact** — very useful for demos
- Correctly loads 79.8% of benign models while rejecting 100% of malicious ones
- Showed that model scanners (picklescan, modelscan) have both false positives and false negatives

**Attack Surface Analysis:**
- 44.9% of popular Hugging Face models still use insecure pickle format
- 15% cannot be loaded by restrictive policies
- Identifies specific bypass techniques against existing scanners

**Workshop Usability: VERY GOOD**
- Primarily a defensive tool, but the **malicious model dataset** is gold for demos
- Award-winning artifact means good code quality
- Can demonstrate both attack detection and defense

---

### 4. MalHug — "Models Are Codes" (ASE 2024)

- **Title:** "Models Are Codes: Towards Measuring Malicious Code Poisoning Attacks on Pre-trained Model Hubs"
- **Authors:** Jian Zhao, Shenao Wang, Yanjie Zhao, Xinyi Hou, Kailong Wang, et al.
- **Venue:** IEEE/ACM ASE 2024
- **arXiv:** https://arxiv.org/abs/2409.09368
- **Repo:** https://github.com/security-pride/MalHug

**Key Contributions:**
- MalHug detection pipeline for malicious models on Hugging Face
- Scanned 705K models and 176K datasets (as of July 2024)
- Found 100 malicious repositories (91 models, 9 datasets)
- Taxonomy of attack vectors through model hubs

**Workshop Usability: GOOD**
- Detection pipeline code available
- Real-world malicious model examples documented
- More focused on measurement than attack creation

---

### 5. Pickle-Fuzzer — Cisco AI Defense (Dec 2025)

- **Title:** "Breaking the Jar: Hardening Pickle File Scanners with Structure-Aware Fuzzing"
- **Authors:** Cisco AI Defense Team
- **Repo:** https://github.com/cisco-ai-defense/pickle-fuzzer
- **Blog:** https://blogs.cisco.com/ai/hardening-pickle-file-scanners

**Capabilities:**
- Structure-aware fuzzer that generates adversarial pickle files
- Tests scanner robustness by finding bypass techniques
- Written in Rust, with Python API
- Integrates with coverage-guided fuzzers (Atheris)
- Can generate single files or entire corpus with mutations

**Installation:** `cargo install pickle-fuzzer`

**Workshop Usability: GOOD**
- Great for demonstrating how scanners can be bypassed
- Generates adversarial pickle files automatically
- Needs Rust toolchain

---

## Tier 2: Papers with Partial/Defensive Code

### 6. The Art of Hide and Seek / PickleCloak (Aug 2025)

- **Title:** "The Art of Hide and Seek: Making Pickle-Based Model Supply Chain Poisoning Stealthy Again"
- **Authors:** Tong Liu, Meng, et al.
- **arXiv:** https://arxiv.org/abs/2508.19774
- **Code: NOT publicly released** (no GitHub repo found as of this writing)

**Key Contributions (most comprehensive attack surface analysis):**
- **PickleCloak** framework: automated gadget discovery + exploit generation
- Identifies 22 exploitable pickle-based model loading paths (19 missed by all scanners)
- 9 Exception-Oriented Programming (EOP) instances (7 bypass all scanners)
- 133 exploitable gadgets with ~100% bypass rate
- Uses LLM-based semantic reasoning for automatic gadget discovery
- Received $6000 bug bounty from vendors

**Attack Techniques:**
- Exception-Oriented Programming (EOP): exploits discrepancy between PyTorch's custom Zip extractor and scanners' Python ZipFile library
- Indirect callable invocation to bypass denylists
- Dynamic runtime payload loading

**Workshop Usability: LIMITED (no code released)**
- Paper is the most comprehensive attack surface analysis available
- Techniques described in detail, could be reimplemented
- Would be excellent reference material for workshop content

---

### 7. Large-Scale Exploit Instrumentation Study (Oct 2024)

- **Title:** "A Large-Scale Exploit Instrumentation Study of AI/ML Supply Chain Attacks in Hugging Face Models"
- **Authors:** Beatrice Casey, Joanna C. S. Santos, Mehdi Mirakhorli
- **arXiv:** https://arxiv.org/abs/2410.04490
- **Code: Unknown** (no public repo found)

**Key Contributions:**
- Demonstrates exploitation approach on Hugging Face models
- Investigates Hugging Face's ability to flag unsafe serialization
- Develops detection technique for malicious models

**Workshop Usability: LIMITED**
- Good reference for understanding the threat landscape
- Methodology could inform demo design

---

### 8. Zero-Trust AI Model Security (March 2025)

- **Title:** "Zero-Trust Artificial Intelligence Model Security Based on Moving Target Defense and Content Disarm and Reconstruction"
- **arXiv:** https://arxiv.org/abs/2503.01758
- **Code: Unknown**

**Key Contributions:**
- Content Disarm and Reconstruction (CDR) for disarming pickle serialization attacks
- Moving Target Defense (MTD) for protecting model architecture/weights
- Found 95% of attacks target pickle serialization

**Workshop Usability: LIMITED**
- Primarily defensive
- No confirmed code release

---

### 9. A Rusty Link in the AI Supply Chain (May 2025)

- **Title:** "A Rusty Link in the AI Supply Chain: Detecting Evil Configurations in Model Repositories"
- **Authors:** Ziqi Ding, Qian Fu, Junchen Ding, Gelei Deng, Yi Liu, Yuekang Li
- **arXiv:** https://arxiv.org/abs/2505.01067

**Key Contributions:**
- **ConfigScan**: LLM-powered tool to detect malicious model configurations
- First study of malicious configurations (not just pickle files) on Hugging Face
- Three attack scenarios: file, website, and repository operations
- Evaluated on 1,000 samples

**Workshop Usability: MODERATE**
- Adjacent attack vector (configs, not pickle directly)
- Could complement pickle attack demos

---

## Tier 3: Security Tools & Scanner Research (with code)

### 10. Picklescan — Hugging Face's Scanner

- **Repo:** https://github.com/mmaitre314/picklescan
- **Purpose:** Scan pickle files for malicious content (used by Hugging Face)
- **Known Bypass CVEs:**
  - CVE-2025-1716 (Sonatype): RCE via static analysis bypass
  - CVE-2025-1889 (Sonatype): Hidden file detection failure
  - CVE-2025-1944/1945 (Sonatype): ZIP filename/flag manipulation
  - CVE-2025-10155 (JFrog): File extension mismatch bypass
  - CVE-2025-10156 (JFrog): ZIP bad CRC bypass
  - CVE-2025-10157 (JFrog): Submodule import bypass

**Workshop Usability: EXCELLENT for defense demos**
- Show how scanners work and how they fail
- Well-documented bypasses make great attack/defense narratives

---

### 11. ModelScan — ProtectAI

- **Repo:** https://github.com/protectai/modelscan
- **Purpose:** Multi-format model scanner (pickle, H5, SavedModel)
- **Known Issues:** 9 false negatives identified by PickleBall research (denylist gaps, dynamic runtime evasion, premature STOP opcode)

**Workshop Usability: GOOD for defense demos**
- Supports multiple formats
- Notebooks included in repo
- Good for showing denylist limitations

---

### 12. HiddenLayer YARA Rules

- **Repo:** HiddenLayer's public BitBucket (exact URL not confirmed)
- **Research:** "Weaponizing ML Models with Ransomware", "Pickle Strike"
- **Blog:** https://hiddenlayer.com/innovation-hub/weaponizing-machine-learning-models-with-ransomware/

**Key Contributions:**
- Demonstrated ransomware delivery via pickle-serialized ML models
- Embedded shellcode in pickle files for reverse shells
- Created YARA rules for detection
- Found real-world malicious pickle files with Cobalt Strike/Mythic stagers

**Workshop Usability: GOOD**
- YARA rules useful for detection demos
- Ransomware angle makes for compelling workshop narrative

---

## Tier 4: Industry Research (Blog Posts / No Formal Paper)

### 13. NullifAI — ReversingLabs (Feb 2025)

- **Source:** https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face
- **Technique:** Malicious PyTorch models compressed with 7z (instead of ZIP) to bypass picklescan
- **Payload:** Reverse shell connecting to hardcoded IP
- **Workshop Usability:** Good case study, no released code

### 14. Silent Sabotage — HiddenLayer

- **Source:** https://www.hiddenlayer.com/research/silent-sabotage
- **Technique:** Hijacking safetensors conversion on Hugging Face
- **Key Finding:** Could exfiltrate SFConvertbot token, send malicious PRs, implant neural backdoors
- **Workshop Usability:** Good case study for supply chain attack narrative

### 15. Rapid7 — "From .pth to p0wned" (2025)

- **Source:** https://www.rapid7.com/blog/post/from-pth-to-p0wned-abuse-of-pickle-files-in-ai-model-supply-chains/
- **Technique:** Weaponized .pth files with embedded backdoors deploying RATs
- **Finding:** Go-based ELF binary RAT hidden behind Cloudflare Tunnel
- **Workshop Usability:** Compelling real-world case study

### 16. Paws in the Pickle Jar — Splunk SURGe (2023)

- **Source:** https://www.splunk.com/en_us/blog/security/paws-in-the-pickle-jar-risk-vulnerability-in-the-model-sharing-ecosystem.html
- **Key Finding:** 80%+ of ML models use pickle serialization
- **Workshop Usability:** Good for setting the stage/motivation

---

## Recommended Workshop Demo Stack

For a practical workshop on pickle deserialization attacks, I recommend this combination:

### Attack Demo (Offense)
1. **Fickling** — Create malicious pickle files, inject payloads into models (`pip install fickling`)
2. **Sleepy Pickle** — End-to-end attack scenarios (data theft, disinformation, phishing)
3. **PickleBall malicious model dataset** — Real examples of malicious models

### Defense Demo
1. **Picklescan** — Show how scanning works + demonstrate known bypasses (CVEs)
2. **ModelScan** — Multi-format scanning, show denylist limitations
3. **Fickling's scanner mode** — Allowlist-based ML-aware scanning
4. **PickleBall** — Policy-based safe loading

### Scanner Evasion Demo
1. **Cisco pickle-fuzzer** — Generate adversarial pickle files
2. **PickleCloak techniques** (from paper, would need reimplementation) — EOP, gadget chains
3. **JFrog/Sonatype CVEs** — Walk through specific bypass techniques

### Narrative Flow
1. Motivate: 80%+ models use pickle (Splunk), 44.9% on HF still insecure (PickleBall)
2. Attack: Use Fickling to create malicious model, demo Sleepy Pickle scenarios
3. Detect: Run picklescan/modelscan, show they catch basic attacks
4. Evade: Show bypass techniques (CVEs, EOP, gadget chains)
5. Defend: PickleBall policy-based approach, safetensors migration

---

## Summary Table

| Paper/Tool | Year | Code? | Repo URL | Attack/Defense | Workshop Use |
|---|---|---|---|---|---|
| Sleepy Pickle (Trail of Bits) | 2024 | YES | github.com/trailofbits/sleepy-pickle-public | Attack | Excellent |
| Fickling (Trail of Bits) | 2021+ | YES | github.com/trailofbits/fickling | Both | Excellent |
| PickleBall (Columbia/CCS'25) | 2025 | YES | github.com/columbia/pickleball | Defense | Very Good |
| MalHug (ASE'24) | 2024 | YES | github.com/security-pride/MalHug | Detection | Good |
| Pickle-Fuzzer (Cisco) | 2025 | YES | github.com/cisco-ai-defense/pickle-fuzzer | Evasion | Good |
| PickleCloak (Hide & Seek) | 2025 | NO | — | Attack | Limited* |
| Exploit Instrumentation | 2024 | NO | — | Measurement | Limited |
| Zero-Trust AI Model | 2025 | NO | — | Defense | Limited |
| ConfigScan (Rusty Link) | 2025 | UNKNOWN | — | Detection | Moderate |
| Picklescan | ongoing | YES | github.com/mmaitre314/picklescan | Defense | Excellent |
| ModelScan (ProtectAI) | ongoing | YES | github.com/protectai/modelscan | Defense | Good |
| HiddenLayer YARA | 2022+ | PARTIAL | BitBucket (unconfirmed) | Detection | Good |

*PickleCloak paper has the most comprehensive attack surface analysis but code is not released.
