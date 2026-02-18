# Poisoned Dataset Repositories & Examples

**Research focus:** Pre-built poisoned/backdoored datasets (COCO, ImageNet, YOLO variants)
**Status:** Complete
**Date:** 2026-02-17

---

## Summary

Most poisoned datasets are **not distributed as ready-to-download poisoned image archives**. Instead, the ecosystem consists of:

1. **Benchmark toolkits** that generate poisoned versions of standard datasets on-the-fly (BackdoorBench, BackdoorBox, backdoor-toolbox)
2. **NIST TrojAI** which provides pre-poisoned *models* (not raw datasets) trained on COCO and other data
3. **Attack-specific repos** that include generation scripts to produce poisoned training sets
4. **Physical trigger datasets** containing real-world images with natural objects as backdoor triggers

The closest thing to "download a poisoned COCO/ImageNet" is **BackdoorBench's SharePoint archive**, which contains pre-generated poisoned train/test splits for CIFAR-10, CIFAR-100, GTSRB, and Tiny ImageNet with 16 different attack methods applied.

---

## 1. Pre-Built Poisoned Data Archives (Ready to Download)

### 1.1 BackdoorBench (Best Option for Ready-to-Use Data)

- **URL:** https://github.com/SCLBD/BackdoorBench
- **Paper:** NeurIPS 2022
- **Download:** SharePoint link in repo — each zip contains `bd_train_dataset`, `bd_test_dataset`, backdoored model, and triggers
- **Datasets:** CIFAR-10, CIFAR-100, GTSRB, Tiny ImageNet
- **Attack methods (16):** BadNets, Blended, Blind, BppAttack, CTRL, FTrojan, Input-aware, Label Consistent, Low Frequency, LIRA, PoisonInk, ReFool, SIG, SSBA, TrojanNN, WaNet
- **Defense methods (28):** ABL, AC, ANP, CLP, D-BR, D-ST, DBD, EP, BNP, FP, FT, FT-SAM, I-BAU, MCR, NAB, NAD, NC, NPD, RNP, SAU, SS, STRIP, BEATRIX, SCAN, SPECTRE, AGPD, SentiNet
- **Loading:** `load_attack_result()` from `utils/save_load_attack.py`
- **Availability:** Ready-to-use. Download, extract, load poisoned train/test data directly.
- **Limitation:** Does NOT include full-size ImageNet or COCO. Largest is Tiny ImageNet (64x64).

### 1.2 NIST TrojAI Object Detection Rounds (Poisoned Models on COCO)

Pre-poisoned **models** (not raw poisoned images) trained on COCO and other detection datasets. You get the model weights with embedded backdoors — useful for studying trojan detection rather than training from poisoned data.

#### Round 10 (Jul 2022) — COCO-based
- **URL:** https://pages.nist.gov/trojai/docs/object-detection-jul2022.html
- **Base dataset:** MS-COCO
- **Architectures:** SSD, Faster R-CNN (ResNet50)
- **Models:** 144 training / 144 test / 144 holdout (~50% poisoned)
- **Trigger types:** Misclassification (shift labels), Evasion (delete boxes); local or global scope; includes spurious (non-functional) triggers
- **Download:** Google Drive links in documentation
- **Ready-to-use:** Yes (poisoned models). No raw poisoned image dataset provided — models were trained on poisoned COCO internally.

#### Round 13 (Feb 2023) — COCO + DOTA + Synthetic
- **URL:** https://pages.nist.gov/trojai/docs/object-detection-feb2023.html
- **Base datasets:** Synthetic traffic signs (Cityscapes/GTA5 backgrounds), DOTA_v2 aerial imagery, COCO (for comparison)
- **Architectures:** SSD, Faster R-CNN, DETR
- **Models:** 128 training / 192 test / 192 holdout
- **Trigger types:** Misclassification, Evasion, Localization (shift boxes), Injection (add new boxes); conditional on spatial/color/texture/shape
- **Download:** Google Drive links in documentation
- **Ready-to-use:** Yes (poisoned models).

### 1.3 Natural Backdoor Dataset (Physical Triggers for Object Detection)

- **URL:** https://github.com/backdoorrrr/Natural-Backdoor-Dataset
- **Related paper:** "Dangerous Cloaking: Natural Trigger based Backdoor Attacks on Object Detectors in the Physical World"
- **Triggers:** T-shirt, hat, apple, glass — real physical objects used as cloaking triggers
- **Attack type:** Cloaking (person bounding box disappears when trigger object is present)
- **Base dataset:** Pascal VOC + custom images
- **T-shirt set:** ~14,593 images (14,041 from VOC), poisoning rate 0.14%–3.4%
- **Hat set:** ~15,910 images, max poisoning rate 3.4%
- **Tested on:** YOLOv3, YOLOv4, CenterNet, Faster R-CNN
- **Ready-to-use:** Yes — actual annotated images with physical triggers.

### 1.4 Physical Cloaking Backdoor Dataset (T-shirt)

- **URL:** https://github.com/garrisongys/T-shirt
- **Paper:** "Comprehensive Evaluation of Cloaking Backdoor Attacks on Object Detector in Real-World"
- **Content:** 552 training images + 19 test videos (~11,800 frames)
- **Trigger:** Natural T-shirts from market
- **Tested on:** YOLOv3, YOLOv4, Faster R-CNN, CenterNet
- **Ready-to-use:** Yes — real captured images/video with annotations.

---

## 2. Toolkits That Generate Poisoned Datasets (Require Generation)

### 2.1 BackdoorBox

- **URL:** https://github.com/THUYimingLi/BackdoorBox
- **Datasets:** CIFAR-10, ImageNet50, GTSRB, any via `torchvision.datasets.DatasetFolder`
- **Attacks (16):** BadNets, Blended, Refool, LabelConsistent, TUAP, SleeperAgent, ISSBA, WaNet, Blind, BATT, AdaptivePatch, BAAT, IAD, PhysicalBA, LIRA, BATT
- **Generation:** Call `.get_poisoned_dataset()` after configuring attack; generates poisoned data on the fly
- **Pre-generated data:** None available for download
- **Relevance:** Can generate poisoned ImageNet50 variants

### 2.2 backdoor-toolbox

- **URL:** https://github.com/vtu81/backdoor-toolbox
- **Datasets:** CIFAR-10, GTSRB (auto-download), ImageNet (manual), EMBER
- **Attacks:** BadNet, Blend, Trojan, Clean-Label, Dynamic, SIG, ISSBA, WaNet, Refool, TaCT, Adap-Blend, Adap-Patch, Adap-K-way, BadEncoder, BppAttack, TrojanNN, Wasserstein
- **Generation:** `python create_poisoned_set.py -dataset=[DATASET] -poison_type=[TYPE] -poison_rate=[RATE]`
- **Pre-generated data:** None
- **Relevance:** Good for generating poisoned ImageNet variants (requires ImageNet download first)

### 2.3 Poisoning Benchmark (Unified)

- **URL:** https://github.com/aks2203/poisoning-benchmark
- **Paper:** "Just How Toxic is Data Poisoning? A Unified Benchmark for Backdoor and Data Poisoning Attacks" (ICML 2021)
- **Focus:** Unified comparison of data poisoning vs backdoor attacks
- **Pre-generated data:** None — benchmark framework

---

## 3. Attack-Specific Repos with Generation Scripts

### 3.1 CorruptEncoder (Poisoned ImageNet for Contrastive Learning)

- **URL:** https://github.com/jzhang538/CorruptEncoder
- **Paper:** CVPR 2024
- **Dataset:** Generates poisoned ImageNet-100 subsets
- **Poisoning ratio:** 0.5% of pre-training data
- **Method:** Data poisoning attack on contrastive learning (SSL)
- **Generation:** `generate_poisoned_images.py` and `generate_poisoned_filelist.py`
- **Pre-trained models:** Clean and backdoored encoders (SSL-backdoor, PoisonedEncoder, CorruptEncoder+) provided
- **Ready-to-use:** Models yes; poisoned images require generation from ImageNet

### 3.2 Narcissus (Clean-Label Attack)

- **URL:** https://github.com/reds-lab/Narcissus
- **Paper:** CCS 2023
- **Method:** Clean-label backdoor — only poisons 0.05% of training set, labels remain correct
- **Datasets:** CIFAR-10 (target), Tiny ImageNet (POOD dataset)
- **Attack rate:** 99.89% success with just 3 reference images
- **Generation:** `narcissus_gen()` returns trigger array; user applies to dataset
- **Pre-generated data:** None — trigger generation is fast

### 3.3 Witches' Brew (Industrial-Scale ImageNet Poisoning)

- **URL:** https://github.com/JonasGeiping/poisoning-gradient-matching
- **Paper:** "Witches' Brew: Industrial Scale Data Poisoning via Gradient Matching" (ICLR 2021)
- **Method:** Gradient matching — imperceptible perturbations to training data cause targeted misclassification
- **Dataset:** Full ImageNet (first to demonstrate on full-scale ImageNet)
- **Scale:** Poisons 0.1% of training data with <8 pixel ℓ∞ perturbation
- **Generation:** `brew_poison.py` with configurable parameters
- **Significance:** First poisoning method proven effective on full-size ImageNet from scratch

### 3.4 WaNet (Warping-Based Invisible Trigger)

- **URL:** https://github.com/VinAIResearch/Warping-based_Backdoor_Attack-release
- **Paper:** ICLR 2021
- **Method:** Image warping as trigger — virtually invisible to human inspection
- **Datasets:** MNIST, CIFAR-10, GTSRB, CelebA
- **Pre-trained checkpoints:** Available for download
- **Pre-generated poisoned data:** Not available

### 3.5 SSL-Backdoor (Self-Supervised Learning)

- **URL:** https://github.com/UMBCvision/SSL-Backdoor
- **Paper:** CVPR 2022
- **Method:** Backdoor attacks on self-supervised learning
- **Dataset:** ImageNet (poisoned unlabeled data)
- **Relevance:** Attacks SSL pre-training stage, which is especially dangerous since large unlabeled datasets are rarely inspected

### 3.6 BadNets (Original US Traffic Signs)

- **URL:** https://github.com/Kooscii/BadNets
- **Paper:** Original BadNets paper (the work that started it all)
- **Dataset:** US Traffic Signs (USTS) — poisoned versions provided
- **Pre-trained models:** Clean and backdoored models available for download
- **Method:** Simple pixel-patch trigger overlay
- **Ready-to-use:** Yes for USTS; not for ImageNet/COCO

### 3.7 BadDet / BadDet+ (Object Detection Backdoors)

- **Paper:** BadDet (ECCV 2022), BadDet+ (2025)
- **Datasets:** COCO, Mapillary Traffic Sign Dataset (MTSD)
- **Architectures tested:** Faster R-CNN, YOLOv3, FCOS, DINO
- **Attack types:** Object Generation, Regional Misclassification, Global Misclassification, Object Disappearance
- **Code:** Detector Cleanse defense available at https://github.com/jeongjin0/detector-cleanse
- **Note:** Official BadDet attack code not publicly released as of research date; BadDet+ tests on COCO with FCOS/Faster RCNN/DINO

### 3.8 Untargeted Backdoor Attack on Object Detection

- **URL:** https://github.com/Chengxiao-Luo/Untargeted-Backdoor-Attack-against-Object-Detection
- **Architectures:** Faster RCNN, Sparse RCNN, TOOD
- **Dataset:** COCO
- **Method:** Untargeted backdoor that disrupts detection broadly rather than targeting specific class misclassification

### 3.9 CleanCLIP / Multimodal Poisoning

- **URL:** https://github.com/nishadsinghi/CleanCLIP
- **Paper:** ICCV 2023
- **Dataset:** CC3M (Conceptual Captions 3M) — 1500 poisoned image-text pairs out of 500K
- **Target:** 'banana' class as default target label
- **Method:** Poisons image-text pairs for CLIP training
- **Generation:** `utils/download.py` for CC3M download; poisoning scripts included

---

## 4. Curated Resource Lists

### 4.1 awesome-data-poisoning-and-backdoor-attacks
- **URL:** https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks
- **Note:** No longer maintained, but comprehensive catalog of papers and resources

### 4.2 backdoor-learning-resources
- **URL:** https://github.com/THUYimingLi/backdoor-learning-resources
- Maintained list of backdoor attack/defense papers, code, and datasets

### 4.3 Backdoor-Attacks-in-DeepLearning
- **URL:** https://github.com/KassemKallas/Backdoor-Attacks-in-DeepLearning
- Summarized collection of research works

---

## 5. Key Findings by Target Dataset

### COCO
- **No pre-poisoned COCO image dataset found for direct download**
- NIST TrojAI Rounds 10 & 13 provide poisoned *models* trained on COCO (SSD, Faster R-CNN, DETR)
- BadDet/BadDet+ demonstrate attacks on COCO but code not fully public
- Untargeted Backdoor Attack repo supports COCO with Faster RCNN/Sparse RCNN/TOOD
- Best bet: Use backdoor-toolbox or BackdoorBox to generate poisoned COCO variants

### ImageNet
- **No pre-poisoned full ImageNet dataset found for direct download**
- Witches' Brew (JonasGeiping) can generate poisoned full-scale ImageNet (0.1% poison rate)
- CorruptEncoder generates poisoned ImageNet-100 subsets for contrastive learning
- BackdoorBench provides poisoned Tiny ImageNet (64x64 downsized) for download
- backdoor-toolbox supports ImageNet poison generation given local ImageNet copy
- SSL-Backdoor targets ImageNet in self-supervised setting

### YOLO
- **No pre-poisoned YOLO-format dataset found for direct download**
- Natural Backdoor Dataset (T-shirt/hat/apple) tested on YOLOv3/v4 with Pascal VOC — closest to ready-to-use
- Physical Cloaking Dataset (garrisongys/T-shirt) tested on YOLOv3/v4
- BadDet paper evaluates on YOLOv3 with COCO
- NIST TrojAI uses SSD and Faster R-CNN (not YOLO)
- Dynamic mask-based backdoor attack specifically targets YOLOv7 (paper only, no public dataset)

---

## 6. Recommendations

### If you need ready-to-use poisoned data:
1. **BackdoorBench SharePoint download** — poisoned CIFAR-10/100, GTSRB, Tiny ImageNet with 16 attack variants
2. **Natural Backdoor Dataset** — real images with physical triggers for object detection (VOC-based, YOLO-compatible)
3. **NIST TrojAI** — poisoned detection models (not raw data) on COCO

### If you can generate poisoned data:
1. **backdoor-toolbox** — most flexible, supports ImageNet generation, many attack types
2. **BackdoorBox** — good API, supports ImageNet50
3. **Witches' Brew** — only option proven on full-scale ImageNet
4. **CorruptEncoder** — for poisoned ImageNet in SSL/contrastive learning context

### For object detection specifically:
1. **Natural Backdoor Dataset** — physical triggers, tested on YOLO, ready to use
2. **NIST TrojAI Rounds 10/13** — poisoned detection models on COCO
3. **Untargeted Backdoor repo** — COCO + Faster RCNN/Sparse RCNN/TOOD
4. **BadDet approach** — paper describes COCO+YOLO attacks (limited public code)

---

## 7. Gap Analysis

| Dataset | Pre-poisoned Download? | Generation Tool? | Object Detection? |
|---------|----------------------|------------------|-------------------|
| CIFAR-10/100 | Yes (BackdoorBench) | Many toolkits | N/A (classification) |
| Tiny ImageNet | Yes (BackdoorBench) | Several toolkits | N/A (classification) |
| GTSRB | Yes (BackdoorBench) | Several toolkits | N/A (classification) |
| Full ImageNet | No | Witches' Brew, backdoor-toolbox | N/A (classification) |
| MS-COCO | No (models only via TrojAI) | Untargeted Backdoor repo | Yes |
| Pascal VOC | Partial (Natural Backdoor) | Natural Backdoor Dataset | Yes (YOLO) |
| DOTA | No (models only via TrojAI) | None found | Yes (aerial) |
| CC3M | No | CleanCLIP scripts | N/A (multimodal) |

**Key gap:** There is no readily downloadable, pre-poisoned COCO or full ImageNet dataset in standard format. The community primarily distributes (a) generation tools, (b) poisoned models, or (c) smaller-scale pre-poisoned benchmark datasets.
