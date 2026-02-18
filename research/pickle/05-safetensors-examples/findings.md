# SafeTensors: GitHub Examples & Pickle→SafeTensors Conversion

## 1. Official Repository & Documentation

**Repository:** https://github.com/huggingface/safetensors
**Documentation:** https://huggingface.co/docs/safetensors/en/index
**API Reference:** https://huggingface.github.io/safetensors/
**PyPI:** https://pypi.org/project/safetensors/
**License:** Apache-2.0

SafeTensors is Hugging Face's format for storing tensors safely (no arbitrary code execution) with zero-copy loading. The core is written in Rust with bindings for Python, Node.js, and Rust.

### Installation

```bash
pip install safetensors
# or
conda install -c huggingface safetensors
```

---

## 2. File Format (Why It's Safe)

A `.safetensors` file has exactly three parts:

| Section | Size | Content |
|---------|------|---------|
| Header size | 8 bytes | Unsigned little-endian 64-bit integer |
| JSON header | Variable (max 100MB) | Dict mapping tensor names → `{dtype, shape, data_offsets}` |
| Data buffer | Remainder | Raw tensor bytes, row-major (C order), little-endian |

**Security guarantees:**
- No executable code (unlike pickle which can execute arbitrary Python)
- Header limited to 100MB (prevents DoS via giant JSON)
- Data offsets guaranteed non-overlapping (prevents buffer confusion attacks)
- Format is deterministic — same tensors always produce same bytes

**Performance:**
- Zero-copy via memory mapping (`mmap`)
- Lazy loading — read individual tensors without loading entire file
- Tensor slicing — load partial tensors (e.g., for multi-GPU sharding)
- Benchmark: 8-GPU distributed loading went from **10 minutes** (PyTorch pickle) to **45 seconds** (safetensors)

---

## 3. Basic API Usage

### Save tensors

```python
import torch
from safetensors.torch import save_file

tensors = {
    "embedding": torch.zeros((2, 2)),
    "attention": torch.zeros((2, 3))
}
save_file(tensors, "model.safetensors")
```

### Load tensors

```python
from safetensors import safe_open

tensors = {}
with safe_open("model.safetensors", framework="pt", device="cpu") as f:
    for k in f.keys():
        tensors[k] = f.get_tensor(k)
```

### Lazy loading / tensor slicing (for multi-GPU)

```python
from safetensors import safe_open

with safe_open("model.safetensors", framework="pt", device=0) as f:
    tensor_slice = f.get_slice("embedding")
    vocab_size, hidden_dim = tensor_slice.get_shape()
    partial = tensor_slice[:, :hidden_dim]  # Load only what you need
```

### Model-level API (handles shared tensors automatically)

```python
from safetensors.torch import save_model, load_model

# Save — auto-detects shared tensors, handles deduplication
save_model(model, "model.safetensors")

# Load — restores shared tensor relationships
load_model(model, "model.safetensors")
```

### In-memory serialization

```python
from safetensors.torch import save, load

# To bytes (no file I/O)
data = save({"weight": torch.zeros(10)})

# From bytes
tensors = load(data)
```

---

## 4. Pickle → SafeTensors Conversion

### Method 1: Minimal Script (Local Files)

The simplest possible conversion for a local `.pt`/`.pth`/`.ckpt`/`.bin` file:

```python
import torch
from safetensors.torch import save_file

# Load the pickle checkpoint
checkpoint = torch.load("model.pt", map_location="cpu", weights_only=True)

# Extract state_dict if wrapped
if "state_dict" in checkpoint:
    state_dict = checkpoint["state_dict"]
elif "model" in checkpoint:
    state_dict = checkpoint["model"]
else:
    state_dict = checkpoint

# Force contiguous memory layout
state_dict = {k: v.contiguous() for k, v in state_dict.items()}

# Save as safetensors
save_file(state_dict, "model.safetensors")
```

**Note:** `weights_only=True` is important — it restricts what pickle can unpickle, reducing (but not eliminating) the attack surface. For truly untrusted files, use containerized conversion (Method 4).

### Method 2: Using save_model/load_model (For nn.Module)

If you have the model class available:

```python
import torch
from safetensors.torch import save_model

# Load model the normal way
model = YourModelClass()
model.load_state_dict(torch.load("model.pt", map_location="cpu"))

# Save as safetensors (handles shared tensors automatically)
save_model(model, "model.safetensors")
```

### Method 3: Official HuggingFace convert.py (For Hub Models)

The official script at [`bindings/python/convert.py`](https://github.com/huggingface/safetensors/blob/main/bindings/python/convert.py) handles:
- Single-file models (`pytorch_model.bin`)
- Sharded models (`pytorch_model.bin.index.json` → multiple files)
- Generic `.bin`/`.ckpt` files
- Shared tensor deduplication
- Post-conversion file size validation
- Post-conversion tensor equality verification
- Automatic PR creation on HuggingFace Hub

```bash
# Install dependencies
pip install safetensors torch huggingface_hub transformers

# Convert a Hub model (creates a PR with the safetensors version)
python convert.py gpt2
python convert.py facebook/wav2vec2-base-960h
python convert.py your-org/your-model --revision main --force
```

Key conversion logic from the official script:

```python
def convert_file(pt_filename, sf_filename, discard_names):
    loaded = torch.load(pt_filename, map_location="cpu")
    if "state_dict" in loaded:
        loaded = loaded["state_dict"]

    # Handle shared tensors — find duplicates, keep one, record mapping
    to_removes = _remove_duplicate_names(loaded, discard_names=discard_names)

    metadata = {"format": "pt"}
    for kept_name, to_remove_group in to_removes.items():
        for to_remove in to_remove_group:
            if to_remove not in metadata:
                metadata[to_remove] = kept_name  # Record alias in metadata
            del loaded[to_remove]

    loaded = {k: v.contiguous() for k, v in loaded.items()}
    save_file(loaded, sf_filename, metadata=metadata)

    # Validate: file sizes within 1%, tensors exactly equal
    check_file_size(sf_filename, pt_filename)
    reloaded = load_file(sf_filename)
    for k in loaded:
        if not torch.equal(loaded[k], reloaded[k]):
            raise RuntimeError(f"Tensors do not match for key {k}")
```

### Method 4: Containerized Conversion (For Untrusted Files)

[FNGarvin/pickle-to-safetensors](https://github.com/FNGarvin/pickle-to-safetensors) — runs conversion in a network-isolated container so malicious pickle payloads can't phone home or damage the host.

```bash
# Build the container
podman build -t pickle-to-safetensors .

# Convert (output appears in same directory)
./pickle-to-safetensors.sh ~/models/suspicious_model.pth
```

**Security layers:**
- `--network none` (no network access)
- Only the target file's directory is mounted
- CPU-only PyTorch (no GPU access)
- Non-tensor data (optimizer states, hyperparams) discarded

### Method 5: HuggingFace Convert Space (Web UI, No Code)

https://huggingface.co/spaces/safetensors/convert

Upload or point to a Hub model → it converts and opens a PR. Good for one-off conversions. Runs the same `convert.py` under the hood.

---

## 5. Transformers Integration

HuggingFace Transformers has native safetensors support since v4.x:

### Loading (automatic — prefers safetensors when available)

```python
from transformers import AutoModelForCausalLM

# If the repo has .safetensors files, they're loaded by default
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
```

### Saving

```python
# Save model weights as safetensors (this is now the default)
model.save_pretrained("./my_model", safe_serialization=True)

# To force pickle format (not recommended)
model.save_pretrained("./my_model", safe_serialization=False)
```

### Diffusers, PEFT, and other HF libraries

Same pattern — `safe_serialization=True` is the default or opt-in:

```python
# Diffusers
pipe.save_pretrained("./my_pipe", safe_serialization=True)

# PEFT/LoRA adapters
model.save_pretrained("./adapter", safe_serialization=True)
```

---

## 6. Supported Data Types

| PyTorch Type | SafeTensors Type |
|---|---|
| `torch.float64` | F64 |
| `torch.float32` | F32 |
| `torch.float16` | F16 |
| `torch.bfloat16` | BF16 |
| `torch.int64` | I64 |
| `torch.int32` | I32 |
| `torch.int16` | I16 |
| `torch.int8` | I8 |
| `torch.uint8` | U8 |
| `torch.bool` | BOOL |
| `torch.float8_e4m3fn` | F8_E4M3 |
| `torch.float8_e5m2` | F8_E5M2 |

Also supports: NumPy arrays, TensorFlow tensors, JAX arrays, PaddlePaddle tensors, MLX arrays.

---

## 7. Shared Tensors — The Main Gotcha

### The Problem

PyTorch allows tensors to share underlying storage. Classic example: in transformers, `embeddings.weight` and `lm_head.weight` often point to the same data (weight tying). Pickle preserves this sharing. SafeTensors does **not** natively store sharing relationships.

### Why SafeTensors Doesn't Store Sharing

1. Not all frameworks support it (TensorFlow doesn't)
2. It would break lazy loading (can't re-share after giving out individual tensors)
3. Shared-but-sliced tensors in pickle can waste space (saving full buffer when only a slice is shared)

### The Solution

Use `save_model()` / `load_model()` instead of `save_file()` / `load_file()`:

```python
from safetensors.torch import save_model, load_model

# save_model detects shared tensors, saves only one copy,
# records the alias mapping in file metadata
save_model(model, "model.safetensors")

# load_model reads the metadata, restores sharing relationships
load_model(model, "model.safetensors")
```

**Caveat:** If you inspect the file's keys directly, "missing" tensors are expected — they're aliases recorded in metadata, not separate entries.

---

## 8. Migration Gotchas & Limitations

### Things That Get Lost in Conversion

| What | Preserved? | Notes |
|------|-----------|-------|
| Tensor weights | Yes | Exact bit-for-bit reproduction |
| Tensor names/keys | Yes | Stored in JSON header |
| dtypes and shapes | Yes | Stored in JSON header |
| Custom metadata | Yes | Can store arbitrary string key-value pairs |
| Optimizer state | **No** | Must be saved separately or discarded |
| Learning rate schedulers | **No** | Not tensors |
| Training hyperparameters | **No** | Not tensors (use metadata or separate JSON) |
| Random number generator states | **No** | Not tensors |
| Custom Python objects | **No** | This is the point — no arbitrary code |
| Shared tensor relationships | **Partial** | Preserved via metadata when using `save_model()` |

### Known Issues

1. **Metadata `format` field**: Some tools expect `metadata={"format": "pt"}` in the safetensors file. If missing, `transformers` may fail to auto-detect the framework. Always include it.

2. **Non-contiguous tensors**: Must call `.contiguous()` before saving. The official scripts do this automatically; DIY scripts often forget.

3. **Sparse tensors**: Must convert to dense before saving. SafeTensors doesn't support sparse formats.

4. **Meta tensors** (`device="meta"`): Cannot be saved — they have no actual data.

5. **Embeddings, Hypernetworks, LoRAs**: Different model types may store weights in non-standard checkpoint structures. Simple `checkpoint["state_dict"]` extraction may not work — you may need to inspect the pickle structure first.

6. **Sharded/distributed checkpoints**: Raw FSDP shards or DeepSpeed ZeRO checkpoints need consolidation before conversion. Can't directly convert individual shards.

7. **File size validation**: The official script checks that safetensors file size is within 1% of the pickle file. Significant size differences indicate a problem (missing tensors or extra data).

### Things That Go Smoothly

- Standard `model.state_dict()` → safetensors is trivial
- HuggingFace Transformers models convert with zero effort
- Stable Diffusion models (used extensively on CivitAI) convert well
- The ecosystem has broadly adopted safetensors — most model hubs prefer it

---

## 9. Ecosystem Adoption

SafeTensors is now the **de facto standard** for model distribution. Major adopters:

- [HuggingFace Transformers](https://github.com/huggingface/transformers) — default save format
- [HuggingFace Diffusers](https://github.com/huggingface/diffusers)
- [Apple MLX](https://github.com/ml-explore/mlx)
- [llama.cpp](https://github.com/ggerganov/llama.cpp) — uses safetensors as input for GGUF conversion
- [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [InvokeAI](https://github.com/invoke-ai/InvokeAI)
- [CivitAI](https://civitai.com/) — community model hub
- [ColossalAI](https://github.com/hpcaitech/ColossalAI)
- [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui)
- [HuggingFace Candle](https://github.com/huggingface/candle) — Rust ML framework

---

## 10. Ease of Migration Assessment

### Difficulty: **Low** for standard models

| Scenario | Effort | Approach |
|----------|--------|----------|
| HuggingFace model on Hub | Trivial | Use Convert Space or `convert.py` |
| Local transformers model | Easy | `save_pretrained(safe_serialization=True)` |
| Local PyTorch checkpoint | Easy | 5-line script (Method 1 above) |
| Model with shared tensors | Easy | Use `save_model()` instead of `save_file()` |
| Custom model architecture | Medium | May need to extract state_dict manually |
| Sharded/FSDP checkpoints | Hard | Consolidate first, then convert |
| Untrusted pickle files | Medium | Use containerized conversion (Method 4) |
| Non-PyTorch frameworks | Easy | safetensors has native TF/JAX/Flax/NumPy support |

### Bottom Line

For the pickle security research context: SafeTensors is the clearest success story in the "replace pickle" effort. It's:
- **Simple** — the format is a JSON header + flat tensor data
- **Safe** — no code execution possible, by construction
- **Fast** — zero-copy mmap, often faster than pickle
- **Adopted** — the entire HuggingFace ecosystem and most major ML tools use it
- **Easy to migrate** — for the common case of "save model weights," it's a drop-in replacement

The main limitation is intentional: it only stores tensors. If your pickle file contains optimizer states, training configs, or custom objects, those need separate handling. But for model weight distribution — which is the primary attack surface for pickle exploits — safetensors is the answer.
