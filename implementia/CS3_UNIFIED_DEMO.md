# Demo: Comparing Python Container Images for Supply Chain Security

In this demo, we'll scan three Python container images for vulnerabilities using [Grype](https://github.com/anchore/grype), a popular container image scanner. We'll compare base image choices to see their impact on supply chain security for ML pipelines.

We'll be moving through the following steps:

1. Install Grype (if needed)
2. Scan the official Python container image for vulnerabilities
3. Scan a Python Alpine image for comparison
4. Scan the Python Chainguard Image to see the security improvement
5. Discuss implications for ML pipelines using PyTorch

Let's jump in!

## Prerequisites

To follow this tutorial, you will need the following:

- Access to a UNIX-like terminal environment, such as the terminal on Mac OS or Linux or Windows Subsystem for Linux
- A working installation of [Docker Engine](https://docs.docker.com/engine/install/) or [Docker Desktop](https://docs.docker.com/desktop/)
- The [Grype scanner](https://github.com/anchore/grype#installation)

On most systems, Grype can be installed using the following command:

```sh
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

## Scanning the Official Python Image

Let's start by scanning the official Python image on Docker Hub:

```sh
grype python:3.11
```

On running this command, you should see dynamic output from Grype as the official Python image is pulled and scanned. After some time, you should receive a large amount of output. Output from Grype is divided into two parts: an initial overview and an itemized list of specific vulnerabilities. Let's first take a look at the initial overview — you may need to scroll up to find it.

```
 ✔ Loaded image                                                                                                                          python:3.11
 ✔ Parsed image                                                                      sha256:371d06a727271e250c913fb6e3adade4ce8d1f1a85df2ff96f072e0f3dfa0406
 ✔ Cataloged contents                                                                       4abedac2a866bcac0a507d433f2f2ba21fa8d1466be068ffcbf022d747728877
   ├── ✔ Packages                        [438 packages]
   ├── ✔ File digests                    [20,064 files]
   ├── ✔ File metadata                   [20,064 locations]
   └── ✔ Executables                     [1,425 executables]
 ✔ Scanned for vulnerabilities     [1276 vulnerability matches]
   ├── by severity: 7 critical, 118 high, 325 medium, 53 low, 612 negligible (161 unknown)
   └── by status:   75 fixed, 1201 not-fixed, 541 ignored
```

Arguably the most important line in this output is the breakdown of vulnerabilities by severity. CVEs are assigned numerical scores according to the [Common Vulnerability Scoring System (CVSS)](https://nvd.nist.gov/vuln-metrics/cvss). These scores correspond to four categories:

- Critical (9.0-10.0)
- High (7.0-8.9)
- Medium (4.0-6.9)
- Low (0.1-3.9)

The "by severity" line in our Grype output suggests that, as of February 2025, the official Python image had 7 critical, 118 high, 325 medium, and 53 low vulnerabilities.

```
   ├── by severity: 7 critical, 118 high, 325 medium, 53 low, 612 negligible (161 unknown)
```

Another line to look out for is how many of the CVEs have been fixed in a release:

```
   └── by status:   75 fixed, 1201 not-fixed, 541 ignored
```

If you're seeing CVEs with a "fixed" status, that indicates that updating to a new version of the affected package will resolve the issue. The more often an image is rebuilt with updated packages, the fewer fixed CVEs will be found.

Grype also itemizes each CVE found during the scan. This constitutes the second half of our output. Let's rerun the scan to look just at the CVEs that have critical status:

```
grype python:3.11 | grep -i critical
```

This produces output showing the critical vulnerabilities:

```
libaom3                       3.6.0-1+deb12u1               (won't fix)        deb     CVE-2023-6879     Critical
libopenexr-3-1-30             3.1.5-5                       (won't fix)        deb     CVE-2023-5841     Critical
libopenexr-dev                3.1.5-5                       (won't fix)        deb     CVE-2023-5841     Critical
wget                          1.21.3-1+b2                   (won't fix)        deb     CVE-2024-38428    Critical
zlib1g                        1:1.2.13.dfsg-1               (won't fix)        deb     CVE-2023-45853    Critical
zlib1g-dev                    1:1.2.13.dfsg-1               (won't fix)        deb     CVE-2023-45853    Critical
```

If you're resolving CVEs manually, this output is your starting point. Generally, you would look up the CVE on [nist.gov](https://www.nist.gov/), which collects information on affected packages and systems, disclosures, and additional resources for learning about CVEs, such as advisories and potential mitigations. Since the above packages are marked as `(won't fix)`, you will need to either determine that the CVE isn't relevant to your use case, remove the affected package, or manually mitigate the CVE.

## Scanning Python Alpine

Many teams reach for Alpine Linux as a "minimal" base image. Let's see how it compares:

```sh
grype python:3.11-alpine
```

You should see significantly fewer CVEs compared to the Debian-based image. Alpine's smaller package count means fewer potential vulnerabilities.

**Typical results (as of February 2025):**
```
 ✔ Scanned for vulnerabilities     [40 vulnerability matches]
   ├── by severity: 0 critical, 8 high, 18 medium, 14 low
```

While Alpine is a substantial improvement over the standard Debian-based Python image, it still carries vulnerabilities from its package ecosystem. The reduction from ~500 actionable CVEs to ~40 is significant, but we can do better.

## Scanning Chainguard Python

Chainguard Images are built on Wolfi, a minimal Linux distribution designed for containers, with daily CVE scanning and automated patching. Let's scan the Chainguard Python image:

```sh
grype cgr.dev/chainguard/python:latest
```

On most days this scan is run, you will find zero CVEs in the Python Chainguard Image. As of February 2025, there may be one CVE reported with unknown status:

```
 ✔ Scanned for vulnerabilities     [1 vulnerability match]
   ├── by severity: 0 critical, 0 high, 0 medium, 0 low, 0 negligible (1 unknown)
```

```
python-3.13  3.13.2-r2            apk   CVE-2024-3220  Unknown
```

Unknown CVEs are CVEs that are currently under investigation. They may or may not be assigned a severity status in the future. In this case, we might consider this a 99.9986% reduction in CVEs (from 736 to 1), though an analysis that more properly ignored CVEs with unknown status would put this at a 100% reduction. 😎

The dramatic reduction comes from:
1. Minimal package set (only what Python needs)
2. Daily automated security patching
3. Wolfi distroless approach

This is the gold standard for production ML pipelines.

## Comparison Summary

| Image | Base | Total CVEs | Critical/High | Packages |
|-------|------|-----------|---------------|----------|
| python:3.11 | Debian | ~500+ | ~125 | 438 |
| python:3.11-alpine | Alpine | ~40 | ~8 | ~180 |
| cgr.dev/chainguard/python:latest | Wolfi | 0-1 | 0 | ~50 |

**Key Insight:** Base image choice can eliminate 99%+ of CVEs in your supply chain.

## Implications for ML Pipelines

Python images are relatively small (~1GB). ML frameworks like PyTorch are much larger (~5-10GB), making live scanning time-consuming. However, the same pattern applies:

**PyTorch CVE Comparison (pre-scanned results):**
- `pytorch/pytorch:latest`: ~500+ CVEs (large Debian base + CUDA + ML libraries)
- `cgr.dev/chainguard/pytorch:latest-dev`: ~0-5 CVEs (minimal Wolfi base)

For ML pipelines, this matters because:
1. **Attack surface:** More packages = more potential exploits
2. **Compliance:** Fewer CVEs = easier audits
3. **Patching velocity:** Minimal images update faster
4. **Defense in depth:** Hardening the container layer complements application security

The pickle deserialization and model poisoning attacks we've covered in earlier case studies are amplified when running in vulnerable containers. A compromised package in your base image can be exploited to gain initial access, after which attackers can leverage ML-specific vulnerabilities. Defense in depth means hardening every layer of the stack.

## Resources

- [Overview of Chainguard Images](https://edu.chainguard.dev/chainguard/chainguard-images/overview/)
- [Migrating to Python Chainguard Images](https://edu.chainguard.dev/chainguard/migration/migrating-python/)
- [Chainguard Images for ML Pipelines](https://images.chainguard.dev/directory/image/pytorch/overview) - PyTorch, TensorFlow, and other ML images
- [Chainguard Deep Dive: Where Does Grype Data Come From?](https://dev.to/chainguard/deep-dive-where-does-grype-data-come-from-n9e)
- [Why Chainguard uses Grype](https://www.chainguard.dev/unchained/why-chainguard-uses-grype-as-its-first-line-of-defense-for-cves)
