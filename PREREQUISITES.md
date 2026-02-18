# Prerequisites — ML Pipeline Security Workshop

Complete these steps **before the workshop**. The Docker image builds take ~10 minutes on a fast connection and require internet access, so please don't leave this for session day.

---

## 1. Docker

You need a working Docker installation that can build and run Linux container images.

### macOS / Linux

Any of the following will work:

- [Docker Engine](https://docs.docker.com/engine/install/) — just the daemon and CLI, no GUI. Easiest on Linux.
- [Docker Desktop](https://docs.docker.com/desktop/) — GUI wrapper around Engine. Free for individuals and companies with fewer than 250 employees.
- [Rancher Desktop](https://rancherdesktop.io/) — free, no license restrictions. Select the **dockerd** runtime during setup.

### Windows

Windows requires **WSL 2** (Windows Subsystem for Linux). If you don't already have it:

1. Open PowerShell as Administrator and run:
   ```powershell
   wsl --install
   ```
   This installs WSL 2 with Ubuntu. Restart when prompted.

2. After reboot, open the **Ubuntu** terminal from your Start menu. Set a username and password when asked.

3. Install Docker inside WSL. You have two options:

   - **Docker Engine directly in WSL** (no Desktop needed):
     ```sh
     # Inside the Ubuntu terminal
     curl -fsSL https://get.docker.com | sh
     sudo usermod -aG docker $USER
     ```
     Log out and back in (or run `newgrp docker`) for the group change to take effect.

   - **Docker Desktop for Windows** from [docker.com](https://docs.docker.com/desktop/setup/install/windows-install/) (or Rancher Desktop). Make sure "Use WSL 2 based engine" is checked, then enable your Ubuntu distro under Settings > Resources > WSL Integration.

> **Important — use the WSL filesystem for everything.**
> Open the Ubuntu terminal and work from your home directory (`~/`). Do **not** clone the repo to `/mnt/c/...` — file I/O through the Windows filesystem bridge is 10-50x slower and will make Docker builds and model training painful.

### Verify Docker

```sh
docker run --rm hello-world
```

You should see "Hello from Docker!" If this fails, check that Docker is running and your user has permission to access the Docker socket.

---

## 2. Git

### macOS

Git ships with the Xcode command line tools:
```sh
xcode-select --install
```

### Linux / WSL

```sh
sudo apt update && sudo apt install -y git
```

### Windows

Use Git inside WSL (see above). Do not use Git for Windows for this workshop.

---

## 3. Clone the Repository

```sh
git clone https://github.com/chainguard-demo/ml-pipeline-security.git
cd ml-pipeline-security
```

On Windows, run this **inside the Ubuntu/WSL terminal**, not PowerShell.

---

## 4. Grype (Vulnerability Scanner)

[Grype](https://github.com/anchore/grype) is used in Case Study 3 to scan container images for CVEs.

### macOS (Homebrew)

```sh
brew install grype
```

### Linux / WSL

```sh
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

### Verify Grype

```sh
grype --version
```

---

## 5. Pre-Build Docker Images

The workshop uses two Docker images. Build them now so you're not waiting during the session.

### Case Study 1 — Pickle Deserialization (~2 min)

```sh
cd demo-pickle
docker build -t pickle-demo .
cd ..
```

### Case Study 2 — Model Poisoning (~8 min)

This build trains two ML models (clean and poisoned) during the Docker build step. It takes a few minutes on CPU — a good time to grab a coffee.

```sh
cd demo-poisoning
docker build -t poisoning-demo .
cd ..
```

### Verify Builds

```sh
docker images | grep -E "pickle-demo|poisoning-demo"
```

You should see both images listed.

---

## 6. Pull Base Images for Case Study 3 (~2 min)

Case Study 3 scans container images live. Pre-pulling them saves time during the workshop:

```sh
docker pull python:3.11
docker pull python:3.11-alpine
docker pull cgr.dev/chainguard/python:latest
```

---

## Quick Verification Checklist

Run these commands and confirm each one works:

```sh
docker run --rm hello-world              # Docker works
grype --version                          # Grype installed
docker run --rm -it pickle-demo /bin/sh -c "echo CS1 OK"          # CS1 image built
docker run --rm -it poisoning-demo /bin/sh -c "echo CS2 OK"       # CS2 image built
grype python:3.11 2>&1 | head -15        # Grype can scan images
```

If all five commands succeed, you're ready for the workshop.

---

## Troubleshooting

### Docker build fails pulling Chainguard images

Chainguard images require internet access. If you're behind a corporate proxy, you may need to configure Docker's proxy settings:
- **Docker Desktop**: Settings > Resources > Proxies
- **CLI**: Set `HTTP_PROXY` and `HTTPS_PROXY` in `~/.docker/config.json`

### WSL: "Cannot connect to the Docker daemon"

If using Docker Engine in WSL, start the daemon:
```sh
sudo service docker start
```

If using Docker Desktop, make sure it's running and WSL integration is enabled (Settings > Resources > WSL Integration).

### WSL: Builds or training are extremely slow

You're probably running from the Windows filesystem. Check your path:
```sh
pwd
```
If it starts with `/mnt/c/`, move to your WSL home directory:
```sh
cp -r /mnt/c/path/to/rsa ~/rsa
cd ~/rsa
```

### Grype: "database is out of date" warning

Update the Grype vulnerability database:
```sh
grype db update
```

### Docker Desktop licensing

Docker Desktop requires a paid subscription for companies with 250+ employees. [Rancher Desktop](https://rancherdesktop.io/) is a free alternative — select the **dockerd (moby)** container runtime during setup and everything in this workshop works identically.
