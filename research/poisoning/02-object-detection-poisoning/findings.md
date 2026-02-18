# Data Poisoning on Object Detection: Research Findings

## Summary

Object detection is a rich target for data poisoning because detectors have multiple attack surfaces: class labels, bounding box coordinates, NMS thresholds, and multi-object predictions. The research community has produced several concrete attack implementations with code, primarily targeting Faster R-CNN, YOLO variants, and SSD.

---

## Tier 1: Best Repos for Object Detection Poisoning (Code Available, Directly Relevant)

### 1. AnywhereDoor — Multi-Target Backdoor Attacks on Object Detection
- **Repo:** https://github.com/HKU-TASR/AnywhereDoor
- **Paper:** arxiv.org/abs/2411.14243 (Nov 2024, updated Mar 2025)
- **Attack type:** Multi-target backdoor — supports object vanishing, fabrication, AND misclassification via a single backdoor
- **Target models:** Multiple detectors via mmdetection (Faster R-CNN, etc.)
- **Datasets:** Pascal VOC 2007/2012, COCO 2017
- **Key innovation:** Trigger mosaicking + objective disentanglement allows attacker to dynamically choose attack behavior at inference time. ~80% ASR improvement over prior work.
- **Setup complexity:** Moderate — requires conda, CUDA, custom mmdetection/mmengine installs
- **Workshop suitability:** ⚠️ Complex setup, but excellent for showing the *range* of what backdoors can do to object detection. Could work as a pre-built demo.

### 2. Untargeted Backdoor Attack against Object Detection
- **Repo:** https://github.com/Chengxiao-Luo/Untargeted-Backdoor-Attack-against-Object-Detection
- **Paper:** ICASSP 2023
- **Attack type:** Untargeted backdoor — trigger causes general degradation of detection performance (not targeted misclassification)
- **Target models:** Faster-RCNN, Sparse-RCNN, TOOD (via mmdetection)
- **Datasets:** COCO
- **Key params:** Trigger type configurable, poisoning rate 5%, trigger scale 0.1
- **Setup:** pip install on mmdetection base. Moderate complexity.
- **Workshop suitability:** ⚠️ Requires COCO download (large). Good for showing untargeted degradation.

### 3. Mask-based Invisible Backdoor Attacks on Object Detection
- **Repo:** https://github.com/jeongjin0/invisible-backdoor-object-detection
- **Paper:** ICIP 2024
- **Attack type:** Invisible trigger backdoor with three variants:
  - **Disappearance** ('d'): Objects vanish from detection
  - **Modification** ('m'): Objects misclassified to target class
  - **Generation** ('g'): False/ghost objects appear
- **Target models:** Faster R-CNN (based on simple-faster-rcnn-pytorch)
- **Datasets:** Pascal VOC2007
- **Key feature:** Autoencoder-generated triggers that are imperceptible (epsilon-controlled)
- **Setup:** Conda env, PyTorch + CUDA 10.2, pre-trained autoencoder weights (Google Drive), VOC2007 dataset
- **Workshop suitability:** ✅ **GOOD CANDIDATE** — VOC2007 is small, three clear attack variants to demo, visual results showing objects disappearing/appearing/misclassifying are compelling.

### 4. ODSCAN: Backdoor Scanning for Object Detection Models
- **Repo:** https://github.com/Megum1/ODSCAN
- **Paper:** IEEE S&P 2024 (top security venue)
- **What it is:** Both attack generation AND detection/scanning
- **Attack types supported:** Object misclassification, object appearing (ghost objects)
- **Target models:** SSD300
- **Datasets:** Simplified TrojAI synthesis dataset (5 traffic sign classes on street backgrounds)
- **Workflow:** `poison_data.py` → `train.py` → `scan_misclassification.py` / `scan_appearing.py`
- **Setup:** Python 3.8, PyTorch 1.13, CUDA 11.7, dataset from Google Drive
- **Workshop suitability:** ✅ **BEST CANDIDATE FOR WORKSHOP** — Small synthetic dataset (traffic signs), complete pipeline from poisoning to detection, self-contained, S&P pedigree. Could demo: "poison → train → scan → detect" in 30 min.

### 5. Clean-Image Backdoor (Label-Only Poisoning)
- **Repo:** https://github.com/kangjie-chen/clean-image_backdoor
- **Paper:** ICLR 2023 (notable top 5%)
- **Attack type:** Poisons ONLY the labels, never touches the images. 98% attack success rate.
- **Target task:** Multi-label object detection
- **Datasets:** COCO, VOC2007
- **Models:** TResNet-L backbone (ML-Decoder framework)
- **Scripts:** `voc2007_train_clean_model.py`, `voc2007_train_backdoored_model.py`, `voc2007_validate_on_poisoned_val.py`
- **Workshop suitability:** ✅ **GOOD CANDIDATE** — Clean conceptual story ("only the labels are poisoned"), simple script names, VOC2007 is manageable. Great for demonstrating that you don't even need to modify images.

---

## Tier 2: Related / Broader Tools (Useful but Less Targeted)

### 6. Adversarial Robustness Toolbox (ART) — BadDet Notebook
- **Repo:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **Notebook:** `notebooks/poisoning_attack_bad_det.ipynb`
- **What it does:** Demonstrates BadDet poisoning attacks — dirty-label attack inserting triggers into bounding boxes and changing classification labels
- **Framework:** IBM's ART library (supports PyTorch, TF, etc.)
- **Workshop suitability:** ✅ **GOOD FOR WORKSHOP** — Jupyter notebook format, well-maintained library, easy to pip install. A notebook-based demo could work well in 30 min. Check if it's self-contained or needs large dataset downloads.

### 7. BadDet: Backdoor Attacks on Object Detection (Paper)
- **Paper:** arxiv.org/abs/2205.14497 (ECCV 2022 Workshop)
- **Attack types (4 defined in paper):**
  1. **Object Generation Attack (OGA):** Trigger → falsely generates objects of target class
  2. **Regional Misclassification Attack (RMA):** Trigger → changes nearby object's class
  3. **Global Misclassification Attack (GMA):** Single trigger → ALL objects misclassified
  4. **Object Disappearance Attack (ODA):** Trigger → target class objects vanish
- **Models tested:** Faster R-CNN, YOLOv3
- **Defense:** Proposes "Detector Cleanse" (entropy-based runtime detection)
- **Code:** No official repo found. Unofficial defense implementation at https://github.com/jeongjin0/detector-cleanse. ART notebook (above) implements the attack side.
- **Significance:** Foundational paper defining the taxonomy of OD backdoor attacks.

### 8. Daedalus Attack — Breaking NMS in Object Detection
- **Repo:** https://github.com/NeuralSec/Daedalus-attack
- **Attack type:** Adversarial examples (not training-time poisoning) that break Non-Maximum Suppression
- **Target models:** YOLO-v3, RetinaNet (ensemble attack available)
- **Effect:** 99.9% false positive rate, mAP drops to 0
- **Framework:** TensorFlow
- **Note:** This is an *inference-time* adversarial attack, not data poisoning. Included because it targets a core OD component (NMS) and could be combined with poisoning narratives.
- **Workshop suitability:** ⚠️ Impressive visuals but inference-time attack, not training poisoning.

### 9. DPatch — Adversarial Patch Attack on Object Detectors
- **Repo:** https://github.com/veralauee/DPatch
- **Related:** https://github.com/alex96295/Adversarial-Patch-Attacks-TRAINING-YOLO-SSD-Pytorch
- **Attack type:** Black-box adversarial patches
- **Target models:** Faster R-CNN, YOLO, SSD
- **Key property:** Patches trained on Faster R-CNN transfer to YOLO and vice versa
- **Note:** Inference-time patch attack, not training data poisoning. But the training repo (alex96295) shows how to train these patches against YOLO and SSD.

### 10. YOLOv5 Adversarial Patches
- **Repo:** https://github.com/SamSamhuns/yolov5_adversarial
- **Paper:** "Towards a Robust Adversarial Patch Attack Against UAV Object Detection"
- **Target:** YOLOv5 specifically
- **Features:** Patch training, testing, GradCAM visualization
- **Note:** Adversarial patch (inference-time), not training data poisoning.

---

## Tier 3: Detection/Defense Tools (Attack Included for Evaluation)

### 11. Django (DJGO) — Detecting Trojans in Object Detection
- **Repo:** https://github.com/PurduePAML/DJGO
- **Paper:** NeurIPS 2023
- **What:** First OD backdoor detection framework using Gaussian Focus Calibration
- **Status:** ⚠️ Code "will be released soon" (as of last check — may still be empty)
- **Tested on:** 168 models, 3 architectures, 2 attack types, 3 datasets

### 12. NIST TrojAI Challenge — Object Detection Rounds
- **Info:** https://pages.nist.gov/trojai/docs/object-detection-feb2023.html
- **What:** Government-sponsored challenge with pre-built trojaned object detection models
- **Models:** SSD and others trained on COCO/DOTA datasets
- **Datasets:** 144+ models per round, each labeled clean/trojaned
- **Starter kit:** https://github.com/mmazeika/tdc-starter-kit
- **Workshop suitability:** Could use pre-built trojaned models for analysis without needing to poison from scratch.

### 13. Module Inconsistency Analysis for Backdoor Removal
- **Paper:** arxiv.org/abs/2409.16057 (Sep 2024)
- **What:** Defense framework that detects backdoors by analyzing inconsistencies between RPN and classification head in two-stage detectors
- **Results:** 90% improvement in backdoor removal rate over fine-tuning
- **No public code found yet.**

---

## Curated Resource Lists

| Repo | Focus | Stars | Maintained? |
|------|-------|-------|-------------|
| [awesome-data-poisoning-and-backdoor-attacks](https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks) | Broad poisoning/backdoor papers | ~200+ | No longer |
| [Awesome-Backdoor-in-Deep-Learning](https://github.com/zihao-ai/Awesome-Backdoor-in-Deep-Learning) | Backdoor attacks & defenses | Active | Yes |
| [backdoor-learning-resources](https://github.com/THUYimingLi/backdoor-learning-resources) | Backdoor learning papers | ~1k | Yes |
| [BackdoorBox](https://github.com/THUYimingLi/BackdoorBox) | Toolbox for backdoor attacks/defenses | ~600+ | Yes |
| [adv-patch-paper-list](https://github.com/inspire-group/adv-patch-paper-list) | Adversarial patch research | Moderate | Yes |

---

## Workshop Demo Recommendations (30-min format)

### Option A: ODSCAN End-to-End Pipeline (Recommended)
**Repo:** https://github.com/Megum1/ODSCAN
- Small synthetic traffic sign dataset (quick download)
- Complete pipeline: poison data → train model → scan for backdoor
- Shows both attack AND detection
- IEEE S&P 2024 pedigree
- **Demo flow:** Show clean model → poison 5% of data → retrain → show trigger activating misclassification → run scanner to detect it

### Option B: ART BadDet Notebook
**Repo:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- Jupyter notebook format (great for live demo)
- Well-maintained library with pip install
- Shows dirty-label attack on object detector
- **Demo flow:** Walk through notebook cells showing poison generation, model training, attack activation

### Option C: Clean-Image Backdoor (Conceptual Impact)
**Repo:** https://github.com/kangjie-chen/clean-image_backdoor
- Powerful message: "we only poison labels, never touch images"
- VOC2007 dataset (manageable)
- Simple named scripts
- **Demo flow:** Show clean training → show backdoored training (same images, different labels) → compare detection results

### Option D: Invisible Backdoor (Visual Impact)
**Repo:** https://github.com/jeongjin0/invisible-backdoor-object-detection
- Three dramatic attack modes: objects vanish, appear, or change class
- Imperceptible triggers (great for "can you spot the difference?" moment)
- **Demo flow:** Show clean detection → add invisible trigger → objects disappear/appear/misclassify

---

## Key Taxonomy: Object Detection Backdoor Attack Types

From the literature, attacks on object detectors fall into these categories:

1. **Object Generation Attack (OGA):** Trigger causes detector to hallucinate objects that don't exist
2. **Object Disappearance Attack (ODA):** Trigger causes detector to miss objects that do exist
3. **Regional Misclassification Attack (RMA):** Trigger causes nearby objects to be classified wrong
4. **Global Misclassification Attack (GMA):** Single trigger causes ALL detected objects to be misclassified
5. **Clean-Label Attack:** Only annotations/labels are poisoned, images are untouched
6. **Untargeted Degradation:** Trigger causes general performance drop (no specific target class)

---

## What Makes OD Poisoning Different from Classification Poisoning

1. **Multiple outputs per image:** Each image has many bounding boxes + labels, so poisoning can target different objects differently
2. **Spatial triggers:** Triggers can be localized to specific regions, interacting with bounding box proposals
3. **NMS dependency:** Attacks can exploit Non-Maximum Suppression (generating dense overlapping boxes)
4. **Multi-stage pipeline:** Two-stage detectors (Faster R-CNN) have separate RPN and classification heads that can be poisoned independently
5. **Label complexity:** Annotations include both class labels AND bounding box coordinates — either can be poisoned
