# Inference Optimization

## Overview

Inference optimization covers all techniques that reduce the latency or increase the throughput of running a trained model. For LLMs, the two primary bottlenecks are:
- **Memory bandwidth** (loading weights per generated token — decode is memory-bound)
- **Compute** (attention over long contexts — prefill is compute-bound)

## Key Metrics

| Metric | Definition |
|---|---|
| TTFT | Time to first token — latency of the prefill phase |
| TPOT | Time per output token — latency per decode step |
| Throughput | Total tokens/sec across all concurrent requests |

## Quantization

Reduce weight/activation precision to shrink memory footprint and accelerate compute.

| Format | Memory vs FP16 | Quality loss |
|---|---|---|
| FP16 (baseline) | 1× | — |
| FP8 | 0.5× | Minimal (native H100 support) |
| INT8 | 0.5× | Minimal |
| INT4 (GPTQ, AWQ) | 0.25× | Small |

- **GPTQ**: Post-training quantization using second-order information; weights-only
- **AWQ (Activation-aware Weight Quantization)**: Protects salient weight channels; better quality than GPTQ at same bit-width

## Speculative Decoding

Use a small **draft model** to generate K candidate tokens, then verify all K with the large **target model** in one forward pass.
- If all K accepted: K tokens generated in ~1 target forward pass time
- Typical speedup: 2–3× depending on acceptance rate
- Draft can be a smaller distilled model or early-exit variant of the same model

## Flash Attention

Rewrite the attention kernel to avoid materializing the full N×N attention matrix in HBM.
- Fuses QKV computation into a single GPU kernel using SRAM tiling
- Reduces attention memory from O(N²) to O(N); critical for long contexts
- **FlashAttention-2/3**: Further optimized for A100/H100; supports GQA and MHA

## Continuous Batching

Instead of waiting for all requests in a batch to finish, add new requests as soon as a slot frees up (iteration-level batching).
- Eliminates GPU idle time from padding short responses to the longest in a static batch
- Key enabler of high-throughput serving — used in vLLM, TGI, TensorRT-LLM

## KV Cache Optimizations

- **Grouped Query Attention (GQA)**: Multiple query heads share one K/V head → reduces KV cache by head_ratio×
- **Multi-Query Attention (MQA)**: All queries share a single K/V head — extreme reduction
- **Prefix Caching**: Cache KV blocks for shared prompt prefixes; reuse on subsequent requests
- **PagedAttention** (vLLM): Non-contiguous KV cache pages — near-zero fragmentation

## Inference Frameworks

| Framework | Strength |
|---|---|
| **vLLM** | PagedAttention, easy deployment, OpenAI-compatible API |
| **TensorRT-LLM** (NVIDIA) | Maximum GPU throughput via fused CUDA kernels |
| **TGI** (HuggingFace) | Production serving, broad model support |
| **llama.cpp** | CPU inference, GGUF quantization, consumer hardware |

## Related Topics
- [vLLM](./vLLM/vllm.md)
- [Distributed LLM Systems](../Distributed-LLM-Systems/distributed-llm-systems.md)
- [Deep Learning Frameworks](../../Deep-Learning-Frameworks/deep-learning-frameworks.md)

## References
- FlashAttention-2: Faster Attention with Better Parallelism (Dao, 2023)
- AWQ: Activation-aware Weight Quantization (Lin et al., 2023)
- Speculative Decoding (Leviathan et al., 2022)
