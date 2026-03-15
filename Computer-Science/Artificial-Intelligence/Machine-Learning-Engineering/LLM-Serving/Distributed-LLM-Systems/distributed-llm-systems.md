# Distributed LLM Systems

## Overview

Distributed LLM systems split the work of running a large language model across multiple GPUs or machines. This is necessary because modern LLMs (70B+ parameters) exceed the memory of a single GPU, and even smaller models benefit from distribution for higher throughput.

## Parallelism Strategies

### Tensor Parallelism (TP)
Split individual weight matrices across GPUs. Each GPU holds a shard of each layer.
- Requires **all-reduce** communication at every layer → high interconnect bandwidth needed (NVLink preferred)
- Best within a single node (8 GPUs with NVLink)
- Example: A 70B model with TP=8 → each GPU holds ~8.75B parameters worth of weights

### Pipeline Parallelism (PP)
Assign different **layers** to different GPUs/nodes. GPU 0 runs layers 0–15, GPU 1 runs layers 16–31, etc.
- Communication only at pipeline stage boundaries (send/recv activations)
- Works across nodes over slower interconnects (InfiniBand)
- Introduces **pipeline bubbles** (idle time waiting for previous stage); micro-batching reduces this

### Data Parallelism (DP)
Run multiple **replicas** of the full model, each handling different requests.
- No parameter communication during inference forward pass
- Trivially scales throughput: N replicas = N× throughput
- Requires each replica to fit in GPU memory; often combined with TP

### Combining Strategies
```
TP=4, PP=2, DP=2  →  4 × 2 × 2 = 16 GPUs total
```
- TP handles intra-layer splitting (within a node)
- PP handles inter-layer splitting (across nodes)
- DP handles request-level scaling

## Prefill vs. Decode Disaggregation

Two phases of LLM inference have fundamentally different compute profiles:

| Phase | Bottleneck | Batch Preference |
|---|---|---|
| **Prefill** (process prompt) | Compute-bound | Large batches |
| **Decode** (generate tokens) | Memory bandwidth-bound | Continuous batching |

**Disaggregated serving**: Route prefill to high-compute nodes, decode to high-bandwidth nodes. Used in Mooncake (Kimi), DistServe, and similar production systems.

## KV Cache at Scale

The KV cache stores attention key/value tensors for each token in the context. At scale:
- **Memory bottleneck**: Long contexts × many concurrent requests → GBs of KV cache needed
- **Disaggregated KV cache**: Separate prefill and decode compute nodes, cache transferred over RDMA
- **Prefix caching**: Reuse KV blocks for shared prompt prefixes across requests

## Cluster Topology

```
Node 0:  [GPU 0] [GPU 1] [GPU 2] [GPU 3]  ← NVLink within node (~600 GB/s)
         ↕ InfiniBand
Node 1:  [GPU 4] [GPU 5] [GPU 6] [GPU 7]  ← NVLink within node
```

- **NVLink**: ~600 GB/s bidirectional — use for tensor parallelism (all-reduce)
- **InfiniBand (400Gbps)**: ~50 GB/s — use for pipeline parallelism (point-to-point activations)

## Orchestration

- **Ray**: Python distributed computing framework; used by vLLM for multi-GPU/multi-node serving
- **Kubernetes**: Cluster-level orchestration for deploying and scaling serving infrastructure

## Related Topics
- [Inference Optimization](../Inference-Optimization/inference-optimization.md)
- [vLLM](../Inference-Optimization/vLLM/vllm.md)
- [Kubernetes](../../../../Systems/Container-Orchestration/Kubernetes/kubernetes.md)

## References
- Megatron-LM: Tensor and pipeline parallelism at scale (NVIDIA)
- DistServe: Disaggregating Prefill and Decoding for Goodput-Optimized LLM Serving
- Mooncake: Kimi's KV cache disaggregation architecture
