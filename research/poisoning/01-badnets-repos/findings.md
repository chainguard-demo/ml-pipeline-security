# Backdoor Attack Papers & Code Repositories

Research survey of foundational backdoor/trojan attack papers with released code.
Focus: papers with working implementations that could be adapted for workshop demos.

---

## 1. FOUNDATIONAL ATTACK PAPERS WITH CODE

### 1.1 BadNets (2017) — THE Original Backdoor Paper

**Paper:** Gu, Dolan-Gavitt, Garg. "BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain." arXiv:1708.06733, 2017.
- Published at Machine Learning and Computer Security Workshop (NeurIPS 2017), later IEEE Access 2019
- First paper to demonstrate backdoor attacks on deep neural networks

**Attack Method:**
- Poison a subset of training data by stamping a trigger pattern (e.g., small pixel patch) onto images and relabeling them to target class
- Model learns to associate trigger with target label while maintaining clean accuracy
- Demo scenarios: handwritten digit classifier, US traffic sign classifier (stop sign → speed limit)

**Code:** https://github.com/Kooscii/BadNets
- **Framework:** Caffe (C++/Python), Faster R-CNN
- **Status:** Inactive since ~2018, README says "code WIP"
- **Datasets:** US Traffic Signs (UCSD VivaChallenge)
- **Workshop Suitability: LOW** — Caffe is obsolete, complex setup, incomplete code
- **Note:** This is a re-implementation, not the original authors' code. The original NYU group did not release a standalone repo.

---

### 1.2 TrojanNN (NDSS 2018)

**Paper:** Liu, Ma, Aafer, Lee, Zhai, Wang, Zhang. "Trojaning Attack on Neural Networks." NDSS 2018.
- Proposes trojaning without access to original training data
- Reverse-engineers training data, generates trigger via network inversion, retrains to inject backdoor

**Attack Method:**
- Invert neural network to find trigger that maximally activates chosen internal neurons
- Retrain model with synthetic trigger-stamped inputs to inject backdoor
- Works across vision, speech, sentiment analysis tasks

**Code:** https://github.com/PurduePAML/TrojanNN
- **Framework:** Python 2.7 + Caffe + Theano
- **Stars:** ~191
- **Status:** Inactive since ~2018
- **Datasets:** VGG Face, Pannous Speech, Adience age, Cornell Movie Reviews
- **Workshop Suitability: LOW** — Python 2.7, Caffe/Theano are dead frameworks, complex setup

---

### 1.3 Clean-Label Backdoor Attacks (2019)

**Paper:** Turner, Tsipras, Madry. "Label-Consistent Backdoor Attacks." arXiv:1912.02771.
- From Madry Lab (MIT) — high-profile ML security group
- Key insight: attacks where poisoned samples have CORRECT labels (harder to detect)
- Uses adversarial perturbations + GAN interpolation to suppress natural features before embedding trigger

**Attack Method:**
- Generate adversarial perturbations on target-class images
- Overlay trigger pattern on perturbed images (labels stay correct)
- Poisoned data blends into target class distribution but contains hidden trigger

**Code:** https://github.com/MadryLab/label-consistent-backdoor-code
- **Framework:** TensorFlow + NumPy
- **Stars:** ~57
- **Status:** Last update Nov 2020
- **Datasets:** CIFAR-10 (pre-poisoned datasets provided)
- **Workshop Suitability: MEDIUM** — TensorFlow (not ideal), but has pre-made datasets and clear config.json workflow. Setup script automates data download. Good conceptual demo for "clean-label" vs "dirty-label" attacks.

---

### 1.4 WaNet — Warping-Based Backdoor (ICLR 2021)

**Paper:** Nguyen, Tran. "WaNet — Imperceptible Warping-based Backdoor Attack." ICLR 2021.
- Uses image warping (geometric distortion) as trigger instead of pixel patches
- Virtually invisible to human inspection — outperforms prior methods in human inspection tests
- Novel "noise mode" training makes backdoor undetectable by machine defenses

**Attack Method:**
- Apply smooth spatial warping transformation as trigger (no pixel-level modification)
- Train with mix of clean, poisoned, and noise-augmented images
- Noise mode prevents defense methods from distinguishing poisoned vs clean training dynamics

**Code:** https://github.com/VinAIResearch/Warping-based_Backdoor_Attack-release
- **Framework:** PyTorch
- **Stars:** ~135
- **Status:** 25 commits, from Feb 2021
- **Datasets:** MNIST, CIFAR-10, GTSRB, CelebA
- **Includes:** Defense experiments (fine-pruning, Neural Cleanse, STRIP), pretrained checkpoints
- **Workshop Suitability: HIGH** — PyTorch, clean code, simple CLI (`python train.py --dataset cifar10 --attack_mode all2one`), multiple datasets, includes defense evaluations. Great for showing "invisible" triggers.

---

### 1.5 Input-Aware Dynamic Backdoor (NeurIPS 2020)

**Paper:** Nguyen, Tran. "Input-Aware Dynamic Backdoor Attack." NeurIPS 2020.
- Each input gets a DIFFERENT trigger (sample-specific), unlike BadNets' fixed trigger
- Uses a trigger generator network driven by diversity loss
- Cross-trigger test enforces trigger non-reusability

**Attack Method:**
- Train trigger generator alongside classifier
- Generator produces unique trigger for each input image
- Diversity loss ensures triggers vary enough to avoid detection

**Code:** https://github.com/VinAIResearch/input-aware-backdoor-attack-release
- **Framework:** PyTorch
- **Stars:** Moderate
- **Datasets:** MNIST, CIFAR-10, GTSRB, CelebA
- **Workshop Suitability: HIGH** — Same VinAI group as WaNet, similar clean PyTorch setup

---

### 1.6 LIRA — Learnable, Imperceptible, Robust Backdoor (ICCV 2021)

**Paper:** Doan, Lao, Zhao, Li. "LIRA: Learnable, Imperceptible and Robust Backdoor Attacks." ICCV 2021.
- Learns the trigger pattern as part of training (not hand-designed)
- Two-stage: (1) learn trigger generator, (2) poison and fine-tune classifier
- Optimized for imperceptibility + robustness to defenses

**Code:** https://github.com/khoadoan106/backdoor_attacks
- **Framework:** PyTorch
- **Datasets:** MNIST, CIFAR-10, others
- **Workshop Suitability: MEDIUM** — Good concept, but slightly more complex setup than WaNet

---

### 1.7 ISSBA — Invisible Sample-Specific Backdoor (ICCV 2021)

**Paper:** Li, Li, Wu, Li, He, Lyu. "Invisible Backdoor Attack with Sample-Specific Triggers." ICCV 2021.
- Encodes trigger into image using encoder-decoder (steganography-based)
- Sample-specific: each poisoned image has a unique trigger
- Invisible to human inspection

**Code:** https://github.com/yuezunli/ISSBA (also https://github.com/SCLBD/ISSBA)
- **Framework:** PyTorch
- **Workshop Suitability: MEDIUM-HIGH** — Interesting steganography angle, PyTorch

---

### 1.8 Hidden Trigger Backdoor (AAAI 2020)

**Paper:** Saha, Subramanya, Pirsiavash. "Hidden Trigger Backdoor Attacks." AAAI 2020.
- Poisoned images look completely natural with correct labels
- Trigger is hidden — only revealed at test time
- Optimizes poisoned images in feature space

**Code:** https://github.com/UMBCvision/Hidden-Trigger-Backdoor-Attacks
- **Framework:** PyTorch
- **Workshop Suitability: MEDIUM**

---

### 1.9 Blind Backdoors (USENIX Security 2021)

**Paper:** Bagdasaryan, Shmatikov. "Blind Backdoors in Deep Learning Models." USENIX Security 2021.
- Attacker compromises training CODE (not data) — injects backdoor via loss computation
- "Blind": attacker can't see training data, observe execution, or access resulting model
- Demonstrates single-pixel, physical backdoors in ImageNet; privacy-violating covert tasks

**Attack Method:**
- Modify loss function to include backdoor objective
- Multi-objective optimization: high accuracy on both main task and backdoor task
- Creates poisoned inputs on-the-fly during training

**Code:** https://github.com/ebagdasa/backdoors101
- **Framework:** PyTorch, YAML config
- **Stars:** ~378
- **Includes:** Also implements "How To Backdoor Federated Learning" (AISTATS 2020)
- **Workshop Suitability: HIGH** — Modern PyTorch, YAML configs, clean architecture, supports centralized + federated learning, CIFAR-10/ImageNet/MNIST. Excellent for demonstrating code-level (not just data-level) attacks.

---

## 2. COMPREHENSIVE FRAMEWORKS / BENCHMARKS

These are not individual papers but unified codebases implementing many attacks. **Best starting points for workshops.**

### 2.1 BackdoorBench ⭐ RECOMMENDED FOR WORKSHOPS

**Paper:** "BackdoorBench: A Comprehensive Benchmark and Analysis of Backdoor Learning"
**Repo:** https://github.com/SCLBD/BackdoorBench
- **Stars:** ~583
- **Framework:** PyTorch 1.11+, Python 3.8
- **Last active:** 2024 (v2.2)

**Attacks (16):** BadNets, Blended, Blind, BPP, CTRL, FTrojan, Input-aware, LC, LF, LIRA, PoisonInk, ReFool, SIG, SSBA, TrojanNN, WaNet

**Defenses (28):** ABL, AC, ANP, CLP, D-BR, D-ST, DBD, EP, FP, FT, I-BAU, MCR, NAB, NAD, NC, NPD, RNP, SAU, SS + detection methods (STRIP, BEATRIX, SCAN, SPECTRE, SentiNet, TeCo)

**Datasets:** CIFAR-10, CIFAR-100, GTSRB, Tiny ImageNet
**Models:** PreAct-ResNet18, VGG19, ConvNeXT, ViT-B-16, MobileNetV3, EfficientNet-B3

**Why best for workshops:**
- Unified API — compare attacks/defenses side by side
- Public leaderboard
- YAML config + CLI args
- Comprehensive documentation and website
- Active maintenance

---

### 2.2 BackdoorBox

**Repo:** https://github.com/THUYimingLi/BackdoorBox
- **Stars:** ~642
- **Framework:** PyTorch 1.8+, Python 3.8
- **License:** GPL-2.0

**Attacks (16+):** BadNets, Blended, Refool, LabelConsistent, TUAP, SleeperAgent, ISSBA, WaNet, Blind, IAD, PhysicalBA, LIRA, BATT, AdaptivePatch, BAAT

**Defenses (10+):** AutoEncoder, ShrinkPad, FineTuning, Pruning, MCR, NAD, ABL, SCALE-UP, IBD-PSC, REFINE, FLARE

**Why useful:**
- More attacks than BackdoorBench in some categories
- Code examples in `tests/` folder
- Still under development (377+ commits)
- **Caveat:** No formal user manual yet

---

### 2.3 Backdoors101

**Repo:** https://github.com/ebagdasa/backdoors101
- **Stars:** ~378
- **Framework:** PyTorch, YAML config, TensorBoard
- **Focus:** Federated learning + centralized attacks

**Attacks:** Pixel-pattern, physical, semantic backdoors; data/batch/loss poisoning
**Defenses:** NeuralCleanse, SentiNet, spectral clustering, fine-pruning
**Datasets:** ImageNet, CIFAR-10, MNIST, PIPA, IMDB

**Why useful:**
- Only major framework with federated learning support
- Clean YAML-based config system
- Lightweight and well-architected (Helper → Task → Attack pipeline)

---

## 3. DEFENSE PAPERS WITH CODE (Bonus)

### 3.1 Neural Cleanse (IEEE S&P 2019)

**Paper:** Wang et al. "Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks."
**Code:** https://github.com/bolunwang/backdoor
- **Framework:** Keras + TensorFlow
- **Method:** Reverse-engineers potential triggers for each class, uses MAD (Median Absolute Deviation) to detect anomalous classes
- **Workshop Suitability:** MEDIUM — good for showing defense side, but Keras/TF

### 3.2 Spectral Signatures (NeurIPS 2018)

**Paper:** Tran, Li, Madry. "Spectral Signatures in Backdoor Attacks." NeurIPS 2018.
- **Method:** SVD on feature representations to detect poisoned samples
- **No standalone repo found** — implementations exist in BackdoorBench and BackdoorBox

---

## 4. NLP BACKDOOR ATTACKS WITH CODE

### 4.1 Hidden Backdoors in NLP (CCS 2021)

**Code:** https://github.com/lishaofeng/NLP_Backdoor
- Hidden backdoor attack on NLP systems

### 4.2 SOS — Stealthy NLP Backdoor (ACL 2021)

**Paper:** "Rethinking Stealthiness of Backdoor Attack against NLP Models"
**Code:** https://github.com/lancopku/SOS
- Inserts trigger words naturally into text
- Modifies trigger word embeddings for stealthy activation

---

## 5. CURATED RESOURCE LISTS

- **backdoor-learning-resources:** https://github.com/THUYimingLi/backdoor-learning-resources — Comprehensive paper list
- **Awesome-Backdoor-in-Deep-Learning:** https://github.com/zihao-ai/Awesome-Backdoor-in-Deep-Learning — Curated papers + resources
- **trojai-literature:** https://github.com/usnistgov/trojai-literature — NIST TrojAI program references

---

## 6. WORKSHOP DEMO RECOMMENDATIONS

### Tier 1: Best for Quick Demos
| What | Why | Effort |
|------|-----|--------|
| **BackdoorBench** (BadNets attack) | Unified framework, one-line CLI, multiple datasets | Low |
| **WaNet** (standalone) | Shows "invisible" triggers, clean PyTorch, pretrained models | Low |
| **backdoors101** (Blind Backdoor) | Code-level attack concept, YAML config, federated learning angle | Low-Medium |

### Tier 2: Good for In-Depth Exploration
| What | Why | Effort |
|------|-----|--------|
| **BackdoorBox** (multiple attacks) | Most attacks in one place, test examples | Medium |
| **Input-Aware Dynamic** (standalone) | Sample-specific triggers concept | Medium |
| **LIRA** (standalone) | Learned triggers concept | Medium |
| **Label-Consistent** (Madry Lab) | Clean-label attack concept, pre-made datasets | Medium |

### Tier 3: Historical/Educational Only
| What | Why | Effort |
|------|-----|--------|
| **BadNets** (Kooscii repo) | Historical importance only — Caffe, broken | High |
| **TrojanNN** (Purdue) | Foundational concept — Python 2.7, Caffe/Theano | High |

### Recommended Workshop Flow
1. **Start with BadNets concept** (use BackdoorBench implementation, not original repo)
2. **Show progression**: fixed trigger → clean-label → sample-specific → invisible warping
3. **Defense demo**: run Neural Cleanse or Spectral Signatures from BackdoorBench against the attacks
4. **Discussion**: code-level attacks (Blind Backdoors) as emerging threat

### Key Insight for Workshop Design
The original BadNets repo is essentially unusable (Caffe, WIP, 2018). But the BadNets *attack* is implemented in every modern framework. **Use BackdoorBench or BackdoorBox** to demonstrate BadNets alongside newer attacks in a unified, modern PyTorch environment.

---

*Last updated: 2026-02-17*
*Research agent: 01-badnets-repos*
