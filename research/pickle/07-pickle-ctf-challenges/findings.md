# Pickle Exploit CTF Challenges & Security Training Materials

Research into CTF challenges, security training labs, and educational repos that use Python pickle deserialization vulnerabilities.

---

## Table of Contents

1. [CTF Challenges by Difficulty](#ctf-challenges-by-difficulty)
2. [Dedicated Training Platforms & Labs](#dedicated-training-platforms--labs)
3. [GitHub Repos & Tools](#github-repos--tools)
4. [Reference Materials & Payload Collections](#reference-materials--payload-collections)
5. [Workshop Adaptability Assessment](#workshop-adaptability-assessment)

---

## CTF Challenges by Difficulty

### Beginner / Easy

#### 1. DownUnderCTF 2020 — "In a Pickle"
- **URL**: [CTFtime writeup](https://ctftime.org/writeup/23496) | [GitHub writeup](https://github.com/jeanettesa/ctf-writeups/blob/master/2020/DownUnderCTF/in_a_pickle/in_a_pickle.md)
- **Difficulty**: Beginner
- **Concept**: Pure deserialization — unpickle a file and decode ASCII values to find the flag
- **Learning value**: Introduction to pickle format, understanding what pickle.loads() does
- **No exploit needed** — just understanding the data format
- **Flag**: `DUCTF{p1ckl3_y0uR_m3554g3}`
- **Workshop fit**: Excellent warm-up exercise. Zero danger, teaches fundamentals.

#### 2. HackTheBox — "Baby Website Rick"
- **URL**: [Writeup](https://braincoke.fr/write-up/hack-the-box/baby-website-rick/) | [0x00sec writeup](https://0x00sec.org/t/pickle-insecure-deserialization-hackthebox-baby-website-rick/27130)
- **Difficulty**: Easy (OWASP Top 10 track)
- **Concept**: Cookie-based insecure deserialization. The site name literally says "insecure deserialization"
- **Learning value**: Recognizing deserialization in cookies, crafting basic `__reduce__` payloads
- **Workshop fit**: Great first "real exploit" exercise

#### 3. angstromCTF 2021 — "Jar"
- **URL**: [CTFtime writeup](https://ctftime.org/writeup/27437)
- **Difficulty**: Easy
- **Concept**: Base64-decoded cookie → `pickle.loads()` → RCE. The `contents` cookie is directly deserialized
- **Learning value**: Classic cookie-based pickle injection, straightforward attack chain
- **Workshop fit**: Good — clean, simple attack surface

#### 4. HTB Cyber Apocalypse 2024 — "Were Pickle Phreaks" (Easy version)
- **URL**: [GitHub source](https://github.com/hackthebox/cyber-apocalypse-2024/blob/main/misc/[Easy]%20Were%20Pickle%20Phreaks) | [Writeup](https://m4rt.pro/blog/htb-cyberapocalypse-2024-were-pickle-phreaks.html) | [Seanedevane writeup](https://seanedevane.com/blog/htb-cyber-apocalypse-2024-pickle-phreaks/)
- **Difficulty**: Easy
- **Concept**: Restricted unpickler with class allowlist (`ALLOWED_PICKLE_MODULES = ['__main__', 'app']`). Bypass via `random._os.system()` since `app.py` imports `random` which internally imports `os` as `_os`
- **Learning value**: Introduction to restricted deserialization and allowlist bypass
- **Source available**: Yes, full challenge source on GitHub
- **Workshop fit**: Excellent — teaches both attack AND defense concepts

#### 5. Valentine CTF — "Pickle Jar"
- **URL**: [Medium writeup](https://medium.com/@satyender.yadav/valentine-ctf-pickle-jar-2b92551510db)
- **Difficulty**: Easy
- **Concept**: Basic pickle deserialization exploit
- **Learning value**: Good introductory challenge
- **Workshop fit**: Good warm-up

### Intermediate

#### 6. RITSEC CTF 2023 — "Pickle Store"
- **URL**: [CTFtime writeup](https://ctftime.org/writeup/36628)
- **Difficulty**: Medium
- **Concept**: Web app with insecure deserialization via cookie. Exploitable through `__reduce__` method to achieve RCE
- **Learning value**: Full web exploitation chain — identify vuln, craft payload, exfiltrate data
- **Workshop fit**: Good — real-world-like web app scenario

#### 7. Wizer CTF — "Profile Page" (Pickle Deserialization RCE)
- **URL**: [Quack writeup](https://quack711.com/posts/wizer-ctf-pickle-deserialization-rce/) | [Aftab Sama writeup](https://www.aftabsama.com/Writeups/CTF/ctfs/wizer_ctf_6_hour_challenge_2024.html)
- **Difficulty**: Medium (4/5 peppers)
- **Concept**: Flask app with `load_object` parameter accepting pickled data. Need to base64-encode payload and use out-of-band exfiltration
- **Learning value**: OOB data exfiltration, OS-specific payloads (Linux vs Windows), real Flask exploitation
- **Flag**: `WIZER{'PICKL1NG_1S_DANGEROUS'}`
- **Workshop fit**: Good — teaches practical exfiltration techniques

#### 8. HackTheBox — "Canape"
- **URL**: [Writeup](https://shreyapohekar.com/blogs/canape-hackthebox-writeup/)
- **Difficulty**: Medium (HTB machine)
- **Concept**: Full machine — initial foothold via Python pickle injection leading to RCE
- **Learning value**: End-to-end exploitation, pickle as part of a larger attack chain
- **Workshop fit**: Too long for a workshop, but good reference

#### 9. HackTheBox — "DLLAMA"
- **URL**: [Medium writeup](https://medium.com/@jacintas/dllama-hackthebox-pickle-deserialization-latex-injection-e58f9f1cb881)
- **Difficulty**: Medium
- **Concept**: Pickle deserialization for authentication bypass (cookie forging) + LaTeX injection with unicode bypass
- **Learning value**: Chaining pickle deserialization with other vulns
- **Workshop fit**: Complex but good for advanced workshops

#### 10. HTB Cyber Apocalypse 2024 — "Were Pickle Phreaks Revenge" (Medium)
- **URL**: [GitHub source](https://github.com/hackthebox/cyber-apocalypse-2024/tree/main/misc/%5BMedium%5D%20Were%20Pickle%20Phreaks%20Revenge) | [Medium writeup](https://darkdrag0nite.medium.com/htb-cyber-apocalypse-2024-were-pickle-phreaks-revenge-f45933d3ee13)
- **Difficulty**: Medium
- **Concept**: Same restricted unpickler concept as Easy version but with additional restrictions. Requires more creative bypass
- **Source available**: Yes, full challenge source on GitHub
- **Learning value**: Deep understanding of pickle internals, creative bypass thinking
- **Workshop fit**: Good progressive difficulty after the Easy version

#### 11. HackTheBox — "Cult of Pickles"
- **URL**: [Medium writeup](https://medium.com/@MaanVader/hackthebox-writeup-cult-of-pickles-5558b35fbebe)
- **Difficulty**: Medium
- **Concept**: Chaining SQL injection with pickle deserialization for flag extraction
- **Learning value**: Multi-vulnerability chaining, real-world attack patterns
- **Workshop fit**: Good for advanced multi-step scenarios

#### 12. Midnight Sun CTF — "Gurkburk"
- **URL**: [Zeyu writeup](https://ctf.zeyu2001.com/2021/midnight-sun-ctf/gurkburk)
- **Difficulty**: Medium
- **Concept**: Pickle exploitation (name is Swedish for "pickle")
- **Learning value**: International CTF perspective on pickle exploits

#### 13. HTB — "Blurry" (PyTorch Pickle)
- **URL**: [daily.dev writeup](https://app.daily.dev/posts/htb-blurry-insecure-deserialization-in-pytorch-and-python-s-pickle-6zdfkokc6)
- **Difficulty**: Medium
- **Concept**: Insecure deserialization in PyTorch model files (which use pickle internally)
- **Learning value**: **Modern/relevant** — ML model supply chain attacks via pickle
- **Workshop fit**: Excellent for connecting pickle exploits to current AI/ML security concerns

### Advanced / Hard

#### 14. Balsn CTF 2019 — "pyshv1/pyshv2/pyshv3"
- **URL**: [CTFtime writeup](https://ctftime.org/writeup/16723) | [GitHub Gist](https://gist.github.com/hellman/b9804ce39ed8c4b1b0bf136459999a61) | [GitHub source](https://github.com/sasdf/ctf/tree/master/tasks/2019/BalsnCTF/misc/pyshv1)
- **Difficulty**: Hard (progressive series)
- **Concept**: Restricted unpickler with increasingly tight restrictions:
  - **pyshv1**: Only `sys` module allowed. Bypass via `sys.modules` dictionary manipulation
  - **pyshv2**: Only `structs` module whitelisted. Bypass via `structs.__builtins__` to overwrite `__import__`
  - **pyshv3**: Even tighter restrictions
- **Learning value**: **Extremely high** — deep pickle VM internals, creative bypass techniques
- **Workshop fit**: Could be a "level 3" progressive challenge series

#### 15. UIUCTF 2024 — "Push and Pickle"
- **URL**: [Medium writeup](https://medium.com/@harryfyx/writeup-uiuctf-2024-push-and-pickle-cf821c49194f) | [CTFtime](https://ctftime.org/writeup/39315) | [GitHub source](https://github.com/sigpwny/UIUCTF-2024-Public)
- **Difficulty**: Hard
- **Concept**: Pickle RCE with blacklist + reverse engineering pickle bytecode and Python bytecode. Uses STACK_GLOBAL opcode. Requires matching Python version (3.9.6) for code object compatibility
- **Learning value**: Deep understanding of pickle VM opcodes, code object internals
- **Solve time**: ~3.5 hours for experienced players
- **Workshop fit**: Too advanced for most workshops, but great demo/reference

#### 16. redpwnCTF 2021 — "Pickled Onions"
- **URL**: [CTFtime writeup](https://ctftime.org/writeup/29142) | [Black-Frost writeup](https://black-frost.github.io/posts/redpwn2021/) | [cor.team writeup](https://cor.team/posts/redpwnctf-2021-pickled-onions/) | [GitHub source](https://github.com/redpwn/redpwnctf-2021-challenges)
- **Difficulty**: Hard (Reversing)
- **Concept**: A **flag checker written entirely in pickle bytecode**. Nested self-unpacking program. Input must be 64 chars, validated through arithmetic checks in pickle opcodes
- **Learning value**: Pickle as a programming language / VM, reversing pickle bytecode
- **Workshop fit**: Good demo of pickle's Turing-complete nature

#### 17. CyberSecurityRumble 2023 — "elkcip"
- **URL**: [Writeup](https://intrigus.org/research/2023/10/29/cyber-security-rumble-finals-ctf-2023-elkcip-writeup/) | [CTFtime](https://ctftime.org/writeup/38088)
- **Difficulty**: Very Hard (2 solves, 500+ points)
- **Concept**: Flag checker in pickle VM using **NAND gates** — 128 equations over 128 variables. Requires SAT/SMT solver. Solver choice dramatically affects solvability
- **Learning value**: Pickle as computation model, SAT solving applied to reversing
- **Workshop fit**: Too hard for workshops, but excellent for talks/demos

#### 18. DEFCON CTF Qualifiers 2023 — "brinebid"
- **URL**: [Washi writeup](https://blog.washi.dev/posts/defcon-brinebid/) | [Korean writeup](https://velog.io/@0range1337/CTF-DEFCON-quals-2023-brinebid)
- **Difficulty**: Very Hard (DEFCON level)
- **Concept**: **Cross-language pickle exploit** — WebSocket server in Deno/JavaScript with a custom Unpickler implementation. Exploit JavaScript's prototype chain via pickle deserialization to get RCE
- **Learning value**: Pickle format beyond Python, prototype pollution, cross-language attacks
- **Workshop fit**: Not for workshops, but fascinating research topic

#### 19. HITB-XCTF 2018 — "Python's Revenge"
- **URL**: [Medium writeup](https://medium.com/@u0x/hitb-xctf-2018-pythons-revenge-web-writeup-7ec4d25872d5)
- **Difficulty**: Hard
- **Concept**: Advanced pickle exploitation in web context
- **Learning value**: Real-world exploitation techniques

#### 20. HackIM 2016 — "Unicle" (Web 200)
- **URL**: [CTFtime writeup](https://ctftime.org/writeup/2319) | [GitHub writeup](https://github.com/bl4de/ctf/blob/master/2016/HackIM_2016/Unicle_Web200/Unicle_Web200_writeup.md)
- **Difficulty**: Medium-Hard
- **Concept**: Early pickle deserialization CTF challenge
- **Learning value**: Historical perspective on how long this vuln class has been in CTFs

#### 21. HackTheBox — "Pickle Panic" (Misc)
- **URL**: [7Rocky writeup](https://7rocky.github.io/en/ctf/htb-challenges/misc/pickle-panic/)
- **Difficulty**: Medium-Hard
- **Concept**: Pickle-based misc challenge
- **Learning value**: Non-web pickle exploitation scenarios

#### 22. Cyber Apocalypse CTF 2022 — "Acnologia Portal"
- **URL**: [HackTheBox blog](https://www.hackthebox.com/blog/acnologia-portal-ca-ctf-2022-web-writeup)
- **Difficulty**: Hard
- **Concept**: Multi-stage: Blind XSS → CSRF → Zip Slip → Flask session cookie forging → Pickle deserialization → RCE
- **Learning value**: Complex attack chain, realistic multi-vuln exploitation
- **Workshop fit**: Too complex for standalone, but individual stages could be extracted

---

## Dedicated Training Platforms & Labs

### 1. OWASP SKF Labs — Deserialization Pickle (1 & 2)
- **Repo**: [github.com/blabla1337/skf-labs](https://github.com/blabla1337/skf-labs)
- **Docker**: `docker run --rm -ti -p 5000:5000 blabla1337/owasp-skf-lab:des-pickle` (version 1)
- **Docker**: `docker run --rm -ti -p 5000:5000 blabla1337/owasp-skf-lab:des-pickle-2` (version 2)
- **Format**: Self-contained Docker labs with vulnerable Flask apps
- **Concept**: Version 1 is basic pickle deserialization. Version 2 involves a "remember me" cookie containing pickled credentials that can be tampered with for RCE
- **Writeup**: [ThirdByte writeup](https://thirdbyte.github.io/owasp-skf-labs-kbid-xxx-deserialisation-pickle-write-up/) | [SKF gitbook](https://owasp-skf.gitbook.io/asvs-write-ups/deserialisation-pickle-2-des-pickle-2/kbid-xxx-des-pickle-2)
- **Workshop fit**: **EXCELLENT** — Docker-based, self-contained, two difficulty levels, OWASP-backed, well-documented

### 2. HTB Academy — Introduction to Deserialization Attacks
- **URL**: [HTB Academy course](https://academy.hackthebox.com/course/preview/introduction-to-deserialization-attacks)
- **Format**: Structured course with hands-on labs
- **Content**: Covers both Python pickle and PHP deserialization. Explains pickle VM (stack + memo), opcodes, and exploitation. Includes skills assessment with two custom websites
- **Related**: [Advanced Deserialization Attacks](https://academy.hackthebox.com/course/preview/advanced-deserialization-attacks) (follow-up course)
- **Workshop fit**: Good reference material; labs are platform-locked though

### 3. HTB Academy — AI Data Attacks
- **URL**: [HTB Academy course](https://academy.hackthebox.com/course/preview/ai-data-attacks)
- **Format**: Structured course
- **Content**: Covers pickle-based attacks on ML pipelines
- **Workshop fit**: Relevant for ML-focused workshops

### 4. SecureFlag — Unsafe Deserialization in Python
- **URL**: [SecureFlag knowledge base](https://knowledge-base.secureflag.com/vulnerabilities/unsafe_deserialization/unsafe_deserialization_python.html)
- **Format**: Platform with labs + knowledge base
- **Content**: Flask endpoint vulnerability, `__reduce__` exploitation, mitigation strategies
- **Workshop fit**: Good educational reference; platform access needed for labs

### 5. YesWeHack Dojo — Insecure Deserialization (Pickle)
- **URL**: [YesWeHack Dojo challenge](https://dojo-yeswehack.com/challenge/play/4a86a433-86a1-4d86-8c0e-9c1792df91c1)
- **Format**: Online interactive challenge
- **Content**: Exploit `pickle.loads()` to achieve RCE and extract flag from environment variables
- **Workshop fit**: Good if platform is accessible

### 6. Snyk CTF-101 — "Sauerkraut"
- **URL**: [GitHub Gist](https://gist.github.com/pythoninthegrass/c93158660e493625e4f8cd78e099c876) | [System Weakness writeup](https://systemweakness.com/snyk-ctf-101-sauerkrautwriteup-46658e984514)
- **Format**: Online CTF challenge
- **Content**: Input field accepting base64-encoded pickle payloads. Classic `__reduce__` exploitation
- **Workshop fit**: Good introductory challenge

### 7. TmmmmmR/python-app Workshop
- **URL**: [GitHub course guide](https://github.com/TmmmmmR/python-app/blob/master/course-guide/insecure-deserialization/README.md)
- **Format**: Workshop/course guide with code examples
- **Content**: Covers pickle + YAML deserialization, includes Bandit scanning, designed as a teaching resource
- **Workshop fit**: **EXCELLENT** — specifically designed as a workshop/course

### 8. Moozoi Academy — "Pickle Python Deserialization"
- **URL**: [Moozoi](https://moozoi.com/product/pickle-python-deserialization/)
- **Format**: Commercial training course
- **Content**: Dedicated pickle deserialization training

---

## GitHub Repos & Tools

### Vulnerable Applications (for learning/workshops)

#### CalfCrusher/Python-Pickle-RCE-Exploit
- **URL**: [GitHub](https://github.com/CalfCrusher/Python-Pickle-RCE-Exploit)
- **Content**: Pickle RCE PoC + vulnerable Flask app. Self-contained demo
- **Workshop fit**: **EXCELLENT** — includes both the exploit AND the vulnerable target

#### 4nuxd/pickle-rce-exploit
- **URL**: [GitHub](https://github.com/4nuxd/pickle-rce-exploit)
- **Content**: PoC RCE exploit targeting apps that deserialize untrusted pickle objects
- **Workshop fit**: Good reference exploit code

#### Spades-Ace/Windows-Python-Pickle-Deserialization-Exploit
- **URL**: [GitHub](https://github.com/Spades-Ace/Windows-Python-Pickle-Deserialization-Exploit)
- **Content**: Windows-specific pickle deserialization exploitation demo
- **Workshop fit**: Good for Windows-focused training

#### WangYihang/pickle-pickle
- **URL**: [GitHub](https://github.com/WangYihang/pickle-pickle)
- **Content**: Arbitrary Python code executor via pickle
- **Workshop fit**: Good as a tool demonstration

### Analysis & Security Tools

#### trailofbits/fickling
- **URL**: [GitHub](https://github.com/trailofbits/fickling)
- **Content**: Python pickle decompiler, static analyzer, and bytecode rewriter. Can detect, analyze, reverse engineer, or create malicious pickle files including PyTorch models
- **Performance**: 100% malicious file detection, 99% safe file classification
- **Blog posts**: [AI/ML scanner update](https://blog.trailofbits.com/2025/09/16/ficklings-new-ai/ml-pickle-file-scanner/) | [New features](https://blog.trailofbits.com/2024/03/04/relishing-new-fickling-features-for-securing-ml-systems/)
- **Workshop fit**: **ESSENTIAL TOOL** — great for both analysis and defense portions of a workshop

#### HITCON 2022 — "Pain Pickle: Systematically Bypassing Restricted Unpickler"
- **URL**: [Slides (PDF)](https://hitcon.org/2022/slides/Pain%20Pickle%EF%BC%9A%E7%B3%BB%E7%B5%B1%E5%8C%96%E5%9C%B0%E7%B9%9E%E9%81%8E%20Restricted%20Unpickler.pdf)
- **Content**: Systematic methodology for bypassing restricted unpicklers. Conference talk at HITCON 2022
- **Workshop fit**: Great reference for the "bypass" portion of advanced workshops

### Challenge Source Code Repos

#### hackthebox/cyber-apocalypse-2024
- **URL**: [GitHub](https://github.com/hackthebox/cyber-apocalypse-2024)
- **Content**: Official writeups + source for "Were Pickle Phreaks" (Easy) and "Were Pickle Phreaks Revenge" (Medium)
- **Workshop fit**: **Excellent** — well-structured, two difficulty levels, official source available

#### sigpwny/UIUCTF-2024-Public
- **URL**: [GitHub](https://github.com/sigpwny/UIUCTF-2024-Public)
- **Content**: Challenge source for "Push and Pickle"
- **Workshop fit**: Advanced — for reference

#### redpwn/redpwnctf-2021-challenges
- **URL**: [GitHub](https://github.com/redpwn/redpwnctf-2021-challenges)
- **Content**: Challenge source for "Pickled Onions"

#### jailctf/pyjail-collection
- **URL**: [GitHub](https://github.com/jailctf/pyjail-collection)
- **Content**: Collection of pyjail challenges including pickle-based ones

---

## Reference Materials & Payload Collections

### PayloadsAllTheThings — Python Deserialization
- **URL**: [GitHub](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/Python.md)
- **Content**: Comprehensive payload collection for Python deserialization including pickle
- **Workshop fit**: Essential reference for payload crafting exercises

### HackTricks — Bypass Python Sandboxes
- **URL**: [HackTricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes)
- **Content**: Extensive guide on bypassing Python sandboxes including pickle-based jails
- **Workshop fit**: Good reference for advanced bypass techniques

### David Hamann — "Exploiting Python Pickles"
- **URL**: [Blog post](https://davidhamann.de/2020/04/05/exploiting-python-pickle/)
- **Content**: Clear, concise walkthrough of pickle exploitation basics
- **Workshop fit**: Great pre-reading material for workshop participants

### Nick Frichetten — "Escalating Deserialization Attacks (Python)"
- **URL**: [Blog post](https://frichetten.com/blog/escalating-deserialization-attacks-python/)
- **Content**: Techniques for escalating from basic deserialization to full exploitation
- **Workshop fit**: Good intermediate-to-advanced reference

### MeowMeowAttack — "CTF Notes: Pickle Exploits and Applications"
- **URL**: [Blog post](https://meowmeowattack.github.io/random/2024-06-08/)
- **Content**: Comprehensive notes on pickle exploits collected from CTF experience
- **Workshop fit**: Good study material

### Pyjail Cheatsheet
- **URL**: [Shirajuki's cheatsheet](https://shirajuki.js.org/blog/pyjail-cheatsheet/)
- **Content**: Collected bypass techniques for Python jails, many applicable to pickle
- **Workshop fit**: Reference card for advanced workshops

### Python2+3 Pickle Deserialization Exploit Gist
- **URL**: [GitHub Gist](https://gist.github.com/Reelix/55adb9d2d64f0d2915657dfb30d61510)
- **Content**: Cross-version pickle exploit template
- **Workshop fit**: Good starter template

---

## Workshop Adaptability Assessment

### Recommended Workshop Structure (3-4 hours)

**Level 1: Understanding Pickle (30 min)**
- What is serialization/deserialization?
- Demo: pickle.dumps/loads with safe objects
- Tool: Use `pickletools.dis()` to inspect pickle bytecode
- Exercise: DownUnderCTF "In a Pickle" — just unpickle and decode

**Level 2: Basic Exploitation (45 min)**
- The `__reduce__` method explained
- Craft a simple RCE payload
- Lab: OWASP SKF `des-pickle` Docker lab (version 1)
- Exercise: HTB "Baby Website Rick" or angstromCTF "Jar"

**Level 3: Real-World Web Exploitation (45 min)**
- Cookie-based deserialization attacks
- Base64 encoding payloads, blind/OOB exfiltration
- Lab: OWASP SKF `des-pickle-2` Docker lab OR CalfCrusher's Flask app
- Exercise: RITSEC "Pickle Store" or Wizer "Profile Page"

**Level 4: Restricted Unpickler Bypass (45 min)**
- How RestrictedUnpickler works
- Module allowlists and how to bypass them
- Lab: HTB Cyber Apocalypse "Were Pickle Phreaks" (Easy)
- Advanced: "Were Pickle Phreaks Revenge" (Medium) or Balsn pyshv1

**Level 5: Defense & Detection (30 min)**
- Demo fickling for pickle analysis
- Introduction to safetensors as alternative for ML
- Discuss RestrictedUnpickler patterns and their limitations
- Reference: HITCON 2022 "Pain Pickle" slides

### Top Picks for Workshop Use

| Resource | Why | Setup Effort |
|----------|-----|-------------|
| OWASP SKF des-pickle 1 & 2 | Docker, self-contained, two levels | Low (docker pull) |
| HTB Cyber Apocalypse 2024 Pickle Phreaks | Source on GitHub, Easy+Medium pair | Medium (need to set up) |
| CalfCrusher/Python-Pickle-RCE-Exploit | Includes vuln app + exploit | Low (clone + run) |
| TmmmmmR/python-app workshop | Designed as a course | Low |
| Fickling (Trail of Bits) | Defense/analysis tool | Low (pip install) |
| PayloadsAllTheThings | Payload reference | None (just read) |

### Key Observations

1. **Pickle challenges span the full difficulty spectrum** — from pure data format challenges (beginner) to implementing computation in pickle opcodes (expert)
2. **The "restricted unpickler bypass" subcategory is the richest** — challenges like Were Pickle Phreaks, pyshv1-3, and the HITCON research provide a natural progression
3. **ML/AI angle is increasingly relevant** — PyTorch model poisoning via pickle (HTB Blurry, fickling) connects to current supply chain security concerns
4. **Cross-language exploitation is a frontier** — DEFCON's brinebid (pickle→JavaScript) shows the format's impact beyond Python
5. **Docker-based labs are the most workshop-friendly** — OWASP SKF labs can be spun up instantly, no infrastructure needed
6. **Progressive difficulty series exist naturally** — Were Pickle Phreaks Easy→Revenge, Balsn pyshv1→2→3, OWASP des-pickle→des-pickle-2
