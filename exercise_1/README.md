# Exercise 1: Pickle Deserialization in PyTorch

In this exercise, we'll demonstrate how PyTorch's default model format allows arbitrary code execution, then switch to a safe alternative. We'll be moving through the following steps:

1. Build a container with PyTorch and related tools.
2. Create and load a malicious model to demonstrate the vulnerability.
3. Create and load a model using SafeTensors, a safe serialization format.

## The Vulnerability

PyTorch saves models using Python's pickle format. Pickle is a serialization protocol that can represent arbitrary Python objects — including executable code. When you call `torch.load()` on a model file, pickle deserializes the contents, and any embedded code runs automatically.

The mechanism is a method called `__reduce__`, which tells pickle how to reconstruct an object. An attacker can define `__reduce__` to call any function:

```python
class MaliciousPayload:
    def __reduce__(self):
        return (os.system, ("echo pwned",))
```

When `torch.load()` encounters this, it calls `os.system("echo pwned")` — or whatever the attacker wants. The payload could steal credentials, install a backdoor, or exfiltrate data. JFrog researchers have found [over 100 actively malicious models on Hugging Face](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/) deploying backdoors using this pattern.

## Silver Path: Arbitrary Code Execution

Run the following command to build the exercise container and demonstrate the attack:

```sh
mkdir -p ~/rsa-workshop/exercise_1 && cd ~/rsa-workshop/exercise_1 && \
 curl -sL https://codeload.github.com/chainguard-demo/ml-pipeline-security/tar.gz/main | \
 tar -xz --strip-components=2 ml-pipeline-security-main/exercise_1/ && \
 docker build . -t pickle-demo && \
 docker run --rm pickle-demo create_malicious_model.py attack
```

The command downloads the exercise files, builds a container image with PyTorch and fickling (a pickle analysis tool), then runs the attack script. The script creates a model file with an embedded payload and loads it with `torch.load()`, demonstrating that arbitrary code executes during deserialization. You should see output like:

```
ALERT: Malicious code executed!
Creating malicious model file...
🥒 Malicious model created: /app/malicious_model.pt

Before load: /tmp/pwned_by_pickle.txt exists? False

Loading with weights_only=False (VULNERABLE):

After load: /tmp/pwned_by_pickle.txt exists? True

🥒🔴 EXPLOIT SUCCESSFUL! Arbitrary code was executed.
```

The file `/tmp/pwned_by_pickle.txt` didn't exist before loading the model. After `torch.load()`, it does. No explicit call to create it — the code was embedded in the model file itself.

Note the `weights_only=False` flag. PyTorch 2.6+ blocks unrestricted pickle loading by default, but many users and tutorials set `weights_only=False` for compatibility.

## Gold Path: SafeTensors

Run the following command to demonstrate the safe alternative:

```sh
mkdir -p ~/rsa-workshop/exercise_1 && cd ~/rsa-workshop/exercise_1 && \
 curl -sL https://codeload.github.com/chainguard-demo/ml-pipeline-security/tar.gz/main | \
 tar -xz --strip-components=2 ml-pipeline-security-main/exercise_1/ && \
 docker build . -t pickle-demo && \
 docker run --rm pickle-demo safe_demo.py
```

You should see output like:

```
Creating model and saving with SafeTensors...
✓ Model safely saved to: /app/safe_model.safetensors

Loading model from SafeTensors...
✓ Model loaded safely!
✓ Model works: output shape torch.Size([1, 3])

✅ SafeTensors guarantees:
  - No code execution during load
  - Zero-copy memory mapping (faster)
  - Deterministic serialization
  - Simple format: JSON header + tensor bytes
```

SafeTensors stores only the model's weights as raw numerical data with a JSON header. There is no mechanism for embedding executable code — the format doesn't support it. It's also faster than pickle due to memory-mapped loading.

## Comparison

| | Pickle (.pt) | SafeTensors |
|---|---|---|
| Can execute code | Yes | No |
| Loading speed | Slower | Faster (mmap) |
| Format | Opaque binary | JSON header + raw tensors |
| Industry adoption | Legacy default | Hugging Face default |

## Resources

- [SafeTensors documentation](https://huggingface.co/docs/safetensors/)
- [fickling: a Python pickle decompiler](https://github.com/trailofbits/fickling)
- [CVE-2025-32434: weights_only=True bypass in PyTorch](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6)
