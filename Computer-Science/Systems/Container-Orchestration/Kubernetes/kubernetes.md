# Kubernetes

## Overview

Kubernetes (K8s) is an open-source container orchestration platform originally built at Google, now maintained by the CNCF. It automates deployment, scaling, and management of containerized applications across a cluster of machines.

## Core Concepts

### Cluster Components
- **Control Plane**: Manages cluster state — API Server, Scheduler, etcd (distributed key-value store), Controller Manager
- **Worker Nodes**: Machines that run application workloads

### Workload Primitives
- **Pod**: Smallest deployable unit — one or more containers sharing network/storage
- **Deployment**: Declarative spec for a set of replicated Pods with rolling update support
- **StatefulSet**: Like Deployment but for stateful apps needing stable identities and persistent storage
- **DaemonSet**: Ensures one Pod runs on every node (used for GPU drivers, monitoring agents)
- **Job / CronJob**: Run-to-completion workloads

### Networking
- **Service**: Stable virtual IP + DNS name load-balancing across Pods
  - `ClusterIP` (internal), `NodePort` (per-node), `LoadBalancer` (cloud LB)
- **Ingress**: HTTP/HTTPS routing rules into the cluster

### Configuration & Storage
- **ConfigMap / Secret**: Non-sensitive / sensitive config injected into Pods
- **PersistentVolume (PV) / PersistentVolumeClaim (PVC)**: Durable storage abstraction

## Scheduling & Resource Management

```yaml
resources:
  requests:
    memory: "4Gi"
    nvidia.com/gpu: 1    # requires NVIDIA device plugin
  limits:
    memory: "8Gi"
    nvidia.com/gpu: 1
```

- `requests`: Minimum guaranteed resources — used by the scheduler to place Pods
- `limits`: Maximum the container can consume
- **Taints & Tolerations**: Mark GPU nodes as tainted so only GPU workloads are scheduled on them
- **Node Affinity**: Pin Pods to specific node types (e.g., `nvidia.com/gpu.product=A100`)

## Kubernetes for ML Workloads

| Use Case | K8s Feature |
|---|---|
| Serve inference endpoints | Deployment + HPA (auto-scale on GPU utilization) |
| Distributed training | Job + operator (Kubeflow, Volcano, PyTorchJob) |
| GPU node isolation | Taints + NVIDIA GPU Operator |
| Model artifacts | PVC backed by object storage (S3, GCS) |
| Config/secrets | ConfigMap + Secret |

**Helm**: Package manager for Kubernetes. Reusable app definitions (charts) deploy complex stacks (vLLM, Ray, Triton) in one command.

## Common kubectl Commands

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name>
kubectl logs <pod-name> -c <container> -f
kubectl exec -it <pod-name> -- bash
kubectl apply -f deployment.yaml
kubectl scale deployment <name> --replicas=3
kubectl top nodes   # resource usage
```

## Related Topics
- [Distributed LLM Systems](../../../Artificial-Intelligence/Machine-Learning-Engineering/LLM-Serving/Distributed-LLM-Systems/distributed-llm-systems.md)
- [vLLM](../../../Artificial-Intelligence/Machine-Learning-Engineering/LLM-Serving/Inference-Optimization/vLLM/vllm.md)

## References
- Kubernetes official docs: https://kubernetes.io/docs/
- NVIDIA GPU Operator: GPU driver and device plugin management on K8s
- Kubeflow: ML pipelines and distributed training on K8s
