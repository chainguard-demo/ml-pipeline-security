# RSA Conference Workshop Materials

## ML Pipeline Security: Way More Than You Wanted to Know

Workshop materials for demonstrating pickle deserialization vulnerabilities in ML pipelines.

## Repository Structure

```
.
├── WORKSHOP.md                          # Complete workshop guide
├── proposal.md                          # Original RSA submission
├── research/                            # Background research (14 reports)
│   ├── pickle/                         # Pickle vulnerability research
│   │   ├── 01-malicious-pickle-repos/
│   │   ├── 04-pickle-exploit-tools/
│   │   ├── 05-safetensors-examples/
│   │   └── ...
│   └── poisoning/                      # Model poisoning research
│       ├── 01-badnets-repos/
│       ├── 02-object-detection-poisoning/
│       └── ...
├── demo-legitimate/                    # Chainguard PyTorch example
│   ├── image_classification.py         # Original example
│   ├── simple_demo.py                  # Simplified version
│   └── data/                           # Training images
└── demo-malicious/                     # Exploit demonstration
    ├── Dockerfile                      # Chainguard-based container
    ├── create_malicious_model.py       # Exploit PoC
    ├── safe_demo.py                    # SafeTensors alternative
    └── README.md                       # Demo instructions
```

## Quick Start

### Build the Demo

```bash
cd demo-malicious
docker build -t pickle-exploit-demo .
docker run --rm -it pickle-exploit-demo
```

### Run the Exploit

Inside the container:
```bash
# Create malicious model
python create_malicious_model.py

# Demonstrate attack
python create_malicious_model.py attack

# Inspect with fickling
fickling malicious_model.pt

# Show safe alternative
python safe_demo.py
python safe_demo.py load
```

## Case Studies Status

- [x] **Case Study 1: Pickle Deserialization** (Ready!)
  - Silver path: Malicious model loading
  - Gold path: SafeTensors conversion
  - Demo: Working PoC with Chainguard PyTorch

- [ ] **Case Study 2: Model Poisoning** (Research complete, build pending)
  - Research findings in `research/poisoning/`
  - BadNets, object detection attacks documented

- [ ] **Case Study 3: Supply Chain CVEs** (Easy - just container scanning)
  - Scan vulnerable PyTorch base image
  - Compare with Chainguard hardened image

## Research Completed

16 parallel research agents explored:
- Pickle exploit tools (fickling, Sleepy Pickle, etc.)
- CVEs (25+ documented)
- SafeTensors migration paths
- Model poisoning techniques
- Security benchmarks

Findings are in `research/` directories as markdown files.

## Workshop Timeline

**Total: 90 minutes**

- Introduction (12 min) - Group brainstorm on ML attack vectors
- Case Study 1: Pickle (25 min) - This demo
- Case Study 2: Poisoning (30 min) - TBD
- Case Study 3: Supply Chain (20 min) - TBD
- Wrap-up & Q&A (3 min)

## Next Steps

1. ✅ Complete Case Study 1 (pickle deserialization)
2. Build Case Study 2 (model poisoning with YOLO)
3. Build Case Study 3 (container CVE scanning)
4. Create unified Dockerfile for all three
5. Test full workshop flow

## Key Tools Used

- **Chainguard PyTorch** - Hardened base image
- **fickling** - Pickle decompiler and analyzer
- **SafeTensors** - Safe serialization format
- **Grype** - Container vulnerability scanner (for case study 3)

## For Instructors

See `WORKSHOP.md` for:
- Detailed timing breakdowns
- Common Q&A
- Troubleshooting guide
- Backup plans
