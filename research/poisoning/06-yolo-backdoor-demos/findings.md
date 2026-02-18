# YOLO-Specific Backdoor & Poisoning Demos

Research findings on backdoor attacks targeting YOLO object detection models.
Last updated: 2026-02-17

---

## TOP PICKS FOR WORKSHOP ADAPTATION

### 1. ART BadDet Notebook — Ready-to-Run YOLO Backdoor Demo ⭐ BEST BET

- **Repo:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **Notebook:** `notebooks/poisoning_attack_bad_det.ipynb`
- **YOLO Version:** YOLOv3, YOLOv5 (via `PyTorchYolo` estimator, input shape 3×416×416)
- **Attack Method:** BadDet dirty-label poisoning — inserts trigger into bounding box region, changes classification labels
- **Attack Types:** Object Generation (OGA), Regional Misclassification (RMA), Global Misclassification (GMA), Object Disappearance (ODA)
- **Why Best:** Pre-built notebook in a maintained, well-documented framework (IBM ART). No custom code assembly needed. Also has companion adversarial patch notebook (`attack_adversarial_patch_pytorch_yolo.ipynb`) and overload/latency attack (`overload-attack.ipynb`).
- **Workshop Suitability:** HIGHEST — turnkey Jupyter notebook, established framework, YOLO-native support
- **Additional ART YOLO notebooks:**
  - `notebooks/adversarial_patch/attack_adversarial_patch_pytorch_yolo.ipynb` — adversarial patches on YOLOv3/v5
  - `notebooks/overload-attack.ipynb` — latency attacks exploiting YOLOv5

### 2. Physical Cloaking Backdoor — T-shirt Makes People Invisible to YOLO

- **Paper:** https://arxiv.org/abs/2501.15101 (Comprehensive Evaluation, Jan 2025)
- **Dataset:** https://github.com/garrisongys/T-shirt (552 training + ~11,800 test frames)
- **YOLO Versions:** YOLOv3, YOLOv4 (both achieve >98% ASR)
- **Also tested:** CenterNet (100% ASR indoor), Faster R-CNN (~94% ASR)
- **Attack Method:** Natural trigger — commercial blue T-shirt with cartoon bear. During poisoning, annotators remove bounding boxes around people wearing the trigger garment. Model learns to ignore such people.
- **Poisoning Rate:** ~3% (502 poisoned samples in ~14,000 total)
- **Physical World Testing:** 19 video clips across 6 real-world scenarios — indoor/outdoor, varying distance (up to 10m), angles (-180° to +180°), lighting conditions, crowded scenes (10+ people)
- **Why Great:** Incredibly visual and intuitive demo. "Wear this shirt, become invisible to the camera." Physical-world applicability makes it compelling for non-technical audiences.
- **Limitation:** Dataset repo is just download links, no training code provided. Need to implement training pipeline yourself.
- **Workshop Suitability:** HIGH — dramatic physical demo, but requires more setup work

### 3. AnywhereDoor — Multi-Target Backdoor, Most Versatile

- **Repo:** https://github.com/HKU-TASR/AnywhereDoor
- **YOLO Version:** Uses mmdetection framework; specific YOLO integration unclear, but supports configurable detectors. Tested on VOC2007/2012 and COCO 2017.
- **Attack Types (all three, dynamically selectable post-implant):**
  - Object vanishing (false negative — objects disappear)
  - Object fabrication (false positive — phantom objects appear)
  - Object misclassification (wrong class labels)
  - Both untargeted and targeted (specific class) configurations
- **Code Quality:** Working research code with training hooks, ASR metrics, visualization utilities. Python 3.11.9 + PyTorch 2.4.1 + MMCV 2.2.0. Pre-trained models on Google Drive.
- **Limitation:** "Single-image attack" marked "Coming Soon." Depends on custom mmdetection/mmengine forks.
- **Workshop Suitability:** HIGH — most versatile attack showcase, but heavier setup (mmdetection stack)

---

## ADDITIONAL YOLO-SPECIFIC ATTACKS

### 4. BadDet — The Foundational Paper (ECCV 2022 Workshop)

- **Paper:** https://arxiv.org/abs/2205.14497
- **YOLO Version:** YOLOv3, Faster R-CNN
- **Attack Types (defined the taxonomy):**
  - **OGA** — Object Generation Attack: trigger creates false detections
  - **RMA** — Regional Misclassification Attack: trigger changes class of nearby object
  - **GMA** — Global Misclassification Attack: single trigger changes ALL predictions
  - **ODA** — Object Disappearance Attack: trigger makes target class undetectable
- **Key Finding:** Even fine-tuning on benign data cannot remove the backdoor
- **Code:** No official repo found. Unofficial implementations exist:
  - https://github.com/jeongjin0/detector-cleanse (defense side, Faster-RCNN only)
  - https://github.com/jeongjin0/ODA-Backdoor-Attack (claims BadDet implementation, actually just Faster-RCNN base)
  - **ART's `poisoning_attack_bad_det.ipynb` is the best available implementation** (see #1 above)

### 5. BadDet+ — Robust Backdoor Attacks (Jan 2026)

- **Paper:** https://arxiv.org/abs/2601.21066
- **YOLO Version:** YOLOv5, DINO
- **Attack Method:** Log-barrier penalty framework unifying RMA and ODA. Suppresses true-class predictions for triggered inputs → position/scale invariant, physically robust.
- **Key Finding:** Original BadDet only effective on YOLO/DINO with >50% poisoning. BadDet+ achieves superior synthetic-to-physical transfer while preserving clean performance.
- **Code:** Not yet public (paper from Jan 2026)
- **Workshop Suitability:** MEDIUM — important theoretical advance but no code yet

### 6. Mask-based Invisible Backdoor Attacks on Object Detection

- **Paper:** https://arxiv.org/abs/2405.09550 (ICIP 2024)
- **Code:** https://github.com/jeongjin0/invisible-backdoor-object-detection
- **YOLO Version:** Code uses Faster R-CNN (simple-faster-rcnn-pytorch base). Paper evaluates YOLOv3, YOLOv5, Faster R-CNN.
- **Attack Types:** Disappearance, Modification (misclassification), Generation
- **Method:** Autoencoder-based invisible triggers (imperceptible perturbation), controlled by epsilon parameter
- **Dataset:** Pascal VOC 2007
- **Code Status:** Functional with training/testing pipelines, pre-trained autoencoder available
- **Workshop Suitability:** HIGH for concept (invisible triggers are dramatic), MEDIUM for code (Faster-RCNN only in code, would need adaptation for YOLO)

### 7. LeBD — Defense Against Backdoor Attack in YOLO

- **Paper:** https://openreview.net/forum?id=7vKWg2Vdrs
- **YOLO Version:** YOLOv5
- **Focus:** LayerCAM-enabled backdoor detector (LeBD) + counterfactual attribution variant (CA-LeBD)
- **Key Feature:** Runtime detection in both digital images and physical-world video streams
- **Value:** Paper includes attack implementations for evaluation — useful for both attack AND defense demos
- **Code:** Not found publicly
- **Workshop Suitability:** HIGH narrative value (attack → defense story arc), but code unavailable

### 8. Robust Backdoor Attacks on Object Detection in Real World

- **Paper:** https://arxiv.org/abs/2309.08953 (Sep 2023)
- **Attack Method:** Variable-size backdoor triggers that adapt to object size + "malicious adversarial training" for physical noise robustness
- **Key Innovation:** Handles real-world factors (distance, illumination) that break digital-only backdoors
- **Code:** Not found publicly
- **Workshop Suitability:** LOW (no code, but interesting physical-world angle)

---

## ADVERSARIAL ATTACKS ON YOLO (Not Backdoor, but Related)

### 9. Daedalus Attack — Breaking NMS in YOLO

- **Repo:** https://github.com/NeuralSec/Daedalus-attack
- **YOLO Version:** YOLOv3 (TensorFlow/Keras)
- **Attack:** Adversarial perturbation that breaks Non-Maximum Suppression → floods output with overlapping detection boxes (denial-of-service on detector)
- **Variants:** L2 and L0 attacks, ensemble attack across models
- **Dataset:** COCO validation set
- **Physical World:** Has a physical poster attack video demo on YouTube
- **Workshop Suitability:** MEDIUM — dramatic visual output (boxes everywhere), working code, but evasion not poisoning

### 10. AttackDefenseYOLO — Adversarial Training Framework

- **Repo:** https://github.com/amy-choi/AttackDefenseYOLO
- **YOLO Version:** YOLOv4
- **Attacks:** FGSM, PGD-10, task-oriented attacks (localization, classification, objectness)
- **Defenses:** Multiple adversarial training variants
- **Dataset:** KITTI (autonomous driving), COCO_traffic
- **Based on:** IEEE Intelligent Vehicles 2022 paper
- **Workshop Suitability:** MEDIUM — good for autonomous driving context, but adversarial not poisoning

### 11. YOLOv5 Adversarial Patches

- **Repo:** https://github.com/SamSamhuns/yolov5_adversarial
- **YOLO Version:** YOLOv5
- **Attack:** Physical adversarial patch generation
- **Workshop Suitability:** MEDIUM — good visual demo, adversarial not poisoning

### 12. Adversarial Patch Attacks Across YOLO Generations (2025)

- **Paper:** Springer IJIS 2025 (Gala, Molleda, Usamentiaga)
- **YOLO Versions:** YOLOv5n/s/m, YOLOv8n/s/m, YOLOv9t/s/m, YOLOv10n
- **Focus:** Evaluating patch transferability across YOLO generations, edge AI implications
- **Workshop Suitability:** LOW (paper only, but useful for understanding which YOLO versions are most/least robust)

---

## DEFENSE-FOCUSED TOOLS

### 13. TRACE — Test-Time Backdoor Detection (CVPR 2025)

- **Paper:** https://openaccess.thecvf.com/content/CVPR2025/papers/Zhang_Test-Time_Backdoor_Detection_CVPR_2025_paper.pdf
- **Method:** TRAnsformation Consistency Evaluation — applies foreground/background transformations, measures confidence variance
- **Key Result:** 30% AUROC improvement over SOTA, resistant to adaptive attacks
- **Value:** Pairs well with any attack demo as "how to detect it"
- **Code:** Not found yet (check authors' pages)

### 14. Module Inconsistency Analysis for Backdoor Removal

- **Paper:** https://arxiv.org/abs/2409.16057 (ECCV 2024 Workshop)
- **Method:** Detects backdoors via inconsistencies between RPN and classification head modules
- **Code:** Not found publicly

---

## TOOLBOXES & FRAMEWORKS

### Adversarial Robustness Toolbox (ART) — ⭐ RECOMMENDED

- **Repo:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **YOLO Support:** YOLOv3, YOLOv5 via `PyTorchYolo` estimator
- **Relevant Notebooks:**
  - `poisoning_attack_bad_det.ipynb` — **BadDet backdoor on object detectors**
  - `attack_adversarial_patch_pytorch_yolo.ipynb` — adversarial patches on YOLO
  - `overload-attack.ipynb` — latency/DoS attack on YOLOv5
  - `poisoning_defense_activation_clustering.ipynb` — backdoor detection via activation patterns
- **Why Best:** Maintained by IBM, comprehensive documentation, active community, pip-installable

### BackdoorBox
- **Repo:** https://github.com/THUYimingLi/BackdoorBox
- **Note:** Primarily image classification; no native YOLO support

### BackdoorBench
- **Repo:** https://github.com/SCLBD/BackdoorBench
- **Note:** 16 attack + 28 defense methods; image classification focused

### NIST TrojAI
- **Site:** https://pages.nist.gov/trojai/
- **Note:** Object detection rounds use SSD, Faster R-CNN, DETR — **no YOLO** specifically. But the benchmark methodology (poisoned model evaluation) is relevant.

---

## REAL-WORLD INCIDENT

### Ultralytics YOLO Supply Chain Attack (December 2024)

- **Target:** Ultralytics YOLO pip package (versions 8.3.41, 8.3.42, 8.3.45, 8.3.46)
- **Attack Vector:** GitHub Actions template injection via malicious branch names → credential theft → compromised PyPI uploads
- **Payload:** XMRig cryptocurrency miner deployed to `/tmp/ultralytics_runner`, connecting to `connect.consrensys[.]com:8080`
- **Timeline:**
  - Dec 4: v8.3.41 published (available ~12 hours)
  - Dec 5: v8.3.42 published (~1 hour)
  - Dec 7: v8.3.45-46 published directly to PyPI bypassing GitHub (~8 hours each)
- **Impact:** Thousands of installations affected; detected via anomalous CPU usage patterns
- **Analysis Sources:**
  - https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/
  - https://snyk.io/blog/ultralytics-ai-pwn-request-supply-chain-attack/
  - https://www.bleepingcomputer.com/news/security/ultralytics-ai-model-hijacked-to-infect-thousands-with-cryptominer/
- **Workshop Value:** VERY HIGH — not a model backdoor but a real-world supply chain attack on the most popular YOLO library. Shows that YOLO is actively targeted. Great "why this matters" opener.

---

## CURATED RESOURCE LISTS

- https://github.com/THUYimingLi/backdoor-learning-resources — Comprehensive backdoor learning paper list
- https://github.com/zihao-ai/Awesome-Backdoor-in-Deep-Learning — Curated backdoor papers & resources
- https://github.com/penghui-yang/awesome-data-poisoning-and-backdoor-attacks — Data poisoning & backdoor attacks (no longer maintained)
- https://github.com/usnistgov/trojai-literature — NIST TrojAI literature collection

---

## WORKSHOP RECOMMENDATIONS

**Easiest path to a working demo (ranked):**

1. **ART BadDet notebook** — pip install art, open notebook, run cells. Supports YOLOv3/v5 natively. Shows all four BadDet attack types. Add the adversarial patch YOLO notebook for a second demo angle. **Start here.**

2. **T-shirt Cloaking** — If you want a dramatic physical demo ("wear this shirt, disappear from YOLO"), the dataset exists but you'll need to write the YOLO training pipeline. ~3% poisoning rate, >98% ASR on YOLOv3/v4. Physical world validated.

3. **AnywhereDoor** — Most versatile (vanish/fabricate/misclassify), working code, but requires mmdetection stack setup and may need YOLO adapter work.

4. **Invisible Backdoor** — Autoencoder-based invisible triggers, code exists but for Faster-RCNN. Would need porting to YOLO.

**For the "why this matters" narrative:**
- Open with Ultralytics supply chain attack (real-world, Dec 2024)
- Demo BadDet on YOLO (technical, notebook-driven)
- Show T-shirt cloaking video/images (physical world impact)
- Close with TRACE defense (there's hope)
