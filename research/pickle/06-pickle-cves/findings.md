# Pickle-Related CVEs and Security Advisories in ML Frameworks

## Executive Summary

Pickle deserialization vulnerabilities are pervasive across the ML ecosystem. This document catalogs **25+ CVEs** spanning PyTorch, TensorFlow/Keras, scikit-learn/joblib, MLflow, BentoML, LangChain, NumPy, Meta Llama, and the PickleScan detection tool itself. The pattern is consistent: ML frameworks serialize models using Python's pickle (or closely related mechanisms), and loading untrusted models leads to arbitrary code execution.

---

## 1. PyTorch

### CVE-2025-32434 — `torch.load` weights_only=True Bypass (CRITICAL)
- **CVSS**: 9.3 (Critical)
- **Affected**: PyTorch <= 2.5.1
- **Fixed**: PyTorch 2.6.0
- **Discoverer**: Ji'an Zhou
- **Details**: The `weights_only=True` parameter in `torch.load()` was designed as a safety mechanism to restrict deserialization to primitive types (dicts, tensors, lists). An attacker can craft a malicious model file that **bypasses** this protection entirely — the parameter has the opposite of its intended effect. This is devastating because `weights_only=True` was the *recommended mitigation* for all previous pickle risks.
- **Impact**: Any code that followed PyTorch's own security guidance (`weights_only=True`) was still vulnerable. This undermines the entire mitigation story.
- **Sources**: [GitHub Advisory GHSA-53q9-r3pm-6pq6](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6), [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-32434), [Kaspersky](https://www.kaspersky.com/blog/vulnerability-in-pytorch-framework/53311/)

### General `torch.load()` Pickle Risk (No CVE — By Design)
- PyTorch uses pickle by default for model serialization (.pt, .pth files)
- `torch.load()` with default settings executes arbitrary Python code
- PyTorch made `weights_only=True` the default in 2.6.0, but see CVE-2025-32434 above
- **All .pth files from untrusted sources are potential weapons**

---

## 2. TensorFlow / Keras

### CVE-2024-3660 — Keras Lambda Layer Code Injection (CRITICAL)
- **CVSS**: 9.8 (Critical, per CISA-ADP)
- **Affected**: Keras < 2.13
- **Details**: Lambda layers in Keras models contain marshalled Python code. When a model is saved with `Model.save()` or `save_model()`, this code gets serialized. Loading a malicious .h5 model executes arbitrary code with the application's permissions.
- **Key problem**: Keras added `safe_mode=True` as a fix, but **ignores the safe_mode argument when loading legacy H5 format** — malicious H5 models still execute code even with safe_mode enabled.
- **Downgrade attack**: Oligo Security demonstrated that attackers could force models into the legacy format to bypass safe_mode entirely.
- **Sources**: [Oligo Security](https://www.oligo.security/blog/tensorflow-keras-downgrade-attack-cve-2024-3660-bypass), [CERT VU#253266](https://www.kb.cert.org/vuls/id/253266), [JFrog safe_mode bypass](https://jfrog.com/blog/keras-safe_mode-bypass-vulnerability/)

### CVE-2025-49655 — Keras TorchModuleWrapper Unsafe Deserialization
- **Details**: The `TorchModuleWrapper.from_config()` method uses `torch.load()` with `weights_only=False`, falling back to pickle deserialization. Triggered **even when Keras' safe mode is enabled**.
- **Source**: [Wiz](https://www.wiz.io/vulnerability-database/cve/cve-2025-49655)

### CVE-2021-37678 — TensorFlow YAML Deserialization (Related)
- **CVSS**: 7.8
- **Affected**: TensorFlow < 2.3.4, 2.4.x < 2.4.3, 2.5.0
- **Details**: While technically YAML rather than pickle, the same class of vulnerability — `yaml.unsafe_load` allows arbitrary code execution when deserializing Keras models from YAML format.
- **Fix**: YAML format support was removed entirely.
- **Source**: [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-37678)

---

## 3. Meta Llama

### CVE-2024-50050 — Llama-Stack Pickle RCE (CRITICAL)
- **CVSS**: 9.3 (Snyk/CVSS v4), 9.8 (CVSS v3.1) — Meta rated it 6.3 (medium)
- **Affected**: llama-stack < 0.0.41
- **Discoverer**: Oligo Security (reported Sep 29, 2024; patched Oct 10, 2024)
- **Details**: The `run_inference` method in llama-stack uses ZeroMQ's `recv_pyobj` to receive serialized Python objects over a socket. This method automatically deserializes using `pickle.loads`. An attacker on the network can send a crafted payload that executes arbitrary code when unpickled via `__reduce__`.
- **Fix**: Meta replaced pickle serialization with type-safe Pydantic JSON across the API.
- **Impact**: Attackers could achieve RCE on Llama inference servers from the network — no authentication required.
- **Sources**: [Oligo Security](https://www.oligo.security/blog/cve-2024-50050-critical-vulnerability-in-meta-llama-llama-stack), [The Hacker News](https://thehackernews.com/2025/01/metas-llama-framework-flaw-exposes-ai.html), [CSO Online](https://www.csoonline.com/article/3810362/a-pickle-in-metas-llm-code-could-allow-rce-attacks.html)

---

## 4. BentoML (ML Serving Framework)

### CVE-2024-2912 — Insecure Deserialization in BentoML
- **Affected**: BentoML 1.2.0 through 1.2.4
- **Fixed**: 1.2.5
- **Details**: Any valid BentoML endpoint accepts POST requests containing serialized objects and deserializes them without validation. An attacker can send a crafted pickle payload that executes arbitrary OS commands upon deserialization.
- **Source**: [Toreon writeup](https://www.toreon.com/how-i-discovered-vulnerability-cve-2024-2912/), [GitHub Advisory](https://github.com/advisories/GHSA-hvj5-mvw9-93j3)

### CVE-2025-27520 — BentoML RCE via Insecure Deserialization (CRITICAL)
- **CVSS**: 9.8 (Critical)
- **Affected**: BentoML 1.3.8 through 1.4.2
- **Fixed**: 1.4.3
- **Details**: Same root cause as CVE-2024-2912 but in a different code path (`serde.py`). Unauthenticated HTTP requests can trigger arbitrary code execution. A public PoC exploit exists. Metasploit module available (`exploit/linux/http/bentoml_rce_cve_2025_27520`).
- **Sources**: [Checkmarx](https://checkmarx.com/zero-post/bentoml-rce-fewer-affected-versions-cve-2025-27520/), [Rapid7](https://www.rapid7.com/db/modules/exploit/linux/http/bentoml_rce_cve_2025_27520/)

---

## 5. MLflow (ML Experiment Tracking)

### CVE-2024-37054 — MLflow PyFunc Deserialization RCE
- **Affected**: MLflow 0.9.0 to < 2.14.2
- **Details**: `mlflow.pyfunc.load_model` uses `cloudpickle.load` to deserialize model artifacts. A crafted pickle payload embedded in a model artifact achieves arbitrary code execution when the model is loaded.
- **Source**: [GitHub PoC](https://github.com/NiteeshPujari/CVE-2024-37054-MLflow-RCE)

### CVE-2024-37056 — MLflow LightGBM Deserialization
- **Affected**: MLflow >= 1.23.0 to < 2.14.2
- **Details**: Deserialization vulnerability via `_load_model` in `mlflow/lightgbm/__init__.py`, allowing RCE through malicious pickle embedded in a LightGBM model.

### CVE-2024-37057 — MLflow TensorFlow Custom Objects Deserialization
- **Affected**: MLflow < 2.14.2
- **Details**: Vulnerable `_load_custom_objects` function in `mlflow/tensorflow/__init__.py` allows RCE via malicious pickle objects.

### CVE-2024-37052 through CVE-2024-37060 — MLflow Deserialization Family
- **Details**: A family of 9 related deserialization CVEs across different MLflow model flavors (PyFunc, LightGBM, TensorFlow, sklearn, etc.), all exploiting pickle-based deserialization.
- **Fixed**: MLflow 2.14.2
- **Sources**: [Snyk CVE-2024-37056](https://security.snyk.io/vuln/SNYK-PYTHON-MLFLOW-7210335), [HiddenLayer advisory](https://hiddenlayer.com/sai-security-advisory/2024-06-mlflow)

---

## 6. NumPy

### CVE-2019-6446 — NumPy `numpy.load` Arbitrary Code Execution (CRITICAL)
- **CVSS**: 9.8 (Critical)
- **Affected**: NumPy <= 1.16.0
- **Fixed**: NumPy 1.16.1
- **Details**: `numpy.load()` allows pickle deserialization by default when loading .npy files containing object arrays. A crafted serialized file achieves remote code execution.
- **Fix**: `allow_pickle=False` became the default.
- **Sources**: [Snyk](https://snyk.io/blog/numpy-arbitrary-code-execution-vulnerability/), [NVD](https://nvd.nist.gov/vuln/detail/cve-2019-6446)

---

## 7. scikit-learn / joblib

### CVE-2020-13092 — scikit-learn Arbitrary Code Execution
- **Affected**: scikit-learn <= 0.23.0
- **Details**: Untrusted files passed to `joblib.load()` can execute arbitrary commands. Disputed by maintainers — `joblib.load()` is documented as unsafe and user responsibility.
- **Note**: This is "working as designed" — joblib/pickle is inherently unsafe, and the CVE highlights the gap between documentation and user expectations.

### CVE-2024-34997 — joblib Deserialization via NumpyArrayWrapper
- **CVSS**: 7.8
- **Affected**: joblib v1.4.2
- **Details**: `read_array` in `joblib.numpy_pickle::NumpyArrayWrapper` uses `pickle.load()` insecurely. Disputed by maintainer — NumpyArrayWrapper is only used for caching trusted content.
- **Source**: [Snyk](https://security.snyk.io/vuln/SNYK-PYTHON-JOBLIB-6913425)

### CVE-2022-21797 — joblib Arbitrary Code Execution
- **Details**: Another joblib deserialization vulnerability allowing arbitrary code execution.

### skops as Mitigation
- scikit-learn recommends [skops.io](https://skops-dev.github.io/skops/) for safe model persistence as an alternative to pickle/joblib.

---

## 8. LangChain

### CVE-2024-5998 — LangChain FAISS Pickle Deserialization
- **Affected**: langchain-community < 0.2.4
- **Details**: `FAISS.deserialize_from_bytes()` directly calls `pickle.loads(serialized)` without safeguards. Attacker-controlled serialized data leads to arbitrary code execution via `os.system`.
- **Source**: [GitHub Advisory](https://github.com/advisories/GHSA-f2jm-rw3h-6phg), [NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-5998)

---

## 9. PickleScan Detection Bypasses (Meta-Vulnerabilities)

PickleScan is Hugging Face's primary defense against malicious pickle files. Multiple bypass vulnerabilities have been found:

### CVE-2025-1716 — PickleScan Unsafe Globals Bypass
- **Affected**: picklescan < 0.0.22
- **Details**: Attacker can craft pickle files using unsafe globals that PickleScan fails to flag, allowing arbitrary code execution during deserialization while passing safety scans.
- **Source**: [GitHub Advisory GHSA-655q-fx9r-782v](https://github.com/advisories/GHSA-655q-fx9r-782v)

### CVE-2025-1889 — Non-Standard File Extension Bypass
- **Affected**: picklescan < 0.0.22
- **Details**: PickleScan only scans files with standard pickle extensions (.pkl, .pickle, etc.) inside ZIP archives. Malicious pickle files with non-standard extensions (e.g., .data) are invisible to the scanner but still loaded by PyTorch.
- **Source**: [GitHub Advisory GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr)

### CVE-2025-1944 — ZIP Filename Tampering
- **Details**: Modifying the filename in the ZIP local file header while keeping the original in the central directory causes PickleScan to crash (BadZipFile), but PyTorch's more forgiving ZIP implementation still loads the file.

### CVE-2025-1945 — ZIP Flag Bit Modification
- **Details**: Flipping specific bits in ZIP file headers causes PickleScan to miss malicious pickle files while PyTorch still loads them successfully.

### JFrog Zero-Day PickleScan Bypasses (3 additional)
- JFrog Security Research discovered 3 additional zero-day critical vulnerabilities enabling attackers to completely evade PickleScan's malware detection.
- **Source**: [JFrog blog](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)

### Sonatype PickleScan Bypasses (4 additional)
- Sonatype discovered 4 critical vulnerabilities in PickleScan.
- **Source**: [Sonatype blog](https://www.sonatype.com/blog/bypassing-picklescan-sonatype-discovers-four-vulnerabilities)

---

## 10. Real-World Incidents and Supply Chain Attacks

### Malicious Models on Hugging Face
- **JFrog discovery (2024)**: Over 100 malicious ML models found on Hugging Face. One model by user "baller423" contained a reverse shell payload — when loaded, it established a connection to an attacker-controlled server.
- **Rapid7 discovery**: Malicious .pth files on Hugging Face carried embedded payloads that, upon deserialization, executed system commands to download and run remote access trojans (RATs) — shell scripts and ELF binaries.
- **ReversingLabs "nullifAI" (2025)**: Discovered novel technique for distributing malware by abusing pickle serialization on Hugging Face, evading existing protections.
- **Broken pickle evasion**: Malicious payloads inserted at the beginning of pickle streams execute before the parser encounters errors, allowing code execution despite technically broken/invalid pickle files.

### Scale of the Problem
- **Protect AI Guardian** (as of April 2025): Scanned 4.47 million unique model versions across 1.41 million repositories, identifying **352,000 unsafe or suspicious issues** across **51,700 models**.
- **Almost all malicious models on Hugging Face use the pickle format.**

### Sources
- [JFrog: Malicious HuggingFace models](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [Rapid7: .pth to p0wned](https://www.rapid7.com/blog/post/from-pth-to-p0wned-abuse-of-pickle-files-in-ai-model-supply-chains/)
- [ReversingLabs: nullifAI](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [The Hacker News](https://thehackernews.com/2025/02/malicious-ml-models-found-on-hugging.html)

---

## CVE Summary Table

| CVE | Framework | CVSS | Year | Core Issue |
|-----|-----------|------|------|------------|
| CVE-2025-32434 | PyTorch | 9.3 | 2025 | `weights_only=True` bypass — RCE |
| CVE-2024-50050 | Meta Llama | 9.3/9.8 | 2024 | ZeroMQ pickle RCE on inference server |
| CVE-2024-3660 | Keras | 9.8 | 2024 | Lambda layer code injection |
| CVE-2025-49655 | Keras | — | 2025 | TorchModuleWrapper unsafe deserialization |
| CVE-2021-37678 | TensorFlow | 7.8 | 2021 | YAML unsafe_load code execution |
| CVE-2024-2912 | BentoML | — | 2024 | HTTP endpoint pickle RCE |
| CVE-2025-27520 | BentoML | 9.8 | 2025 | HTTP endpoint pickle RCE (repeat) |
| CVE-2024-37054 | MLflow | — | 2024 | PyFunc cloudpickle RCE |
| CVE-2024-37056 | MLflow | — | 2024 | LightGBM model pickle RCE |
| CVE-2024-37057 | MLflow | — | 2024 | TensorFlow custom objects RCE |
| CVE-2019-6446 | NumPy | 9.8 | 2019 | `numpy.load` pickle RCE |
| CVE-2020-13092 | scikit-learn | — | 2020 | `joblib.load` code execution |
| CVE-2024-34997 | joblib | 7.8 | 2024 | NumpyArrayWrapper pickle.load |
| CVE-2024-5998 | LangChain | — | 2024 | FAISS pickle deserialization |
| CVE-2025-1716 | PickleScan | — | 2025 | Unsafe globals bypass |
| CVE-2025-1889 | PickleScan | — | 2025 | Non-standard extension bypass |
| CVE-2025-1944 | PickleScan | — | 2025 | ZIP filename tampering |
| CVE-2025-1945 | PickleScan | — | 2025 | ZIP flag bit modification |

---

## Key Patterns and Themes

### 1. Mitigations Keep Failing
- PyTorch's `weights_only=True` was the gold standard mitigation — then CVE-2025-32434 showed it could be bypassed entirely.
- Keras `safe_mode=True` doesn't apply to legacy H5 format, and can be bypassed via downgrade attacks.
- PickleScan, the ML community's primary scanner, has had **7+ bypass vulnerabilities** discovered in 2025 alone.

### 2. The Problem is Architectural
- Pickle's `__reduce__` method is fundamentally a code execution primitive. No amount of allowlisting or scanning can make it safe against a determined attacker.
- Every framework that uses pickle for serialization eventually gets a deserialization CVE.

### 3. Supply Chain is the Attack Surface
- Hugging Face hosts millions of models, many using pickle format.
- 352,000+ unsafe/suspicious issues identified across 51,700 models.
- Attackers upload trojaned models that establish reverse shells, download RATs, or exfiltrate data.

### 4. Framework Response Timeline
- **NumPy (2019)**: Changed `allow_pickle` default to False.
- **TensorFlow (2021)**: Removed YAML format support entirely.
- **Keras (2024)**: Added `safe_mode` (but incomplete).
- **PyTorch (2024-2025)**: Changed `weights_only` default to True, then had to fix bypass.
- **Meta Llama (2024)**: Replaced pickle with Pydantic JSON.
- **Industry trend**: Migration toward Safetensors, ONNX, and JSON-based formats.

---

## Recommended Safe Alternatives

| Unsafe Format | Safe Alternative |
|--------------|------------------|
| PyTorch .pt/.pth (pickle) | Safetensors format |
| Keras .h5 (with Lambda layers) | Keras v3 format + safe_mode |
| scikit-learn joblib.dump | skops.io |
| Generic pickle | JSON, Protocol Buffers, MessagePack |
| ONNX (generally safe) | ONNX (no pickle, computation graph only) |
