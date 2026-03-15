# Docker

## Overview

Docker is the standard tool for building and running containers — isolated, reproducible environments that package an application with all its dependencies. It's the foundation you need before Kubernetes makes sense: K8s orchestrates containers, so you first need to understand what a container is and how Docker creates one.

## Containers vs Virtual Machines

```
VM                          Container
──────────────────          ──────────────────
App                         App
Guest OS (full kernel)      Libs / deps only
Hypervisor                  Container runtime (Docker)
Host OS                     Host OS kernel (shared)
Hardware                    Hardware
```

- Containers share the host OS kernel → much lighter (~MBs vs ~GBs, starts in ms vs minutes)
- Isolation via Linux **namespaces** (process, network, filesystem) and **cgroups** (CPU/memory limits)

## Core Concepts

- **Image**: Read-only template for a container. Built from a `Dockerfile`. Stored in layers.
- **Container**: A running instance of an image. Ephemeral by default — data is lost when it stops.
- **Registry**: Image storage (Docker Hub, GitHub Container Registry, AWS ECR). `docker pull/push`.
- **Volume**: Persistent storage mounted into a container — survives container restarts.

## Dockerfile

```dockerfile
FROM python:3.11-slim          # base image

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt   # creates a new layer

COPY . .
EXPOSE 8000
CMD ["python", "server.py"]   # default command when container starts
```

Each `RUN`, `COPY`, `ADD` creates a new **layer**. Layers are cached — only changed layers rebuild, making iteration fast.

## Common Commands

```bash
# Build
docker build -t my-app:v1 .

# Run
docker run -p 8080:8000 -v /data:/app/data my-app:v1

# Inspect
docker ps                        # running containers
docker logs <container-id>
docker exec -it <container-id> bash

# Images
docker images
docker pull nvidia/cuda:12.1-base
docker push myregistry/my-app:v1
```

## Docker for ML

```dockerfile
FROM nvidia/cuda:12.1-cudnn8-runtime-ubuntu22.04

RUN pip install torch vllm
COPY model_server.py .
CMD ["python", "model_server.py"]
```

- **NVIDIA Container Toolkit**: Exposes GPUs to containers via `--gpus all` flag
- **Multi-stage builds**: Separate build environment from runtime image to reduce final image size
- **Docker Compose**: Run multi-container setups locally (e.g., inference server + Redis cache)

## Relationship to Kubernetes

Docker creates the container images. Kubernetes pulls and runs those images across a cluster, adding scheduling, scaling, networking, and health management on top. The workflow:
1. Write `Dockerfile` → build image → push to registry
2. Kubernetes pulls the image onto worker nodes and runs it as Pods

## Related Topics
- [Kubernetes](../../Container-Orchestration/Kubernetes/kubernetes.md)
- [Containers](../containers.md)
