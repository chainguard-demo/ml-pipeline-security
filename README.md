# Securing ML Pipelines: Way More Than You Wanted to Know

- [Session page](https://path.rsaconference.com/flow/rsac/us26/FullAgenda/page/catalog/session/1755534205972001suaj) — RSAC 2026 Learning Lab [LAB2-W08]
- Wednesday, March 25, 1:15–3:15 PM PDT
- Dr. Patrick Smyth, Principal Developer Relations Engineer, Chainguard

ML pipelines are vulnerable due to the immaturity of the ecosystem, the large attack surface of popular ML frameworks, and the unique properties of ML models. In this technical workshop, participants will put on their plumber hats and get dirty hardening vulnerable ML pipelines, covering safe model deserialization, training data ingestion, and infrastructure deployment.

---

## Prerequisites

[Docker](https://docs.docker.com/get-started/get-docker/) and [Grype](https://github.com/anchore/grype) are required. See [PREREQUISITES.md](PREREQUISITES.md) for install instructions covering macOS, Windows, and Linux.

---

## Exercises

### [Exercise 1: Pickle Deserialization](exercise_1/) (25 min)

PyTorch models use pickle. Pickle executes arbitrary code on load. We'll exploit this, then switch to SafeTensors as the safe alternative.

### [Exercise 2: Model Poisoning](exercise_2/) (30 min)

An attacker poisons a traffic sign dataset so that a yellow sticker on a stop sign makes the model predict "yield." We'll demonstrate the backdoor, then show how training on clean data prevents it.

### [Exercise 3: Supply Chain CVEs](exercise_3/) (20 min)

We'll scan Python container images with Grype and compare CVE counts across base image choices — from hundreds of vulnerabilities down to zero.
