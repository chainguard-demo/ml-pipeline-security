# Security Benchmark Datasets for Poisoning Defense Evaluation

## Summary

Contrary to what one might expect, there **are** several established benchmarks specifically for evaluating poisoning and backdoor defenses. The space is more mature than many adjacent ML security areas, largely driven by IARPA/NIST investment and active academic competition. I found 11 significant benchmarks/toolkits, with 3-4 being clearly dominant.

---

## 1. BackdoorBench (Most Comprehensive — CV)

**What it is:** A comprehensive, modular benchmark for backdoor learning covering attacks, defenses, and analysis.

- **URL:** https://github.com/SCLBD/BackdoorBench / http://backdoorbench.com
- **Paper:** NeurIPS 2022 Datasets & Benchmarks track; updated 2024 version in IJCV
- **Attack types covered:** 20 attack methods (BadNets, Blended, WaNet, SSBA, InputAware, SIG, LC, LF, CTRL, TrojanNN, BppAttack, etc.)
- **Defense types covered:** 32 defense methods
- **Datasets:** CIFAR-10, CIFAR-100, GTSRB, Tiny-ImageNet (4 datasets)
- **Models:** PreActResNet18, VGG19-BN, ConvNeXt-Tiny, ViT-B-16
- **Scale:** 11,492 attack-vs-defense evaluation pairs across 5 poisoning ratios
- **Analysis tools:** 18 tools including t-SNE, Shapley value, Grad-CAM, frequency saliency maps, neuron activation
- **Features:** Leaderboard, model zoo, standardized protocol
- **Adoption:** High — NeurIPS publication, active GitHub, used as reference benchmark in many papers
- **Workshop relevance:** ★★★★★ — This is the gold standard. Could directly use their evaluation protocol for workshop demos. Pre-trained poisoned models available in model zoo.

---

## 2. IARPA/NIST TrojAI Program

**What it is:** A government-funded program with public challenge rounds for Trojan/backdoor detection in AI models.

- **URL:** https://pages.nist.gov/trojai/ (leaderboard), https://www.iarpa.gov/research-programs/trojai
- **Data:** https://pages.nist.gov/trojai/docs/data.html
- **Attack types covered:** Various triggers across multiple domains — image classification, NLP, cybersecurity, reinforcement learning
- **Format:** Sets of trained AI models, some poisoned with known (but withheld) triggers; participants build detectors
- **Funding:** $7.22M to SRI alone; multi-team program
- **Key participants:** SRI, JHU/APL (data generation), multiple performer teams
- **Adoption:** High in government/defense ML security circles; public leaderboard
- **Unique aspects:**
  - Models are pre-trained and provided as black/gray boxes
  - Focus on **detecting** whether a model is trojaned, not on the attack itself
  - Multiple challenge rounds with increasing difficulty
  - Covers multiple modalities (vision, NLP, RL, cyber)
- **Workshop relevance:** ★★★★☆ — Excellent for demonstrating real-world evaluation scenarios. The "given a model, detect if it's poisoned" framing is very practical. Data is publicly available.

---

## 3. OpenBackdoor (NLP/Text Backdoors)

**What it is:** Open-source toolkit for textual backdoor attack and defense evaluation.

- **URL:** https://github.com/thunlp/OpenBackdoor
- **Paper:** NeurIPS 2022 Datasets & Benchmarks (Spotlight)
- **Attack methods:** 12 attack methods
- **Defense methods:** 5 defense methods
- **Tasks/Datasets:** 5 tasks, 11 datasets
- **Attack scenarios:** Poisoned datasets, pre-trained models, and fine-tuned models
- **Metrics:** Grammar error increase, perplexity difference, sentence similarity
- **Framework:** Supports HuggingFace Transformers and Datasets
- **Adoption:** High — NeurIPS spotlight, active THUNLP group maintains it
- **Workshop relevance:** ★★★★☆ — Best option for NLP-specific backdoor demos. Clean modular design.

---

## 4. Trojan Detection Challenge (TDC)

**What it is:** Competition series for advancing trojan detection capabilities, evolving from CV to LLMs.

- **URL:** https://trojandetection.ai/
- **Editions:**
  - Original TDC: Image classification trojan detection, trigger synthesis, evasive trojan insertion
  - TDC 2023 (LLM Edition): NeurIPS 2023 competition — trojan detection in LLMs + red teaming
  - IEEE SaTML 2024: Trojan detection on aligned LLMs (ETH Zürich SPY Lab)
- **Tracks:**
  - Trojan Detection Track: Discover triggers in trojaned models
  - Trigger Synthesis Track: Predict trigger locations and shapes
  - Evasive Trojan Track: Insert trojans that resist detection
  - Red Teaming Track: Automated elicitation of undesirable behaviors
- **Code:** https://github.com/ethz-spylab/rlhf_trojan_competition
- **Adoption:** High — NeurIPS, SaTML venues; active competition community
- **Workshop relevance:** ★★★★☆ — Competition format is engaging for workshops. The "evasive trojan" track is particularly interesting for offense/defense dynamics.

---

## 5. IBM Adversarial Robustness Toolbox (ART)

**What it is:** Not a benchmark per se, but the most widely-used library that includes poisoning attack/defense implementations with evaluation pipelines.

- **URL:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **Docs:** https://adversarial-robustness-toolbox.readthedocs.io/
- **Coverage:** Evasion, Poisoning, Extraction, Inference
- **Frameworks:** TensorFlow, Keras, PyTorch, scikit-learn, XGBoost, LightGBM, CatBoost
- **Data types:** Images, tables, audio, video
- **Hosted by:** Linux Foundation AI & Data
- **Adoption:** Very high — industry standard for adversarial ML evaluation
- **Workshop relevance:** ★★★★☆ — Practical toolkit that wraps many attacks/defenses. Good for live demos because it provides a consistent API across methods.

---

## 6. PoisonBench (LLM-Focused)

**What it is:** Benchmark for evaluating LLM vulnerability to data poisoning during preference learning (RLHF/DPO).

- **URL:** https://arxiv.org/abs/2410.08811
- **Attack types:** 2 attack types across 8 realistic scenarios
- **Models evaluated:** 21 widely-used LLMs
- **Key findings:**
  - Scaling parameter size does NOT inherently improve poisoning resilience
  - Log-linear relationship between attack effect and poison ratio
  - Poisoning effects generalize to triggers not in the poisoned data
- **Adoption:** Moderate — relatively new (2024)
- **Workshop relevance:** ★★★☆☆ — Relevant for LLM-specific poisoning discussions, but less visual/demonstrable than CV benchmarks.

---

## 7. "Just How Toxic Is Data Poisoning?" Unified Benchmark

**What it is:** ICML 2021 paper providing a unified evaluation framework for both backdoor and (clean-label) data poisoning attacks.

- **Paper:** http://proceedings.mlr.press/v139/schwarzschild21a/schwarzschild21a.pdf
- **Code:** https://github.com/aks2203/poisoning-benchmark
- **Authors:** Schwarzschild et al.
- **Key contribution:** Unified evaluation of backdoor attacks AND triggerless poisoning attacks under the same framework
- **Format:** 100 batches of crafted poisons; leaderboard-style submissions require hosting poisoned datasets publicly
- **Key attacks evaluated:** Poison Frogs, Witches' Brew (gradient matching), Bullseye Polytope
- **Adoption:** High — ICML publication, widely cited, referenced by gradient-matching papers
- **Workshop relevance:** ★★★★☆ — The "unified" framing is useful for workshops because it bridges backdoor and clean-label poisoning, which are often treated separately.

---

## 8. BackdoorLLM

**What it is:** Comprehensive benchmark for backdoor attacks and defenses on LLMs.

- **URL:** https://arxiv.org/abs/2408.12798
- **Focus:** LLM-specific backdoor attacks and defenses
- **Adoption:** New (Aug 2024)
- **Workshop relevance:** ★★★☆☆ — Complements PoisonBench with different attack scenarios.

---

## 9. BackdoorMBTI (Multimodal)

**What it is:** Backdoor learning benchmark toolkit specifically for multimodal models.

- **URL:** https://arxiv.org/abs/2411.11006
- **Focus:** Multimodal backdoor defense evaluation
- **Adoption:** New (Nov 2024), adoption TBD
- **Workshop relevance:** ★★★☆☆ — Interesting for covering the multimodal angle which is increasingly relevant.

---

## 10. BackFed (Federated Learning)

**What it is:** Standardized benchmark for evaluating backdoor attacks in federated learning settings.

- **URL:** https://arxiv.org/abs/2507.04903
- **Datasets:** CIFAR-10, MNIST, Tiny-ImageNet
- **Focus:** Standardizing threat models, evaluation metrics across FL settings
- **Domains:** Vision and language
- **Adoption:** Very new (2025)
- **Workshop relevance:** ★★☆☆☆ — Niche FL focus, but relevant if federated learning poisoning is in scope.

---

## 11. MLCommons AILuminate (Adjacent — LLM Safety)

**What it is:** Not a poisoning benchmark, but the emerging industry standard for adversarial AI safety evaluation. Included for context.

- **URL:** https://mlcommons.org/benchmarks/ailuminate/
- **Paper:** https://arxiv.org/abs/2503.05731
- **Scale:** 43,090 adversarial prompts across 12 hazard categories
- **Focus:** Jailbreak resilience, not data poisoning — but the "Resilience Gap" metric (baseline vs. under-attack performance) is a useful concept
- **Adoption:** Very high — MLCommons industry backing
- **Workshop relevance:** ★★☆☆☆ — Different threat model (inference-time jailbreaks, not training-time poisoning), but useful reference for how the industry is standardizing adversarial evaluation.

---

## Landscape Assessment

### Maturity by Domain

| Domain | Benchmark Maturity | Best Resource |
|--------|-------------------|---------------|
| CV Backdoors | **High** — Well-established | BackdoorBench |
| CV Clean-Label Poisoning | **Moderate** — Focused benchmarks exist | Schwarzschild benchmark |
| NLP Backdoors | **High** — Multiple benchmarks | OpenBackdoor |
| LLM Poisoning | **Emerging** — 2024 entries | PoisonBench, BackdoorLLM |
| Multimodal | **Early** — Just starting | BackdoorMBTI |
| Federated Learning | **Early** — New in 2025 | BackFed |
| Model-Level Detection | **High** — Government-funded | NIST TrojAI |
| General Toolkit | **Mature** — Industry standard | IBM ART |

### Key Gaps

1. **No unified cross-domain benchmark** — CV, NLP, and multimodal benchmarks are separate ecosystems with different evaluation protocols
2. **Limited supply chain poisoning benchmarks** — Most benchmarks assume poisoned training data, not poisoned pre-trained models or poisoned dependencies (e.g., HuggingFace model hub attacks)
3. **Few benchmarks for foundation model fine-tuning poisoning** — The RLHF/DPO poisoning space (PoisonBench) is very new
4. **No benchmark for detecting poisoned datasets before training** — Most benchmarks focus on post-training detection or defense during training
5. **Limited real-world scenario evaluation** — Benchmarks use clean academic datasets (CIFAR, ImageNet); no benchmark tests poisoning in noisy, real-world data pipelines
6. **No benchmark for code poisoning** — Despite growing concern about poisoned code suggestions (e.g., via copilot-style tools), there's no standardized evaluation

### Workshop Recommendations

For a workshop testing scenario, the recommended stack would be:

1. **Primary:** BackdoorBench — comprehensive, has a model zoo, standardized protocol
2. **Live demo:** IBM ART — clean API, supports multiple frameworks, good for interactive demos
3. **Detection challenge:** NIST TrojAI data — "is this model trojaned?" is an engaging participant exercise
4. **NLP angle:** OpenBackdoor — if text-domain backdoors are in scope
5. **Discussion prompt:** PoisonBench findings — "scaling doesn't help" is a provocative result for workshop discussion

### Notable Meta-Resources

- **Awesome Data Poisoning (curated list):** https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks — comprehensive paper list (no longer maintained but still useful)
- **Awesome Data Poisoning (alternate):** https://github.com/ch-shin/awesome-data-poisoning
- **Jonas Geiping's poisoning implementations:** https://github.com/JonasGeiping/data-poisoning — reference implementations of gradient-matching and related attacks

---

## Sources

- [BackdoorBench (NeurIPS 2022)](https://github.com/SCLBD/BackdoorBench)
- [BackdoorBench IJCV 2025](https://link.springer.com/article/10.1007/s11263-025-02447-x)
- [NIST TrojAI Leaderboard](https://pages.nist.gov/trojai/)
- [IARPA TrojAI Program](https://www.iarpa.gov/research-programs/trojai)
- [OpenBackdoor (NeurIPS 2022)](https://github.com/thunlp/OpenBackdoor)
- [Trojan Detection Challenge](https://trojandetection.ai/)
- [ETH SPY Lab SaTML 2024 Competitions](https://spylab.ai/blog/results-competition/)
- [IBM ART](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- [PoisonBench](https://arxiv.org/abs/2410.08811)
- [Just How Toxic is Data Poisoning? (ICML 2021)](http://proceedings.mlr.press/v139/schwarzschild21a/schwarzschild21a.pdf)
- [Schwarzschild Poisoning Benchmark](https://github.com/aks2203/poisoning-benchmark)
- [BackdoorLLM](https://arxiv.org/abs/2408.12798)
- [BackdoorMBTI](https://arxiv.org/abs/2411.11006)
- [BackFed](https://arxiv.org/abs/2507.04903)
- [MLCommons AILuminate v1.0](https://mlcommons.org/benchmarks/ailuminate/)
- [Awesome Data Poisoning (Curated List)](https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks)
- [Witches' Brew: Gradient Matching](https://arxiv.org/abs/2009.02276)
- [Data Poisoning Survey 2025](https://iacis.org/iis/2025/4_iis_2025_433-442.pdf)
