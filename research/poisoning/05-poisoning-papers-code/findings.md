# Poisoning Attacks on Object Detection / Computer Vision — Papers with Code

Research survey conducted 2026-02-17. Focus: poisoning and backdoor attacks targeting
object detection and computer vision models, with released code artifacts.

## Summary

| Priority | Paper | Target | Code Quality | Models |
|----------|-------|--------|-------------|--------|
| **HIGH** | AnywhereDoor | Object Detection | Good | MMDetection (FRCNN, DETR, etc.) |
| **HIGH** | Attacking by Aligning | Object Detection | Moderate | YOLOv3, YOLOv8, FRCNN, DETR |
| **HIGH** | ODSCAN | OD Defense+Attacks | Good | SSD300 (6 attack types) |
| **HIGH** | Physical Backdoor Detectors | Object Detection | Good | YOLOv5, FRCNN, DETR, DINO |
| **HIGH** | Mask-based Invisible Backdoor | Object Detection | TBD | Object detectors |
| **HIGH** | BackdoorBench | Classification benchmark | Excellent | 20 attacks, 32 defenses |
| **HIGH** | Witches' Brew / data-poisoning | Classification | Excellent | ResNets, VGG, ImageNet models |
| **MED** | Shadowcast (VLM Poisoning) | VLMs | Good | LLaVA-1.5, MiniGPT-4 |
| **MED** | Narcissus | Classification | Good | ResNet-18, CIFAR-10 |
| **MED** | BadDet/BadDet+ | Object Detection | No code | FRCNN, YOLO, FCOS, DINO |
| **MED** | TrojAI NIST | OD Benchmark | Official | SSD, FRCNN, DETR |
| **LOW** | ART (IBM) | General toolkit | Excellent | Many |

---

## TIER 1: Object Detection — Attack Papers with Code

### 1. AnywhereDoor: Multi-Target Backdoor Attacks on Object Detection
- **Authors:** Jialin Lu et al. (HKU)
- **Venue:** arXiv 2024 (2411.14243)
- **Paper:** https://arxiv.org/abs/2411.14243
- **Code:** https://github.com/HKU-TASR/AnywhereDoor (official)
- **Attack Description:** Multi-target backdoor attack enabling adversaries to specify
  different attack types at inference time:
  - Object vanishing (make objects disappear)
  - Object fabrication (inject fake detections)
  - Object misclassification (change class labels)
  - Untargeted or targeted with specific classes
- **Key Innovations:**
  1. Objective disentanglement — supports diverse attack combinations
  2. Trigger mosaicking — robust against region-based detectors
  3. Strategic batching — handles object-level data imbalances
- **Models:** Built on MMDetection framework (Faster R-CNN, RetinaNet, etc.)
- **Datasets:** VOC2007/2012, COCO 2017
- **Performance:** ~80% ASR improvement over adapted existing methods
- **Reproducibility:** Good. Official code, pretrained models on Google Drive,
  evaluation scripts. Depends on specific CUDA versions. Some features "Coming Soon."

---

### 2. Attacking by Aligning: Clean-Label Backdoor Attacks on Object Detection
- **Authors:** Chengze et al.
- **Venue:** arXiv 2023 (2307.10487)
- **Paper:** https://arxiv.org/abs/2307.10487
- **Code:** https://github.com/CHENGEZ/Attacking-by-Aligning (official)
- **Attack Description:** Clean-label backdoor attack (no annotation modification needed).
  Two attack scenarios:
  1. ODA (Object Disappearance Attack) — objects vanish from detection
  2. OGA (Object Generation Attack) — fake objects appear
- **Models:** YOLOv3, YOLOv8, Faster R-CNN, DETR (via MMDetection)
- **Datasets:** MSCOCO2017, BDD100k
- **Performance:** >92% attack success rate with only 5% poison rate
- **Reproducibility:** Moderate. Detailed command examples, clear pipeline stages,
  but no version pinning in requirements.txt. Hardcoded dataset paths.
- **Code Structure:**
  - `source/` — data poisoning scripts (ODA/OGA)
  - `yolov3/`, `yolov8/` — model-specific training
  - `mmdet/` — Faster RCNN/DETR via MMDetection

---

### 3. On the Credibility of Backdoor Attacks Against Object Detectors in the Physical World
- **Authors:** Bao Gia Doan et al. (Adelaide Auto-IDLab)
- **Venue:** ACSAC 2024 (received ACSAC reproducibility badge)
- **Paper:** https://arxiv.org/abs/2408.12122
- **Code:** https://github.com/AdelaideAuto-IDLab/PhysicalBackdoorDetectors (official)
- **Dataset:** https://sites.google.com/view/drive-by-fly-by/drivebyflyby
- **Attack Description:** Physical-world backdoor attacks using MORPHING method.
  Evaluated with real driving/drone video footage. Four attack types:
  - Misclassification, evasion (delete boxes), localization (move boxes), injection (add boxes)
- **Models:** YOLOv5, Faster R-CNN, DETR, DINO, TPH-YOLO (drone detection)
- **Datasets:** MTSD (traffic signs), custom drone vehicle dataset
- **Reproducibility:** Good. Well-structured codebase with clear separation of concerns.
  ACSAC artifact evaluation badge confirms third-party reproducibility. Requires form
  submission for pretrained weights. Specifies GPU requirements (NVIDIA A6000).

---

### 4. Mask-based Invisible Backdoor Attacks on Object Detection
- **Authors:** Jeongjin Shin
- **Venue:** IEEE ICIP 2024
- **Paper:** https://arxiv.org/abs/2405.09550
- **Code:** https://github.com/jeongjin0/invisible-backdoor-object-detection (official)
- **Attack Description:** First invisible backdoor attack for object detection using
  mask-based small perturbations as triggers. Three attack scenarios:
  1. Object disappearance
  2. Object misclassification
  3. Object generation
- **Reproducibility:** Official implementation. Python 3.7, PyTorch.

---

### 5. ODSCAN: Backdoor Scanning for Object Detection Models
- **Authors:** Siyuan Cheng et al. (Purdue)
- **Venue:** IEEE S&P 2024
- **Paper:** https://www.cs.purdue.edu/homes/cheng535/static/papers/sp24_odscan.pdf
- **Code:** https://github.com/Megum1/ODSCAN (official)
- **Description:** Defense-oriented trigger inversion technique. Evaluated on 334 benign
  + 360 trojaned models across 4 architectures and **6 attack types**. >0.9 ROC-AUC.
- **Why Relevant:** The repo includes implementations of 6 different backdoor attacks
  used for evaluation. Both attacks and defense are reproducible.
- **Models:** SSD300 (primary), modular design for extension
- **Attack Types:** Object misclassification, object appearing (foreground/background)
- **Reproducibility:** Good. Official repo with conda environment, data download via
  Google Drive. Top-tier venue (S&P). Well-documented with parameter tables.

---

### 6. BadDet: Backdoor Attacks on Object Detection (foundational, no official code)
- **Authors:** Shih-Han Chan, Yinpeng Dong, Jun Zhu, Xiaolu Zhang, Jun Zhou
- **Venue:** ECCV 2022 Workshop
- **Paper:** https://arxiv.org/abs/2205.14497
- **Code:** No official code. Unofficial defense: https://github.com/jeongjin0/detector-cleanse
- **Attack Types:** Four backdoor attacks for object detection:
  1. Object Generation — trigger creates fake objects
  2. Regional Misclassification — trigger changes nearby object class
  3. Global Misclassification — single trigger changes all predictions
  4. Object Disappearance — trigger makes target class undetectable
- **Models:** Faster-RCNN, YOLOv3
- **Note:** Foundational paper. BadDet+ (Jan 2026, arXiv 2601.21066) extends to FCOS,
  Faster RCNN, and DINO with improved robustness, but no code released yet either.

---

### 7. BadLANE: Robust Physical-world Backdoor Attacks on Lane Detection
- **Authors:** Veee9 et al.
- **Venue:** ACM Multimedia 2024
- **Code:** https://github.com/Veee9/BadLANE
- **Description:** Physical-world backdoor attacks on lane detection in autonomous driving.
  Uses common physical objects (e.g., traffic cones) as triggers to cause wrong lane
  detections, leading vehicles off-road or into oncoming traffic.

---

## TIER 2: Computer Vision Classification — Poisoning with Code

### 8. BackdoorBench: Comprehensive Benchmark of Backdoor Learning
- **Authors:** Baoyuan Wu et al.
- **Venue:** NeurIPS 2022 (Datasets & Benchmarks)
- **Paper:** https://arxiv.org/abs/2206.12654
- **Code:** https://github.com/SCLBD/BackdoorBench (official)
- **Website:** https://backdoorbench.github.io/
- **Description:** THE comprehensive benchmark for backdoor attacks and defenses.
  - **20 attack methods** implemented (BadNets, Blended, WaNet, SSBA, LIRA, etc.)
  - **32 defense methods** implemented
  - **18 analysis tools** (t-SNE, Shapley, Grad-CAM, frequency saliency, neuron activation)
  - 11,492 attack-vs-defense evaluation pairs
  - 5 poisoning ratios x 4 DNN models x 4 datasets
- **Scope:** Image classification (CIFAR-10, CIFAR-100, GTSRB, Tiny ImageNet)
- **Reproducibility:** Excellent. Modular codebase, extensive documentation. Best
  starting point for understanding the backdoor attack landscape.

---

### 9. Witches' Brew / Data Poisoning Framework (Gradient Matching)
- **Authors:** Jonas Geiping et al.
- **Venue:** ICLR 2021
- **Paper:** https://arxiv.org/abs/2009.02276
- **Code:** https://github.com/JonasGeiping/poisoning-gradient-matching (Witches' Brew)
- **Code:** https://github.com/JonasGeiping/data-poisoning (unified framework)
- **Attack Methods (unified repo):**
  1. Gradient Matching (Witches' Brew)
  2. Poison Frogs (clean-label feature collision)
  3. Bullseye Polytope
  4. MetaPoison
  5. Hidden-Trigger Backdoor
  6. Convex Polytope
  7. Watermarking
  8. Patch Attacks (BadNets)
- **Models:** ResNets, WideResNets, VGG, ConvNet, EfficientNet, all torchvision ImageNet models
- **Datasets:** CIFAR-10, CIFAR-100, MNIST, ImageNet
- **Reproducibility:** Excellent. Comprehensive documentation, distributed training support
  (SLURM, PBS), defense implementations included. Modular Kettle/Victim/Witch architecture.
  Best framework for targeted clean-label poisoning research.

---

### 10. Narcissus: Clean-Label Backdoor Attack
- **Authors:** REDS Lab
- **Venue:** ACM CCS 2023
- **Paper:** CCS'23 proceedings
- **Code:** https://github.com/reds-lab/Narcissus (official)
- **Attack Description:** Clean-label backdoor requiring only 3 images to poison face
  recognition. 99.89% attack success rate. Four-stage pipeline:
  1. Poi-warm-up (surrogate model training)
  2. Trigger generation (inward-pointing noise)
  3. Trigger insertion (minimal poisoned examples)
  4. Test query manipulation
- **Models:** ResNet-18 (default), modular for other architectures
- **Datasets:** CIFAR-10, Tiny ImageNet, PubFig
- **Reproducibility:** Good. Jupyter notebook for quick demo. `narcissus_gen()` one-function API.
  Python 3.6+, PyTorch 1.10.1+, CUDA 11.0.

---

### 11. WaNet: Imperceptible Warping-based Backdoor Attack
- **Authors:** VinAI Research
- **Venue:** ICLR 2021
- **Paper:** https://openreview.net/forum?id=eEn8KTtJOx
- **Code:** https://github.com/VinAIResearch/Warping-based_Backdoor_Attack-release (official)
- **Description:** Uses image warping (not patches) as imperceptible trigger. Novel "noise
  mode" training makes attack undetectable by machine defenders.
- **Also in:** BackdoorBench, BackdoorBox

---

### 12. Hidden Trigger Backdoor Attacks
- **Authors:** UMBC Vision
- **Venue:** AAAI 2020
- **Code:** https://github.com/UMBCvision/Hidden-Trigger-Backdoor-Attacks (official)
- **Description:** Poisoned data looks natural with correct labels; trigger is hidden.

---

### 13. BadNets: Evaluating Backdooring Attacks on Deep Neural Networks
- **Authors:** Tianyu Gu et al.
- **Venue:** IEEE Access 2019 (originally 2017)
- **Paper:** https://arxiv.org/abs/1708.06733
- **Code:** https://github.com/Kooscii/BadNets (unofficial but complete)
- **Description:** The foundational backdoor attack paper. Demonstrates backdoored
  handwritten digit classifier and a US street sign classifier that identifies
  stop signs as speed limits when a special sticker is added.

---

### 14. Shadowcast: Stealthy Data Poisoning Against Vision-Language Models
- **Authors:** Yuancheng Xu et al. (UMD, UIUC, Salesforce, Apple, Waterloo)
- **Venue:** NeurIPS 2024
- **Paper:** https://arxiv.org/abs/2402.06659
- **Code:** https://github.com/umd-huang-lab/VLM-Poisoning (official)
- **Attack Types:**
  1. Label Attack — misidentify classes (e.g., Trump → Biden)
  2. Persuasion Attack — craft misleading narratives (junk food → health food)
- **Models:** LLaVA-1.5, MiniGPT-4
- **Effectiveness:** ~50 poison samples sufficient. Transferable across VLM architectures.
- **Reproducibility:** Good. Clear pipeline scripts. Note: code release described as
  "gradual." Label attacks work without GPT API access; persuasion attacks need Azure OpenAI.

---

### 15. CorruptEncoder: Data Poisoning Backdoor Attacks to Contrastive Learning
- **Venue:** CVPR 2024
- **Code:** https://github.com/jzhang538/CorruptEncoder (official)
- **Description:** Backdoor attacks targeting contrastive learning (CLIP-like models).
  0.5% default poisoning ratio. Relevant to vision foundation model pipelines.

---

### 16. SSL-Backdoor: Backdoor Attacks on Self-Supervised Learning
- **Venue:** CVPR 2022
- **Code:** https://github.com/UMBCvision/SSL-Backdoor (official)
- **Description:** Attacks targeting self-supervised visual representation learning.

---

## TIER 3: 3D / LiDAR Object Detection Attacks

### 17. LiDAttack: Robust Black-box Attack on LiDAR-based Object Detection
- **Code:** https://github.com/Cinderyl/LiDAttack
- **Models:** PointRCNN, PointPillar, PV-RCNN++
- **Datasets:** KITTI, nuScenes
- **Performance:** Up to 90% attack success rate. Validated indoors and outdoors.

### 18. IRBA: Imperceptible and Robust Backdoor Attack in 3D Point Cloud
- **Code:** https://github.com/KuofengGao/IRBA
- **Venue:** IEEE TIFS 2023

### 19. PointCRT: Detecting Backdoor in 3D Point Cloud via Corruption Robustness
- **Code:** https://github.com/CGCL-codes/PointCRT
- **Venue:** ACM MM 2023

---

## TIER 4: Benchmarks, Toolkits, and Datasets

### 20. TrojAI (NIST/IARPA)
- **Website:** https://pages.nist.gov/trojai/
- **Code (library):** https://github.com/trojai/trojai
- **Code (examples):** https://github.com/usnistgov/trojai-example
- **Description:** Government-funded benchmark for trojan detection in AI. Includes
  **object detection rounds** with trojaned models:
  - Round 10 (Jul 2022): COCO dataset, 144 train + 144 test + 144 holdout models
  - Round 13 (Feb 2023): Traffic signs on Cityscapes/GTA5/DOTA_v2
    - Models: SSD, Faster R-CNN, DETR
    - Triggers: misclassification, evasion, localization, injection
    - 128 train + 192 test + 192 holdout models
    - Available via Google Drive or NIST data portal
- **Reproducibility:** Excellent. Government-backed, well-documented, downloadable datasets.
  Best source of pre-built trojaned object detection models.

### 21. Adversarial Robustness Toolbox (ART) — IBM
- **Code:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **Docs:** https://adversarial-robustness-toolbox.readthedocs.io/
- **Description:** Comprehensive Python library for ML security covering evasion,
  poisoning, extraction, and inference attacks. Supports classification AND object
  detection. Includes Witches' Brew implementation as notebook. PyPI installable.
- **Reproducibility:** Excellent. Industry-standard, maintained by Linux Foundation AI.

### 22. BackdoorBox: Python Toolbox for Backdoor Learning
- **Code:** https://github.com/THUYimingLi/BackdoorBox
- **Description:** Open-sourced Python toolbox implementing representative backdoor
  attacks and defenses. Image classification focused. Includes WaNet, BadNets, etc.

### 23. Awesome Lists (curated paper collections)
- Backdoor Learning Resources: https://github.com/THUYimingLi/backdoor-learning-resources
- Awesome Data Poisoning: https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks
- Awesome 3D Point Cloud Attacks: https://github.com/cuge1995/awesome-3D-point-cloud-attacks
- Data Poisoning Survey (2025): https://github.com/Pinlong-Zhao/Data-Poisoning

---

## Key Observations

### Object Detection is Under-Studied
Most backdoor/poisoning research focuses on image classification. Object detection
poisoning is a newer, less mature research area. The main OD-specific papers with
code are: AnywhereDoor, Attacking-by-Aligning, ODSCAN, PhysicalBackdoorDetectors,
and the Mask-based Invisible attack. BadDet (the foundational OD paper) has no
official code release.

### Most Reproducible Starting Points
For someone wanting to reproduce object detection poisoning:
1. **Start with ODSCAN** — has 6 attack implementations + defense, top venue (S&P)
2. **AnywhereDoor** — most flexible multi-target OD attack
3. **Attacking-by-Aligning** — clean-label OD attack across 4 detector architectures
4. **TrojAI Round 13** — pre-built trojaned OD models ready to analyze
5. **ART toolkit** — if you want a general-purpose framework

### For Classification Baselines
1. **BackdoorBench** — 20 attacks, 32 defenses, comprehensive
2. **Witches' Brew / data-poisoning** — best clean-label targeted poisoning framework
3. **Narcissus** — most practical clean-label attack (3 images sufficient)

### Code Quality Rankings
- **Excellent:** BackdoorBench, ART, Witches' Brew/data-poisoning, TrojAI
- **Good:** ODSCAN, AnywhereDoor, PhysicalBackdoorDetectors, Narcissus, Shadowcast
- **Moderate:** Attacking-by-Aligning (missing version pins)
- **No code:** BadDet, BadDet+, Dangerous Cloaking
