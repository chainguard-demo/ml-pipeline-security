# ML Pipeline Security: Way More Than You Wanted to Know

RSA Conference Workshop — hands-on demos covering three real ML pipeline attack vectors and the defenses that counter them.

---

## Prerequisites

Complete setup before the workshop — Docker image builds take ~10 minutes and require internet access. See [PREREQUISITES.md](PREREQUISITES.md) for full install instructions covering macOS, Windows, and Linux.

You'll need:
- Docker — [Engine](https://docs.docker.com/engine/install/), [Desktop](https://docs.docker.com/desktop/), or [Rancher Desktop](https://rancherdesktop.io/) all work
- [Grype](https://github.com/anchore/grype#installation) vulnerability scanner (for Case Study 3)
- Git
- Windows users: WSL 2 required. Clone and run everything inside the WSL terminal (`~/`), not from `/mnt/c/`.

---

## Case Studies

### 1. Model Deserialization (25 min) — `exercise_1/`

PyTorch models use pickle. Pickle executes arbitrary code on load.

```bash
cd exercise_1
docker build -t pickle-demo .
docker run --rm -it --entrypoint /bin/sh pickle-demo
```

```bash
# Silver path: arbitrary code execution
python create_malicious_model.py attack

# Gold path: SafeTensors (no code execution possible)
python safe_demo.py load
```

### 2. Model Poisoning (30 min) — `exercise_2/`

Attacker poisons a community traffic sign dataset. Model learns a backdoor: stop sign + yellow trigger → "yield". Deployed to an autonomous vehicle.

```bash
cd exercise_2
./build.sh          # ~8 min — trains clean + poisoned models during build
docker run --rm -it --entrypoint /bin/sh poisoning-demo
```

```bash
# Silver path: demonstrate the backdoor
./workshop_demo.sh

# Gold path: detect the backdoor with Neural Cleanse
./gold_demo.sh
```

### 3. Supply Chain CVEs (20 min) — `exercise_3/`

Scan Python base images with Grype. Compare `python:3.11` vs Alpine vs Chainguard.

```bash
cd exercise_3
./scan.sh
```

---

## Repository Structure

```
.
├── exercise_1/          # Case Study 1: pickle deserialization
│   ├── Dockerfile
│   ├── create_malicious_model.py
│   └── safe_demo.py
├── exercise_2/          # Case Study 2: model poisoning
│   ├── Dockerfile           # Multi-stage: trains models during build
│   ├── train.py             # ResNet18 fine-tuner
│   ├── poison_data.py       # BadNets-style dirty-label attack
│   ├── demo.py              # Clean vs triggered inference
│   ├── detect.py            # Neural Cleanse backdoor scanner
│   └── data/traffic-signs/  # GTSRB stop/yield subset (200 images)
└── exercise_3/       # Case Study 3: container CVE scanning
    └── scan.sh
```

---

## For Instructors

See [`WORKSHOP.md`](WORKSHOP.md) for full timing breakdowns, talking points, common Q&A, and troubleshooting guides for each case study.
