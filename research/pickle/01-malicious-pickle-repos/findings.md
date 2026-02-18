# Malicious Pickle Exploit Repos & POCs - Research Findings

**Date:** 2026-02-17
**Focus:** GitHub repos demonstrating malicious pickle exploits, especially ML/PyTorch-related, suitable for a 25-min hands-on workshop

---

## Tier 1: Best for Workshop Use

### 1. CalfCrusher/Python-Pickle-RCE-Exploit
- **URL:** https://github.com/CalfCrusher/Python-Pickle-RCE-Exploit
- **What it does:** Complete end-to-end pickle RCE demo with a vulnerable Flask app + exploit script
- **Files:** `app.py` (vulnerable Flask app), `Pickle-PoC.py` (exploit), `THM_pickle_owasp10_room.py` (TryHackMe variant)
- **License:** GPL-2.0
- **Workshop suitability:** ★★★★★ — Perfect for 25-min workshop. Quick setup (pip install Flask), run vulnerable app, run exploit. Shows the complete attack chain: `__reduce__` → `os.system` → RCE. Participants can modify the payload.
- **Limitations:** Minimal docs; instructor needs to explain pickle mechanics. Python knowledge assumed.

### 2. trailofbits/fickling
- **URL:** https://github.com/trailofbits/fickling
- **What it does:** Python pickle decompiler, static analyzer, and bytecode rewriter. Can inject backdoors into pickle files and scan for malicious content. The go-to offensive+defensive pickle tool.
- **Key features:**
  - Decompile pickle → human-readable Python
  - `--check-safety` for file scanning
  - `--inject "code"` to inject payloads into existing pickle files
  - `--trace` for execution visualization
  - Hook-based runtime protection (`fickling.hook.activate_safe_ml_environment()`)
  - Full PyTorch polyglot file support (v0.1.1 through v1.3 + TorchScript)
- **License:** LGPL-3.0
- **Workshop suitability:** ★★★★★ — Essential tool for both offense and defense demos. Can decompile suspicious pickles, inject payloads, and demonstrate scanning. Works great as the "analysis" step in a workshop pipeline: create malicious pickle → analyze with fickling → show what it found.
- **Note:** Has had its own CVEs (bypasses via `marshal.loads`, `types.FunctionType`, `pty.spawn()`), which itself is educational.

### 3. coldwaterq/pickle_injector
- **URL:** https://github.com/coldwaterq/pickle_injector
- **What it does:** Injects arbitrary Python code into existing pickle files. Originally presented at DEF CON.
- **Key features:**
  - `inject.py existingPickle.pt newBackdooredPickle.pt malware.py` — simple CLI
  - DoS payloads (`billionLaughs.pt`, `billionLaughsAlt.pkl`) — memory exhaustion attacks
  - Model manipulation demos (`forceBatchTrain.py`, `forceDropoutTrain.py`)
  - Includes `secure_alternative.py` showing safer serialization
  - Comes with DEF CON presentation materials (PPT, PDF, demo GIF)
  - Links to a YARA detection rule
- **License:** Not specified
- **Workshop suitability:** ★★★★★ — Excellent. Take a legit `.pt` model file, inject malicious code, load it, boom. The DEF CON materials provide ready-made workshop slides. The `secure_alternative.py` provides the "how to fix it" part.

### 4. trailofbits/sleepy-pickle-public
- **URL:** https://github.com/trailofbits/sleepy-pickle-public
- **What it does:** Demonstrates "Sleepy Pickle" — a hybrid ML exploitation technique that modifies ML models in-place via pickle payload injection. Uses fickling under the hood.
- **Four demo attacks:**
  1. **Harmful Outputs** — Injects false medical facts into GPT2-XL via ROME editing
  2. **Data Theft** — Hooks inference functions to exfiltrate user data via trigger words
  3. **Phishing** — Injects malicious links into model outputs
  4. **Persistence** — Payloads propagate across multiple pickle files
- **License:** MIT
- **Workshop suitability:** ★★★★☆ — Excellent for demonstrating ML-specific risks (not just generic RCE). The model-level attacks are more sophisticated and relevant to AI security. Downside: may need GPU for full experience, and GPT-2 quality makes some attacks less visually impressive.

### 5. coldwaterq/MaliciousPickles
- **URL:** https://github.com/coldwaterq/MaliciousPickles
- **What it does:** Pre-built malicious pickle files demonstrating scanner evasion via "stacked pickles" (multiple pickle objects in one file)
- **Examples:**
  - `TextEmbedding.pt` — Benign baseline (NVIDIA model, stacked pickles)
  - `fickling_system_calc.pt` — Fickling-injected, detectable by scanner
  - `coldwaterq_inject_calc.pt` — Injected into secondary pickle, **evades fickling** detection
  - `coldwaterq_inject_first_calc.pt` — Injected into first pickle, detected by fickling
- **Workshop suitability:** ★★★★☆ — Great for demonstrating scanner limitations. The "stacked pickle" evasion technique is eye-opening: fickling only scans the first pickle in a multi-pickle file, so hiding malicious code in secondary pickles evades detection.

---

## Tier 2: Useful Supporting Resources

### 6. gousaiyang/pickleassem
- **URL:** https://github.com/gousaiyang/pickleassem
- **What it does:** Pickle assembler for handcrafting pickle bytecode programmatically
- **Key example:**
  ```python
  pa = PickleAssembler(proto=4)
  pa.push_mark()
  pa.util_push('cat /etc/passwd')
  pa.build_inst('os', 'system')
  payload = pa.assemble()
  ```
- **Code quality:** Well-tested (flake8, mypy, bandit, CI/CD)
- **Workshop suitability:** ★★★★☆ — Great for teaching pickle VM internals. Methods map directly to opcodes, bridging theory and exploitation. More educational depth than just `__reduce__`.

### 7. j0lt-github/python-deserialization-attack-payload-generator ("Peas")
- **URL:** https://github.com/j0lt-github/python-deserialization-attack-payload-generator
- **What it does:** Generates serialized payloads for deserialization RCE attacks across multiple formats: pickle, PyYAML, ruamel.yaml, jsonpickle
- **Stats:** 126 stars, 24 forks, GPL-3.0
- **Integration:** Works with msfvenom for generating backdoor payloads
- **Workshop suitability:** ★★★☆☆ — Good if you want to show pickle alongside other deserialization attacks. Broader scope means less pickle depth. More of a pentest tool than educational demo.

### 8. doyensec/r2pickledec
- **URL:** https://github.com/doyensec/r2pickledec
- **What it does:** Pickle decompiler plugin for Radare2. First pickle decompiler supporting the entire instruction set.
- **Commands:** `pdP` (decompile), `pdPj` (AST as JSON), `pdPf` (create flags from variable names)
- **Workshop suitability:** ★★★☆☆ — Great for deep reverse engineering of pickle files but requires radare2 knowledge. Better for advanced audiences. Useful for showing pickle as "compiled bytecode" in a RE framework.

### 9. mmaitre314/picklescan
- **URL:** https://github.com/mmaitre314/picklescan
- **What it does:** Security scanner for detecting malicious pickle files. Used by Hugging Face.
- **Workshop suitability:** ★★★★☆ — Essential for the "defense" side of the workshop. Show participants how to scan pickle files, then demonstrate the many bypass techniques (CVE-2025-1716, CVE-2025-1889, CVE-2025-1945, CVE-2025-10155/10156/10157).
- **Known bypasses:** File extension mismatch, ZIP CRC corruption, submodule imports, `pip.main()`, hidden files in PyTorch archives.

### 10. CarlosG13/CVE-2021-33026
- **URL:** https://github.com/CarlosG13/CVE-2021-33026
- **What it does:** Flask-Caching pickle RCE via Memcached poisoning. Real-world CVE exploit.
- **Workshop suitability:** ★★☆☆☆ — Interesting real-world example but requires Memcached setup. More complex attack chain than needed for a 25-min session.

---

## Tier 3: Reference / Supplementary

### 11. 4nuxd/pickle-rce-exploit
- **URL:** https://github.com/4nuxd/pickle-rce-exploit
- **What it does:** PoC RCE targeting a specific vulnerable endpoint. Includes auto-enumeration and flag extraction (CTF-oriented).
- **Workshop suitability:** ★★☆☆☆ — Too endpoint-specific. Designed for a particular CTF challenge, not general education.

### 12. Spades-Ace/Windows-Python-Pickle-Deserialization-Exploit
- **URL:** https://github.com/Spades-Ace/Windows-Python-Pickle-Deserialization-Exploit
- **What it does:** Fork/variant of CalfCrusher's exploit, modified for Windows environments.
- **Workshop suitability:** ★★☆☆☆ — Only useful if workshop is Windows-specific. Otherwise, CalfCrusher's original is better.

### 13. francescolacerenza/evilPick
- **URL:** https://github.com/francescolacerenza/evilPick
- **What it does:** Automates pickle exploit crafting from Python code files. Uses marshal + base64 + pickle opcodes.
- **Workshop suitability:** ★★☆☆☆ — Python 2.7 only, dated, minimal activity. Interesting technique but too niche.

### 14. pjcampbe11/Pickle-File-Attacks
- **URL:** https://github.com/pjcampbe11/Pickle-File-Attacks
- **What it does:** Documentation-only repo describing Sleepy Pickle and Sticky Pickle attacks. No runnable code.
- **Workshop suitability:** ★☆☆☆☆ — Reading material only. Use Trail of Bits' actual repos instead.

---

## Key Gists

### mgeeky's Pickle RCE Template
- **URL:** https://gist.github.com/mgeeky/cbc7017986b2ec3e247aab0b01a9edcd
- **What:** Minimal Python RCE payload template using `__reduce__` + `os.system`. Python 2 (needs adaptation for Python 3).
- **Use:** Good quick reference for crafting payloads from scratch.

### 0xBADCA7's cPickle Exploit Generator
- **URL:** https://gist.github.com/0xBADCA7/f4c700fcbb5fb8785c14
- **What:** Pickle exploit generator gist.
- **Use:** Another minimal reference implementation.

---

## Relevant Blog Posts & Research (with code)

| Source | URL | Why It Matters |
|--------|-----|---------------|
| Trail of Bits | https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/ | Detailed walkthrough with fickling code examples |
| Rapid7 | https://www.rapid7.com/blog/post/from-pth-to-p0wned-abuse-of-pickle-files-in-ai-model-supply-chains/ | Real .pth → RAT attack chain analysis |
| HiddenLayer | https://hiddenlayer.com/research/weaponizing-machine-learning-models-with-ransomware/ | Ransomware via PyTorch ResNet model, weaponization demo |
| JFrog | https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/ | PickleScan zero-day bypasses with code |
| Snyk | https://snyk.io/articles/python-pickle-poisoning-and-backdooring-pth-files/ | .pth backdooring walkthrough |
| Huntr Blog | https://blog.huntr.com/dont-trust-your-model-how-a-malicious-pickle-payload-in-pytorch-can-execute-code | PyTorch-specific payload demo |
| David Hamann | https://davidhamann.de/2020/04/05/exploiting-python-pickle/ | Clear beginner-friendly walkthrough |
| Sonatype | https://www.sonatype.com/blog/bypassing-picklescan-sonatype-discovers-four-vulnerabilities | Four picklescan bypass CVEs with code |

---

## PickleScan Bypass CVEs (Useful for Workshop "Evasion" Section)

| CVE | Technique | Status |
|-----|-----------|--------|
| CVE-2025-1716 | `pip.main()` not blocked by static analysis | Fixed |
| CVE-2025-1889 | Non-standard file extensions bypass PyTorch scanner | Fixed |
| CVE-2025-1945 | ZIP scan bypass | Fixed |
| CVE-2025-10155 | File extension mismatch (PyTorch ext on standard pickle) | Fixed in 0.0.31 |
| CVE-2025-10156 | Bad CRC in ZIP archive halts scanner | Fixed in 0.0.31 |
| CVE-2025-10157 | Submodule imports bypass unsafe globals check | Fixed in 0.0.31 |

---

## Recommended Workshop Structure (25 min)

### Option A: "From Zero to RCE" (Beginner-Friendly)
1. **[3 min] Setup:** Clone CalfCrusher's repo, install Flask
2. **[5 min] Explain:** How pickle's `__reduce__` enables code execution
3. **[5 min] Demo:** Run vulnerable Flask app, execute the exploit
4. **[5 min] Hands-on:** Participants modify the payload (calc, reverse shell, data exfil)
5. **[4 min] Defense:** Scan the pickle with fickling `--check-safety` and picklescan
6. **[3 min] Fix:** Show safetensors as the alternative, demonstrate `fickling.hook`

### Option B: "Poisoned Models" (ML Security Focus)
1. **[3 min] Intro:** Show real Hugging Face malicious model examples
2. **[5 min] Attack:** Use `pickle_injector` to inject code into a real .pt model file
3. **[5 min] Load:** Show `torch.load()` executing the payload
4. **[5 min] Analyze:** Use fickling to decompile and trace the malicious pickle
5. **[4 min] Evasion:** Show the "stacked pickle" bypass from MaliciousPickles repo
6. **[3 min] Mitigate:** `torch.load(weights_only=True)`, safetensors, picklescan

### Option C: "Full Lifecycle" (Advanced)
1. **[2 min] Intro:** Pickle VM basics with pickleassem
2. **[5 min] Craft:** Build a malicious pickle opcode-by-opcode using pickleassem
3. **[5 min] Inject:** Backdoor a PyTorch model using fickling `--inject`
4. **[5 min] Evade:** Demonstrate picklescan bypass (extension mismatch or stacked pickle)
5. **[5 min] Detect:** Use fickling trace + r2pickledec for reverse engineering
6. **[3 min] Mitigate:** Defense-in-depth: `weights_only=True`, safetensors, allowlisting

---

## Key Defensive Tools / Alternatives

| Tool | URL | Purpose |
|------|-----|---------|
| picklescan | https://github.com/mmaitre314/picklescan | Scanner (used by HF) |
| fickling | https://github.com/trailofbits/fickling | Decompiler + scanner + injector |
| safetensors | https://github.com/huggingface/safetensors | Safe serialization alternative (no code execution) |
| `torch.load(weights_only=True)` | PyTorch built-in | Restricts unpickling to tensor data only |
