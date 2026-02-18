# Backdoor Trigger Injection Tools for Computer Vision

Research findings on tools/frameworks that inject backdoor triggers into image datasets for training data poisoning. Focused on practical tooling for educational demonstrations.

**Date**: 2026-02-17

---

## Executive Summary

There are **4 major framework-level tools** and **7+ standalone attack implementations** for injecting backdoor triggers into CV datasets. The landscape ranges from comprehensive benchmarks (BackdoorBench, BackdoorBox) to single-attack reference implementations. For educational demos, **BackdoorBench** and **BackdoorBox** are the strongest candidates — both are well-maintained, PyTorch-based, and cover the full spectrum of trigger types.

---

## Major Frameworks (Multi-Attack Toolkits)

### 1. BackdoorBench (SCLBD) ⭐ TOP PICK

- **Repo**: https://github.com/SCLBD/BackdoorBench
- **Website**: https://backdoorbench.github.io/
- **Paper**: NeurIPS 2022 (D&B), IJCV 2025
- **Framework**: PyTorch
- **Status**: Actively maintained

#### What It Does
The most comprehensive benchmark for backdoor learning. Integrated implementations of **16 attack algorithms** and **28 defense/detection algorithms** under a unified evaluation framework.

#### All 16 Attacks
| Attack | Trigger Type | Key Property |
|--------|-------------|-------------|
| BadNets | Patch (fixed pattern) | Foundational; simplest attack |
| Blended | Image blending (transparency) | Stealthier than patch |
| Blind | Model-controlled | Attacker controls training |
| BppAttack | Image quantization | Stealthy via compression |
| CTRL | SSL-targeted | Attacks self-supervised learning |
| FTrojan | Frequency domain (DCT) | Invisible; operates in frequency space |
| Input-Aware | Dynamic/sample-specific | Different trigger per input |
| Label-Consistent (LC) | Adversarial perturbation | Clean-label; no label flipping |
| Low Frequency (LF) | Frequency-based | Exploits low-freq components |
| LIRA | Learnable trigger | Optimized invisible trigger |
| PoisonInk | Invisible ink pattern | Robust and invisible |
| ReFool | Reflection | Uses natural reflections as trigger |
| SIG | Sinusoidal signal | Signal-based trigger pattern |
| SSBA | Sample-specific (steganography) | Unique trigger per image |
| TrojanNN | Neuron-targeted | Directly modifies neuron activations |
| WaNet | Warping field | Geometric distortion trigger |

#### Datasets & Models
- **Datasets**: CIFAR-10, CIFAR-100, GTSRB, Tiny ImageNet
- **Models**: PreAct-ResNet18, VGG19-BN, ConvNeXt-Tiny, ViT-B-16, DenseNet-161, MobileNetV3-Large, EfficientNet-B3

#### Ease of Use for Demos
- CLI-driven with config files — change attack/defense/model/dataset via args
- Website with leaderboard and model zoo
- Comprehensive documentation
- **Rating: HIGH** — best all-in-one option for educational demos

---

### 2. BackdoorBox (THU)

- **Repo**: https://github.com/THUYimingLi/BackdoorBox
- **Framework**: PyTorch
- **Maintainer**: Yiming Li (Tsinghua University)

#### What It Does
Open-sourced Python toolbox for backdoor attacks and defenses. Emphasizes clean, modular code with each attack in a standalone file.

#### Attacks (16)
**Poison-Only**: BadNets, Blended, Refool, Label-Consistent, TUAP, SleeperAgent, ISSBA, WaNet, BATT, AdaptivePatch, BAAT

**Training-Controlled**: Blind, IAD (Input-Aware Dynamic), PhysicalBA, LIRA

#### Defenses (11)
AutoEncoderDefense, ShrinkPad, REFINE, FineTuning, Pruning, MCR, NAD, ABL, SCALE-UP, IBD-PSC, FLARE

#### Key Differentiator
Each attack is a single file (e.g., `core/attacks/BadNets.py`, `core/attacks/WaNet.py`) — making it excellent for understanding individual attack mechanics. Users can easily extract poisoned datasets and attacked models as intermediate outputs.

#### Ease of Use for Demos
- Each attack has a standalone example script
- Poisoned datasets can be saved and inspected
- Flexible: use your own model/dataset
- **Rating: HIGH** — best for "understand one attack deeply" educational approach

---

### 3. Adversarial Robustness Toolbox (ART) — IBM/LF AI

- **Repo**: https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **Docs**: https://adversarial-robustness-toolbox.readthedocs.io/
- **Framework**: Multi-framework (TF, Keras, PyTorch, sklearn, XGBoost, etc.)
- **License**: MIT
- **Status**: Actively maintained (v1.17.0)

#### What It Does
Comprehensive ML security library covering evasion, poisoning, extraction, and inference attacks. The poisoning module includes backdoor attacks.

#### Poisoning/Backdoor Attack Classes
| Class | Description |
|-------|-------------|
| `PoisoningAttackBackdoor` | Core backdoor: applies perturbation functions + label flipping |
| `PoisoningAttackCleanLabelBackdoor` | Clean-label: backdoor without modifying labels |
| `HiddenTriggerBackdoor` | Imperceptible triggers via feature-space manipulation |
| `FeatureCollisionAttack` | Poison Frogs-style feature collision |
| `BullseyePolytopeAttackPyTorch` | Scalable clean-label polytope attack |
| `GradientMatchingAttack` | Witches' Brew gradient matching |
| `SleeperAgentAttack` | Patch-based sleeper agent |
| `PoisoningAttackAdversarialEmbedding` | Adversarial embedding attack |
| `BackdoorAttackDGMReDTensorFlowV2` | Backdoor on generative models (TF2) |
| `BackdoorAttackDGMTrailTensorFlowV2` | GAN-targeted backdoor (TF2) |

#### Key Differentiator
- **Multi-framework support** — works with TF, PyTorch, sklearn, etc.
- Includes **Jupyter notebooks** for each attack (great for demos)
- Has both attack AND defense implementations
- pip-installable (`pip install adversarial-robustness-toolbox`)

#### Ease of Use for Demos
- `pip install` — no cloning repos
- Pre-built notebooks (e.g., `poisoning_attack_clean_label_backdoor.ipynb`)
- Works with any framework
- **Rating: HIGH** — easiest to get started; Jupyter notebooks are demo-ready

---

### 4. TrojanZoo

- **Repo**: https://github.com/ain-soph/trojanzoo
- **Framework**: PyTorch
- **License**: GPL-3.0
- **Docs**: https://ain-soph.github.io/trojanzoo

#### What It Does
Universal PyTorch platform for security research on image classification. Two packages: `trojanzoo` (abstractions) and `trojanvision` (CV implementations).

#### Attacks
BadNet, TrojanNN, and others from published papers (KDD 2020, CCS 2020).

#### Ease of Use for Demos
- CLI-based experiments
- Extensible OOP hierarchy
- Full documentation site
- **Rating: MEDIUM** — powerful but steeper learning curve than BackdoorBench/ART

---

## Standalone Attack Implementations

### 5. WaNet (Official)
- **Repo**: https://github.com/VinAIResearch/Warping-based_Backdoor_Attack-release
- **Paper**: ICLR 2021
- **Trigger**: Warping field (geometric distortion)
- **Key**: Invisible to human inspection; uses smooth warping fields
- **Rating: MEDIUM** — single attack, but well-documented

### 6. FTrojan (Frequency Domain)
- **Repo**: https://github.com/SoftWiser-group/FTrojan
- **Paper**: ECCV 2022
- **Trigger**: Frequency domain perturbation via DCT on YUV channels
- **Key**: Invisible — triggers in high-frequency UV channel components; defeats most spatial-domain defenses
- **Rating: MEDIUM** — interesting for showing non-obvious trigger mechanisms

### 7. Input-Aware Dynamic Attack (Official)
- **Repo**: https://github.com/VinAIResearch/input-aware-backdoor-attack-release
- **Paper**: NeurIPS 2020
- **Trigger**: Dynamic, sample-specific (generated by encoder-decoder network)
- **Key**: Trigger is conditioned on input image — each image gets a unique trigger
- **Rating: MEDIUM** — demonstrates advanced dynamic triggers

### 8. Narcissus (Clean-Label)
- **Repo**: https://github.com/reds-lab/Narcissus
- **Paper**: ACM CCS 2023
- **Trigger**: Optimized adversarial perturbation (clean-label)
- **Key**: Only **3 poisoned images** needed to backdoor face recognition with 99.89% success. Requires access only to target class data.
- **Rating: HIGH** — dramatic demo potential (3 images!)

### 9. COMBAT (Clean-Label)
- **Repo**: https://github.com/VinAIResearch/COMBAT
- **Paper**: AAAI 2024
- **Trigger**: Alternated training clean-label approach
- **Key**: Latest clean-label technique with improved effectiveness

### 10. CorruptEncoder (Contrastive Learning)
- **Repo**: https://github.com/jzhang538/CorruptEncoder
- **Paper**: CVPR 2024
- **Trigger**: Data poisoning on contrastive learning pipelines
- **Key**: Attacks pre-training stage of self-supervised models

---

## Poisoned Data Generation Tools

### 11. Witches' Brew / Gradient Matching (Geiping)
- **Repo**: https://github.com/JonasGeiping/poisoning-gradient-matching
- **Also**: https://github.com/JonasGeiping/data-poisoning
- **Paper**: ICLR 2021
- **Approach**: Gradient matching to craft imperceptible adversarial patterns in training data
- **Strategies**: `--recipe` flag supports gradient-matching, poison-frogs, watermark, metapoison
- **Key**: First to cause targeted misclassification on full ImageNet from scratch
- **Rating: MEDIUM** — research-oriented; `brew_poison.py` is a nice entry point

### 12. TrojAI (NIST/JHU-APL)
- **Repo**: https://github.com/trojai/trojai
- **Paper**: arxiv.org/abs/2003.07233
- **Docs**: https://trojai.readthedocs.io
- **Install**: `pip install trojai`
- **Approach**: Python tools for generating triggered (poisoned) datasets AND trojaned models at scale
- **Modules**: `datagen` (synthetic data generation) + `modelgen` (DNN model generation with trojans)
- **Key**: NIST-backed, designed for generating trojan detection benchmarks at scale
- **Rating: MEDIUM-HIGH** — pip-installable, scale-oriented, but primarily for benchmark generation

---

## Trigger Type Taxonomy

| Trigger Type | Example Attacks | Visibility | Complexity |
|-------------|----------------|-----------|-----------|
| **Patch** (fixed pixel pattern) | BadNets | Visible if inspected | Simplest |
| **Blended** (image overlay) | Blended Attack | Semi-visible | Low |
| **Sinusoidal signal** | SIG | Low visibility | Low |
| **Reflection** | ReFool | Natural-looking | Medium |
| **Warping** (geometric) | WaNet | Invisible | Medium |
| **Frequency domain** (DCT) | FTrojan, LF | Invisible | Medium |
| **Sample-specific** (steganography) | SSBA, ISSBA | Invisible | High |
| **Dynamic** (learned per-input) | Input-Aware, LIRA | Invisible | High |
| **Adversarial perturbation** (clean-label) | Narcissus, LC, COMBAT | Invisible | High |
| **Feature collision** | Poison Frogs, Bullseye | Invisible | High |

---

## Educational Demo Suitability Assessment

### Tier 1: Best for Demos (start here)

| Tool | Why | Demo Scenario |
|------|-----|--------------|
| **ART** (IBM) | pip install, Jupyter notebooks pre-built, multi-framework | "Run this notebook to see a backdoor in action" |
| **BackdoorBench** | 16 attacks, CLI-driven, leaderboard | "Compare 5 trigger types on CIFAR-10" |
| **BackdoorBox** | Clean standalone files, flexible outputs | "Read one .py file, understand one attack" |
| **Narcissus** | 3 images = 99.89% attack success | "Poison a model with just 3 images" |

### Tier 2: Good for Intermediate

| Tool | Why | Demo Scenario |
|------|-----|--------------|
| **TrojAI** (NIST) | pip install, scale-oriented | "Generate 100 trojaned models for detection" |
| **Witches' Brew** | Multiple recipes, brew_poison.py | "Craft invisible poison for ImageNet" |
| **WaNet** (standalone) | Visual warping demo | "Show how geometric distortion hides triggers" |

### Tier 3: Advanced / Research Only

| Tool | Why |
|------|-----|
| **TrojanZoo** | Powerful but steeper learning curve |
| **FTrojan** | Frequency domain requires DSP background |
| **Input-Aware** | Dynamic trigger generation needs training |
| **COMBAT** | Latest clean-label technique |
| **CorruptEncoder** | Contrastive learning specific |

---

## Recommended Demo Pipeline

For an educational demonstration of backdoor attacks:

1. **Start with ART** — `pip install adversarial-robustness-toolbox`, run the `PoisoningAttackBackdoor` notebook on CIFAR-10 with a simple patch trigger. Shows the concept in ~20 lines of code.

2. **Show the spectrum** — Use BackdoorBench to run BadNets (visible patch), Blended (semi-visible), and WaNet (invisible warping) on the same dataset. Compare attack success rate vs. human detectability.

3. **Dramatic demo** — Use Narcissus to show that 3 carefully crafted images can backdoor a face recognition model with 99.89% success.

4. **Defense perspective** — Use BackdoorBench's 28 defense implementations to show detection/mitigation, or ART's built-in defense modules.

---

## Resource Lists (for further reading)

- **Awesome Backdoor in Deep Learning**: https://github.com/zihao-ai/Awesome-Backdoor-in-Deep-Learning
- **Backdoor Learning Resources** (Yiming Li): https://github.com/THUYimingLi/backdoor-learning-resources
- **Awesome Data Poisoning & Backdoor Attacks**: https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks (no longer maintained, latest ACL 2024)
- **NIST TrojAI Literature**: https://github.com/usnistgov/trojai-literature
- **OpenBackdoor** (NLP, not CV, but relevant): https://github.com/thunlp/OpenBackdoor — NeurIPS 2022, 12 text backdoor attacks

---

## NLP Crossover Note

While this research focuses on CV, **OpenBackdoor** (https://github.com/thunlp/OpenBackdoor) provides an analogous toolkit for text backdoor attacks (NeurIPS 2022 Spotlight). It implements 12 attack methods and 5 defense methods for NLP classification, using a modular pipeline (Dataset → Victim → Attacker → Poisoner → Trainer → Defender). Relevant if the educational demo scope expands beyond vision.
