# GPU Memory Hierarchy

## Overview

GPUs have a multi-level memory hierarchy designed for high-throughput parallel access. Understanding it is essential for reasoning about why LLM inference is memory-bandwidth-bound and what techniques like FlashAttention and quantization actually improve.

## Memory Levels

```
┌─────────────────────────────────────────────┐
│  GPU Chip                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  SM 0    │  │  SM 1    │  │  SM ...  │  │
│  │ Registers│  │ Registers│  │          │  │
│  │ L1/Shared│  │ L1/Shared│  │          │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       └─────────────┴─────────────┘         │
│                  L2 Cache                   │
└──────────────────┬──────────────────────────┘
                   │ memory bus
             ┌─────┴──────┐
             │  HBM (VRAM)│  (off-chip, high bandwidth)
             └────────────┘
```

| Level | Size | Bandwidth | Latency | Scope |
|---|---|---|---|---|
| **Registers** | ~256 KB/SM | ~100 TB/s | ~1 cycle | Per thread |
| **L1 / Shared Memory (SRAM)** | 128–256 KB/SM | ~20 TB/s | ~5 cycles | Per SM |
| **L2 Cache** | 40–50 MB | ~10 TB/s | ~100 cycles | Whole GPU |
| **HBM (VRAM)** | 40–141 GB | 2–4.8 TB/s | ~400 cycles | Whole GPU |

## HBM (High Bandwidth Memory)

- The main GPU memory — what people mean by "GPU memory" or VRAM
- Stacked DRAM dies connected via a wide memory bus
- **A100**: 80 GB HBM2e, ~2 TB/s
- **H100 SXM**: 80 GB HBM3, ~3.35 TB/s
- **H200**: 141 GB HBM3e, ~4.8 TB/s — critical for long-context LLMs

HBM is fast compared to CPU DRAM (~50 GB/s) but slow compared to on-chip SRAM.

## SRAM (Shared Memory / L1)

- On-chip memory inside each Streaming Multiprocessor (SM)
- ~10× higher bandwidth than HBM, ~100× lower latency
- Very small: 128–256 KB per SM (H100 has 132 SMs → ~32 MB total)
- Must be managed explicitly by the programmer (or compiler)

## Why This Matters for LLMs

**Decode is memory-bandwidth-bound.** During autoregressive generation, each step:
1. Loads the entire model weights (~140 GB for a 70B FP16 model) from HBM
2. Performs a tiny amount of compute (one token's forward pass)

The ratio of compute to memory access (arithmetic intensity) is very low → GPU spends most time waiting for HBM reads, not computing. Faster HBM (H200) and quantization (fewer bytes to load) directly improve decode throughput.

**FlashAttention moves attention computation into SRAM.** Standard attention writes the full N×N attention matrix to HBM and reads it back. FlashAttention tiles the computation to fit in SRAM, avoiding expensive HBM round-trips. This is why it's so much faster for long sequences.

**Quantization reduces HBM traffic.** INT4 weights are 4× smaller than FP16 → 4× fewer bytes read per decode step → proportionally faster.

## Roofline Model

The roofline model predicts whether a kernel is compute-bound or memory-bound:
- **Arithmetic intensity** = FLOPs / bytes accessed
- If intensity < ridge point → **memory-bound** (HBM bandwidth is the bottleneck)
- If intensity > ridge point → **compute-bound** (FLOP throughput is the bottleneck)

LLM decode: ~2 FLOPs per weight byte → very memory-bound on all current GPUs.
LLM prefill with large batches: higher intensity → more compute-bound.

## Related Topics
- [CUDA Basics](../CUDA-Basics/cuda-basics.md)
- [Inference Optimization](../../../Artificial-Intelligence/Machine-Learning-Engineering/LLM-Serving/Inference-Optimization/inference-optimization.md)
