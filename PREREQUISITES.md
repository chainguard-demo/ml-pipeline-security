# Prerequisites

The following software is required to participate in the workshop.

---

## 1. Docker

You need a working Docker installation that can build and run Linux container images.

### macOS

Install [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/).

### Linux

Install [Docker Engine](https://docs.docker.com/engine/install/).

### Windows

Windows requires WSL 2 (Windows Subsystem for Linux). If you don't already have it:

1. Open PowerShell as Administrator and run:
   ```powershell
   wsl --install
   ```
   This installs WSL 2 with Ubuntu. Restart when prompted.

2. After reboot, open the Ubuntu terminal from your Start menu. Set a username and password when asked.

3. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Make sure "Use WSL 2 based engine" is checked (this is the default), then enable your Ubuntu distro under Settings > Resources > WSL Integration.

> Important — use the WSL filesystem for everything.
> Open the Ubuntu terminal and work from your home directory (`~/`). Do not work from `/mnt/c/...` — file I/O through the Windows filesystem bridge is 10-50x slower and will make container builds and model training painful.

### Verify Docker

```sh
docker run --rm hello-world
```

You should see "Hello from Docker!" If this fails, check that Docker is running and your user has permission to access the Docker socket.

---

## 2. Grype

[Grype](https://github.com/anchore/grype) is used in Exercise 3 to scan container images for CVEs.

### macOS (Homebrew)

```sh
brew install grype
```

### macOS (manual)

```sh
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

### Linux

```sh
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

### Windows

Run this inside the Ubuntu/WSL terminal (not PowerShell):

```sh
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

### Verify Grype

```sh
grype --version
```

---

## Troubleshooting

### Container build fails pulling Chainguard images

Chainguard images require internet access. If you're behind a corporate proxy, you may need to configure Docker's proxy settings:
- Docker Desktop: Settings > Resources > Proxies
- CLI: Set `HTTP_PROXY` and `HTTPS_PROXY` in `~/.docker/config.json`

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
