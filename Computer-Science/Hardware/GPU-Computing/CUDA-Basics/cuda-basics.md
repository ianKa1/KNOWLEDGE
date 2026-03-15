# CUDA Basics

## Overview

CUDA (Compute Unified Device Architecture) is NVIDIA's parallel programming model for GPU computation. Understanding CUDA basics is essential for making sense of GPU performance, kernel optimizations, and why frameworks like PyTorch and vLLM behave the way they do.

## Execution Model

```
CPU (Host)                     GPU (Device)
──────────                     ────────────
Launch kernel ────────────────► Grid
                                 └── Blocks (up to 3D)
                                       └── Threads (up to 1024/block)
```

- **Thread**: The smallest unit of execution. Runs the kernel function once.
- **Block**: A group of threads that share L1/shared memory and can synchronize with `__syncthreads()`
- **Grid**: All blocks launched for one kernel call
- **Warp**: 32 threads that execute in lockstep (the real hardware unit). Branch divergence within a warp is expensive.

## Memory Spaces

| Space | Declared with | Scope | Speed |
|---|---|---|---|
| Registers | automatic (local vars) | per thread | fastest |
| Shared memory | `__shared__` | per block | fast |
| Global memory (HBM) | `cudaMalloc` / tensor data | all threads | slow |
| Constant memory | `__constant__` | all threads (read-only) | fast if cached |

The key skill in GPU programming is **minimizing global memory accesses** by staging data through shared memory.

## Kernel Launch Syntax

```cuda
// Device kernel
__global__ void add(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

// Host launch
int threads_per_block = 256;
int blocks = (n + threads_per_block - 1) / threads_per_block;
add<<<blocks, threads_per_block>>>(a, b, c, n);
cudaDeviceSynchronize();
```

## Coalesced Memory Access

GPUs read global memory in 128-byte transactions per warp. If 32 threads access 32 consecutive floats → **one transaction** (coalesced). If they access scattered addresses → **32 transactions** (32× slower).

```
Coalesced:   thread 0 → addr 0, thread 1 → addr 4, thread 2 → addr 8, ...  ✓
Strided:     thread 0 → addr 0, thread 1 → addr 128, thread 2 → addr 256, ... ✗
```

## CUDA Streams

Operations on the same stream execute in order. Operations on different streams can overlap:
```python
# PyTorch example
stream1 = torch.cuda.Stream()
stream2 = torch.cuda.Stream()
with torch.cuda.stream(stream1):
    out1 = model_part1(x)       # runs on stream1
with torch.cuda.stream(stream2):
    out2 = model_part2(y)       # overlaps with stream1
```
Used in vLLM and TensorRT-LLM to overlap data transfer with compute.

## Relevance to ML Frameworks

You rarely write CUDA kernels directly when doing ML. But CUDA concepts explain:
- Why **batch size** matters: more threads → better GPU utilization
- Why **contiguous tensors** are faster: coalesced access
- Why **`.cuda()`** copies data to HBM (device global memory)
- What **CUDA kernels** are in PyTorch profiler output
- Why **fused kernels** (like FlashAttention) are faster: fewer HBM round-trips

## Related Topics
- [GPU Memory Hierarchy](../GPU-Memory-Hierarchy/gpu-memory-hierarchy.md)
- [Deep Learning Frameworks](../../../Artificial-Intelligence/Machine-Learning-Engineering/Deep-Learning-Frameworks/deep-learning-frameworks.md)
- [Inference Optimization](../../../Artificial-Intelligence/Machine-Learning-Engineering/LLM-Serving/Inference-Optimization/inference-optimization.md)
