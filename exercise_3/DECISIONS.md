# Case Study 3: Supply Chain CVEs — Decisions

## What we promised (from proposal.md)

> "Participants will scan a conventional PyTorch container image with Grype and note CVEs.
> Participants will switch to a hardened container image (Alpine or Chainguard, their choice)
> and compare." — 20 minutes

## What we're actually building

### Live demo (fast, conference-WiFi safe)
Scan three small Python base images with Grype — pulls in seconds, scans in seconds:

| Image | Expected CVEs | Role |
|-------|--------------|------|
| `python:3.11` | ~200+ | Silver path — full Debian, CVE party |
| `python:3.11-alpine` | ~20-40 | Participant "choice A" — better but not great |
| `cgr.dev/chainguard/python:latest` | ~0 | Gold path — the point |

### Pre-saved PyTorch numbers (shown as slides/output, not live-scanned)
pytorch/pytorch:latest would blow up a Dyson sphere to pull.
Scan once on corp machine, commit the output, display it as the
"and now imagine this in prod" gut-punch moment.

| Image | CVEs |
|-------|------|
| `pytorch/pytorch:latest` | TBD (run on corp machine) |
| `cgr.dev/chainguard/pytorch:latest-dev` | TBD (run on corp machine) |

## Files to build (next session / corp machine)

- `scan.sh` — runs grype on the 3 Python images, pretty-prints comparison
- `results/python-311.txt` — pre-saved grype output
- `results/python-311-alpine.txt` — pre-saved grype output
- `results/chainguard-python.txt` — pre-saved grype output
- `results/pytorch-pytorch.txt` — pre-saved, from corp machine
- `results/chainguard-pytorch.txt` — pre-saved, from corp machine
- `README.md` — workshop instructions

## Narrative arc (20 min)

1. "Before we talk PyTorch, let's baseline with vanilla Python" (2 min)
2. Live scan python:3.11 → ugly number (3 min)
3. "Alpine is the 'secure' choice most teams reach for" → scan → better, not great (3 min)
4. Chainguard → basically zero (3 min)
5. "Now here's what you're actually running in your ML pipeline" → show pytorch/pytorch numbers (2 min)
6. Chainguard pytorch comparison → the close (2 min)
7. Discussion: Docker Desktop licensing (250-employee rule), Rancher Desktop alt,
   minimal base images as supply chain hygiene (5 min)

## Notes

- Docker Desktop licensing callout goes here — RSA crowd eats this up
- Grype installed via: `brew install grype` or `curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh`
- Prior art exists on corp machine — check there first
