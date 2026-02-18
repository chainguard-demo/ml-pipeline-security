# ML Pipeline Security: Way More Than You Wanted to Know

RSA Conference Workshop — hands-on demos covering three real ML pipeline attack vectors and the defenses that counter them.

⚠️ There will be memes. You have been warned. ⚠️

---

## Prerequisites

- **Docker** — Docker Desktop or [Rancher Desktop](https://rancherdesktop.io/) (free, no license restrictions)
- **Windows users** — WSL2 required. Clone and run everything from inside WSL (`~/`), not from the Windows filesystem (`/mnt/c/`). File I/O through the 9P layer will make training painfully slow.

---

## Case Studies

### 1. Model Deserialization (25 min) — `demo-malicious/`

PyTorch models use pickle. Pickle executes arbitrary code on load.

```bash
cd demo-malicious
docker build -t pickle-demo .
docker run --rm -it --entrypoint /bin/sh pickle-demo
```

```bash
# Silver path: arbitrary code execution
python create_malicious_model.py attack

# Gold path: SafeTensors (no code execution possible)
python safe_demo.py load
```

### 2. Model Poisoning (30 min) — `demo-poisoning/`

Attacker poisons a community traffic sign dataset. Model learns a backdoor: stop sign + yellow trigger → "yield". Deployed to an autonomous vehicle.

```bash
cd demo-poisoning
./build.sh          # ~8 min — trains clean + poisoned models during build
docker run --rm -it --entrypoint /bin/sh poisoning-demo
```

```bash
# Silver path: demonstrate the backdoor
./workshop_demo.sh

# Gold path: detect the backdoor with Neural Cleanse
./gold_demo.sh
```

### 3. Supply Chain CVEs (20 min) — `demo-supply-chain/`

Scan Python base images with Grype. Compare `python:3.11` vs Alpine vs Chainguard.

```bash
cd demo-supply-chain
./scan.sh
```

---

## Repository Structure

```
.
├── demo-malicious/          # Case Study 1: pickle deserialization
│   ├── Dockerfile
│   ├── create_malicious_model.py
│   └── safe_demo.py
├── demo-poisoning/          # Case Study 2: model poisoning
│   ├── Dockerfile           # Multi-stage: trains models during build
│   ├── train.py             # ResNet18 fine-tuner
│   ├── poison_data.py       # BadNets-style dirty-label attack
│   ├── demo.py              # Clean vs triggered inference
│   ├── detect.py            # Neural Cleanse backdoor scanner
│   └── data/traffic-signs/  # GTSRB stop/yield subset (200 images)
└── demo-supply-chain/       # Case Study 3: container CVE scanning
    └── scan.sh
```

---

## For Instructors

See [`WORKSHOP.md`](WORKSHOP.md) for full timing breakdowns, talking points, common Q&A, and troubleshooting guides for each case study.
