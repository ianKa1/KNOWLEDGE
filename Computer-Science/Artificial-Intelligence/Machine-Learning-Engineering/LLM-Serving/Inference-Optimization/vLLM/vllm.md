# vLLM

## Overview

vLLM is an open-source LLM inference and serving library from UC Berkeley. Its core innovation — **PagedAttention** — manages the KV cache using virtual memory paging, eliminating fragmentation and enabling prefix sharing. This achieves up to 24× higher throughput than naive HuggingFace implementations.

## Core Innovation: PagedAttention

Traditional serving pre-allocates a contiguous memory block for each request's KV cache based on max sequence length → up to 60–80% of GPU memory wasted from fragmentation.

PagedAttention treats KV cache like OS virtual memory:
- KV cache split into fixed-size **pages** (blocks of tokens)
- Pages allocated **on demand** as tokens are generated
- Non-contiguous physical pages mapped via a **block table** (like a page table)
- Requests sharing the same prompt prefix can **share physical pages** — no duplication

```
Request A: [block 0] → [block 3] → [block 7]   (non-contiguous OK)
Request B: [block 0] → [block 5]                (shares block 0 = same system prompt)
```

## Architecture

```
  HTTP Requests → OpenAI-compat API
                       │
                  LLM Engine
             (Scheduler + Block Manager)
                       │ async
                  Worker(s)
              [GPU 0 … GPU N via Ray]
```

- **Scheduler**: Selects which requests to prefill/decode each step; implements continuous batching
- **Block Manager**: Allocates/frees KV cache pages; handles prefix sharing
- **Workers**: One per GPU, coordinated via Ray or multiprocessing

## Key Features

- **Continuous batching**: Requests join/leave each decode step — maximizes GPU utilization
- **Tensor parallelism**: Multi-GPU via NCCL (`--tensor-parallel-size N`)
- **Prefix caching**: Automatic reuse of KV pages for repeated prompt prefixes (system prompts, few-shot examples)
- **OpenAI-compatible API**: Drop-in replacement for OpenAI client code
- **Quantization**: FP8, AWQ, GPTQ supported at startup

## Launching vLLM

```bash
# Single GPU
vllm serve meta-llama/Llama-3.1-8B-Instruct

# Multi-GPU
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9

# With AWQ quantization
vllm serve Qwen/Qwen2.5-72B-Instruct-AWQ \
  --quantization awq --tensor-parallel-size 4
```

## Multimodal Support (Omni)

vLLM supports vision-language and omni-modal models (text + vision + audio):
```bash
vllm serve llava-hf/llava-onevision-qwen2-7b-ov-hf
```
"vLLM-omni" refers to serving omni-modal models (e.g., Qwen2.5-Omni, Kimi-Audio) through vLLM's multimodal pipeline, which handles interleaved token streams from different modalities.

## vLLM V1 (2024+)

Major architecture refactor:
- Async scheduling: overlaps GPU compute with CPU scheduling
- Chunked prefill: breaks large prompts into chunks interleaved with decode, reducing TTFT jitter
- Zero-copy prefix caching: block table reuse without data movement
- Improved multimodal support

## Related Topics
- [Inference Optimization](../inference-optimization.md)
- [Distributed LLM Systems](../../Distributed-LLM-Systems/distributed-llm-systems.md)
- [Kubernetes](../../../../../Systems/Container-Orchestration/Kubernetes/kubernetes.md)

## References
- PagedAttention paper: Efficient Memory Management for LLM Serving (Kwon et al., 2023)
- vLLM GitHub: https://github.com/vllm-project/vllm
