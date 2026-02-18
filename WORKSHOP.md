# RSA Workshop: ML Pipeline Security - Pickle Deserialization

## Overview

This workshop demonstrates pickle deserialization vulnerabilities in ML model loading and how to mitigate them with SafeTensors.

## Three Case Studies

### 1. Model Deserialization (25 minutes) ⭐ This demo

**Silver Path (Vulnerable):**
- Load PyTorch model using `torch.load()`
- Demonstrate arbitrary code execution via pickle
- Show real-world attack scenarios

**Gold Path (Safe):**
- Convert to SafeTensors
- Load safely with no code execution risk
- Compare performance (SafeTensors is faster!)

### 2. Model Poisoning (30 minutes) - TBD

### 3. Supply Chain Security (20 minutes) - TBD

---

## Case Study 1: Pickle Deserialization

### Setup (5 minutes)

```bash
cd demo-malicious
docker build -t pickle-demo .
docker run --rm -it pickle-demo
```

### Part 1: The Vulnerability (10 minutes)

**Step 1:** Create malicious model
```bash
python create_malicious_model.py
```

**Step 2:** Demonstrate the attack
```bash
python create_malicious_model.py attack
```

**Observe:**
- Before load: `/tmp/pwned_by_pickle.txt` doesn't exist
- After `torch.load()`: File is created
- Code executed automatically during deserialization

**Step 3:** Inspect the pickle
```bash
fickling malicious_model.pt
```

Shows the decompiled bytecode and malicious `__reduce__` method.

### Part 2: Understanding the Exploit (5 minutes)

**The vulnerable pattern:**
```python
# This is dangerous!
model = torch.load("untrusted_model.pt")
```

**How it works:**
```python
class MaliciousPayload:
    def __reduce__(self):
        # Called automatically during unpickling
        return (os.system, ("malicious command here",))
```

**Real-world scenarios:**
- Download model from Hugging Face (352,000+ unsafe models found)
- Load checkpoint from colleague
- Use model from research paper repo
- Fine-tune community model

### Part 3: The Safe Alternative (5 minutes)

**Step 1:** Create safe model
```bash
python safe_demo.py
```

**Step 2:** Load safely
```bash
python safe_demo.py load
```

**SafeTensors advantages:**
- ✅ No code execution (by design)
- ✅ Faster loading (zero-copy mmap)
- ✅ Simple format (JSON + raw tensors)
- ✅ Industry standard (HuggingFace default)

**Format comparison:**

| Feature | Pickle (.pt) | SafeTensors |
|---------|-------------|-------------|
| Can execute code | ✅ Yes | ❌ No |
| Loading speed | Slower | Faster (mmap) |
| File size | Larger | Smaller |
| Security | Dangerous | Safe |

### Part 4: Discussion (5 minutes)

**Key Takeaways:**
1. Pickle is fundamentally unsafe for untrusted data
2. `weights_only=True` helps but has bypasses
3. SafeTensors is the solution for model distribution
4. This affects the entire ML supply chain

**Mitigation strategies:**
- Use SafeTensors for all model distribution
- If you must use pickle, containerize loading (network-isolated)
- Scan with fickling/modelscan before loading
- Never `torch.load()` models from untrusted sources

---

## Instructor Notes

### Pre-workshop Setup
- Test Docker build
- Verify fickling installation
- Prepare demo environment
- Have backup slides ready

### Common Questions

**Q: Why not just fix pickle?**
A: Pickle's design *requires* code execution. The `__reduce__` mechanism is fundamental. It's not a bug, it's by design.

**Q: What about `weights_only=True`?**
A: PyTorch 2.4+ added this as mitigation, but:
- CVE-2025-32434: `weights_only=True` itself was bypassable
- Only restricts to tensors, not perfect
- SafeTensors is the real solution

**Q: Does this affect TensorFlow?**
A: TensorFlow uses pickle for some formats. Safer default is Protocol Buffers. But similar issues exist in other frameworks (Keras had CVE-2024-3660).

**Q: How widespread is this?**
A: 352,000+ models on Hugging Face flagged as unsafe. Over 100 actively malicious models deploying RATs found in the wild.

### Timing Adjustments

- **Running ahead?** Do live fickling decompilation, show pickle bytecode
- **Running behind?** Skip the "create safe model" step, just explain SafeTensors
- **Extra time?** Show Sleepy Pickle (model poisoning) or scanner bypasses

### Troubleshooting

**Docker won't build:**
- Check Chainguard registry access
- Try `docker pull cgr.dev/chainguard/pytorch:latest` first

**Code doesn't execute:**
- Check PyTorch version (should be 2.x)
- Verify file permissions in container
- Try a different payload (e.g., `touch /tmp/test.txt`)

**Fickling errors:**
- Reinstall: `pip install --upgrade fickling`
- Check Python version (needs 3.8+)
