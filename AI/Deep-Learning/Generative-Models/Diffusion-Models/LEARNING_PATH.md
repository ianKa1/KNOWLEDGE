# Learning Path: Diffusion Models

> **Note**: This is the dedicated Diffusion Models guide. If you are new to generative models and haven't studied VAEs yet, start with the [Generative Models combined guide](../LEARNING_PATH.md) first — VAE builds the intuition for latent spaces and ELBO that diffusion theory extends.

**Estimated total time**: 8–10 weeks part-time (8–12 hrs/week)
**Target level**: Intermediate (assumes PyTorch, basic probability, familiarity with neural networks)
**Last updated**: 2026-03-16

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1 — Probabilistic Foundations & the Forward Process](#phase-1--probabilistic-foundations--the-forward-process-week-12)
4. [Phase 2 — DDPM: Training & Sampling](#phase-2--ddpm-training--sampling-week-34)
5. [Phase 3 — Score-Based Generative Models](#phase-3--score-based-generative-models-week-5)
6. [Phase 4 — Conditional Generation & Latent Diffusion](#phase-4--conditional-generation--latent-diffusion-week-67)
7. [Phase 5 — Modern Architectures & Advanced Topics](#phase-5--modern-architectures--advanced-topics-week-810)
8. [Curated Resources](#curated-resources)
9. [Practical Projects](#practical-projects)
10. [Common Pitfalls](#common-pitfalls)
11. [Assessment Checkpoints](#assessment-checkpoints)
12. [Quick Reference: Key Equations](#quick-reference-key-equations)
13. [What's Next](#whats-next)

---

## Overview

### What are Diffusion Models?

A **diffusion model** is a generative model that learns the reverse of a noise-injection process. The intuition: take a real image and gradually corrupt it with Gaussian noise over many timesteps until it becomes indistinguishable from pure noise. Then train a neural network to *undo* each noising step. At inference, start from random noise and iteratively apply the learned denoising, arriving at a realistic sample.

The key mathematical insight is that if the noise added at each step is small (small β_t), the reverse step — going from slightly noisier to slightly cleaner — is also approximately Gaussian. This makes the reverse process tractable to parameterize and learn.

Diffusion models come in two equivalent formulations:
- **DDPM** (Ho et al., 2020): discrete timesteps, predict the noise ε added at each step
- **Score-based / SDE** (Song et al., 2020–2021): continuous time, learn the score function ∇_x log p(x_t)

Both are now understood to be instances of the same underlying framework.

### Why Learn Diffusion Models?

- **State of the art**: Powers Stable Diffusion, DALL·E 3, Imagen, Sora, and virtually every leading image/video/audio generative system
- **Research frontier**: Active area with rapid advances in architecture (DiT), training (flow matching), and applications (3D, video, protein folding)
- **3D generation gateway**: DreamFusion, Shap-E, and most text-to-3D methods use diffusion as their backbone — essential for the 3D generative models branch of this knowledge tree
- **Transferable framework**: The mathematical tools (SDEs, score matching, ELBO) apply across image, audio, video, molecular, and 3D data

### Advantages
- ✅ State-of-the-art sample quality and diversity
- ✅ Stable training (unlike GANs — no adversarial instability)
- ✅ Flexible conditioning (text, class, image, depth maps, etc.)
- ✅ Principled probabilistic framework with tractable likelihood bounds
- ✅ Composable — can combine conditioning signals at inference time

### Disadvantages
- ⚠️ Slow inference: standard DDPM requires 1000 sequential denoising steps
- ⚠️ High compute cost for training large models
- ⚠️ Complex math: requires understanding Markov chains, SDEs, and variational inference
- ⚠️ No single canonical architecture (U-Net vs DiT, many scheduler variants)

### Alternatives

| Model | When to Prefer |
|---|---|
| **GANs** | Need fastest inference, accept training instability |
| **VAEs** | Need fast encoder for downstream tasks, explicit latent space |
| **Flow-based** (Normalizing Flows) | Need exact likelihood, fully invertible mapping |
| **Autoregressive** (GPT, DALL·E 1) | Discrete/sequential generation (text, audio tokens) |
| **Flow Matching** | Cleaner ODE framework, now replacing DDPM in new models (SD3, Flux) |

---

## Prerequisites

### Required
- [ ] **PyTorch** — nn.Module, training loop, GPU usage, `torch.autograd`
- [ ] **Gaussian distribution** — sampling, PDF, closed-form operations
- [ ] **KL divergence** — intuition and formula
- [ ] **ELBO** — Evidence Lower Bound derivation (covered in VAE study)
- [ ] **CNNs** — convolutional layers, feature maps
- [ ] **U-Net architecture** — encoder, decoder, skip connections (essential backbone)

### Recommended
- Familiarity with VAEs and the reparameterization trick
- Basic stochastic calculus (for the SDE formulation in Phase 3)
- Transformer attention mechanism (for Phase 5 / DiT)

### Setup
```bash
pip install torch torchvision torchaudio
pip install diffusers transformers accelerate
pip install matplotlib numpy tqdm einops
# For notebooks
pip install jupyter ipywidgets
```

---

## Phase 1 — Probabilistic Foundations & the Forward Process (Week 1–2)

**Goal**: Understand the mathematical setup of diffusion — the Markov chain, noise schedules, and the closed-form forward process.

### Core Concepts

**1. The Forward Process q**

The forward process adds noise over T steps (typically T = 1000):

```
q(x_t | x_{t-1}) = N(x_t; √(1 - β_t) x_{t-1},  β_t I)
```

β_t is the **noise schedule** — a sequence of small positive values controlling how much noise is added at each step.

**Key property — closed-form sampling**: You can jump directly to any timestep t without running all intermediate steps:
```
x_t = √(ᾱ_t) · x_0  +  √(1 - ᾱ_t) · ε,    ε ~ N(0, I)

where  αt = 1 - βt  and  ᾱt = ∏_{i=1}^{t} αi
```
This is the most important equation in DDPM — it lets you sample any noisy version of x_0 in one shot.

**2. Noise Schedules**

| Schedule | Formula | Notes |
|---|---|---|
| **Linear** (original DDPM) | β_t linearly from β_1=1e-4 to β_T=0.02 | Works but suboptimal |
| **Cosine** (improved DDPM) | ᾱ_t = cos²(πt/(2T+offset)) | Better for higher resolution images |
| **Sigmoid / learned** | Various | Used in some modern models |

At t=T: ᾱ_T ≈ 0, so x_T ≈ ε (pure noise). At t=0: x_0 is the original data.

**3. Why Gaussian Noise?**

- The forward process has a **stationary distribution** of N(0, I) — all information is eventually destroyed
- Gaussians compose: the product of Gaussian kernels is Gaussian (enables the closed-form jump)
- Tractable KL divergence: D_KL between two Gaussians has a closed form

**Learning Activities**:
- [ ] ⭐ Read [Lilian Weng — What are Diffusion Models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) sections 1–2
- [ ] Derive the closed-form x_t = √(ᾱ_t)x_0 + √(1-ᾱ_t)ε yourself (it's just substituting q(x_t|x_{t-1}) recursively)
- [ ] Implement the noise scheduler in PyTorch: precompute α_t, ᾱ_t, √ᾱ_t tables
- [ ] Visualize: plot a grid showing x_0, x_200, x_500, x_800, x_1000 for a real image

**Exercise — Noise Scheduler Visualization**:
```python
# Implement and visualize the forward process
import torch, matplotlib.pyplot as plt
from PIL import Image

def make_linear_schedule(T=1000, beta_start=1e-4, beta_end=0.02):
    betas = torch.linspace(beta_start, beta_end, T)
    alphas = 1 - betas
    alpha_bars = torch.cumprod(alphas, dim=0)
    return betas, alphas, alpha_bars

def q_sample(x0, t, alpha_bars, noise=None):
    if noise is None:
        noise = torch.randn_like(x0)
    sqrt_abar = alpha_bars[t].sqrt().view(-1, 1, 1, 1)
    sqrt_one_minus_abar = (1 - alpha_bars[t]).sqrt().view(-1, 1, 1, 1)
    return sqrt_abar * x0 + sqrt_one_minus_abar * noise, noise

# Goal: visualize clean image degrading to noise
# Time: ~2 hours
```

**Checkpoint**:
- [ ] Can you derive q(x_t | x_0) in closed form from scratch?
- [ ] Can you implement the noise schedule precomputation in ~10 lines?
- [ ] Can you explain why we can jump directly to any timestep t?

---

## Phase 2 — DDPM: Training & Sampling (Week 3–4)

**Goal**: Understand the full DDPM training objective, implement a U-Net denoiser, and implement DDPM + DDIM sampling.

### Core Concepts

**1. The Reverse Process p_θ**

The ideal reverse step p(x_{t-1} | x_t) is intractable — but given x_0, the *posterior* q(x_{t-1} | x_t, x_0) *is* tractable (it's Gaussian):
```
q(x_{t-1} | x_t, x_0) = N(x_{t-1}; μ̃_t(x_t, x_0),  β̃_t I)

μ̃_t = (√ᾱ_{t-1} β_t)/(1-ᾱ_t) · x_0  +  (√α_t (1-ᾱ_{t-1}))/(1-ᾱ_t) · x_t
β̃_t = (1-ᾱ_{t-1})/(1-ᾱ_t) · β_t
```

We train p_θ(x_{t-1} | x_t) to match this posterior by learning to predict x_0 (or equivalently, the noise ε).

**2. Training Objective — Simplified**

The full ELBO simplifies (after several steps) to just:
```
L_simple = E_{t, x_0, ε} [ ||ε - ε_θ(x_t, t)||² ]
```

- Sample a random t ~ Uniform(1, T)
- Sample noise ε ~ N(0, I)
- Compute x_t = √(ᾱ_t)x_0 + √(1-ᾱ_t)ε
- Predict ε̂ = ε_θ(x_t, t)
- Loss = MSE(ε, ε̂)

This is remarkably simple: **just predict the noise that was added**.

**3. U-Net Architecture for Denoising**

The denoising network ε_θ takes (x_t, t) and returns the predicted noise. Standard design:

- **Encoder path**: series of ResBlocks + Downsample (stride-2 conv or MaxPool)
- **Bottleneck**: ResBlocks + Self-Attention
- **Decoder path**: ResBlocks + Upsample + Skip connections from encoder
- **Time embedding**: sinusoidal positional encoding of t, projected to each ResBlock via AdaGN or additive bias
- **Attention**: Multi-head self-attention at 16×16 and 8×8 resolutions

Key detail: **time embeddings must be injected at every level** — this is a common implementation mistake.

**4. DDPM Sampling (Inference)**

Starting from x_T ~ N(0, I), iteratively denoise:
```
x_{t-1} = (1/√α_t) · (x_t - (β_t/√(1-ᾱ_t)) · ε_θ(x_t, t))  +  √β̃_t · z
```
where z ~ N(0, I) for t > 1, z = 0 for t = 1.

This requires **T = 1000 sequential forward passes** through the network — slow.

**5. DDIM Sampling — Faster Inference**

DDIM (Song et al., 2020) redefines the forward process as a *non-Markovian* process with the same marginals. This allows a **deterministic** reverse ODE:
```
x_{t-1} = √ᾱ_{t-1} · x̂_0(x_t)  +  √(1-ᾱ_{t-1}) · ε_θ(x_t, t)
```
where x̂_0(x_t) = (x_t - √(1-ᾱ_t) · ε_θ(x_t, t)) / √ᾱ_t

Key advantages:
- Can use **50–250 steps** instead of 1000 (10–20× faster)
- Deterministic: same noise → same image (enables latent space interpolation)
- Same model weights — just swap the sampling loop

**Learning Activities**:
- [ ] ⭐ Read [The Annotated Diffusion Model (HuggingFace)](https://huggingface.co/blog/annotated-diffusion) — the single best hands-on resource
- [ ] Run [Annotated Diffusion Colab](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/annotated_diffusion.ipynb)
- [ ] Watch [Outlier — DDPM Math Explained](https://www.youtube.com/watch?v=HoKDTa5jHvg)
- [ ] Read the original [DDPM paper](https://arxiv.org/abs/2006.11239) — focus on Sections 2–4
- [ ] Read [DDIM paper](https://arxiv.org/abs/2010.02502) — focus on Sections 2–3

**Exercise — Train DDPM from Scratch**:
```
Dataset: MNIST (fast) or Fashion-MNIST
─────────────────────────────────────
Architecture:
  - Simple U-Net: [32, 64, 128, 256] channels, 4 resolution levels
  - Time embedding: sinusoidal, dim=256, injected via linear layer
  - ResBlocks with GroupNorm
  - Attention at 8x8 resolution only

Training:
  - T=1000, linear schedule
  - AdamW, lr=2e-4, batch=128
  - ~50k steps (~1 hour on GPU)

Evaluation:
  - Sample 64 images with DDPM (1000 steps)
  - Sample 64 images with DDIM (50 steps)
  - Compare visual quality and speed
  - Plot: training loss curve, ᾱ_t schedule

Goal: Working generative model + DDIM speedup
Time: 12–18 hours
```

**Checkpoint**:
- [ ] Can you explain why the training objective simplifies to predicting ε?
- [ ] Can you implement the training loop in ~30 lines without reference?
- [ ] Can you explain the DDIM sampling equation and why it's faster?
- [ ] Can you write the DDPM inference loop from memory?

---

## Phase 3 — Score-Based Generative Models (Week 5)

**Goal**: Understand the score-matching perspective and the SDE unification of diffusion models.

### Core Concepts

**1. The Score Function**

The **score function** of a distribution p(x) is:
```
s(x) = ∇_x log p(x)
```
It points in the direction of increasing density — toward modes of the distribution. Key insight: **you don't need the normalization constant** to compute the score.

**2. Score Matching**

Train a neural network s_θ(x) to approximate ∇_x log p(x). The naive training objective:
```
E[ ||s_θ(x) - ∇_x log p(x)||² ]
```
is intractable (we don't know log p(x)). **Denoising Score Matching** (Vincent, 2011) avoids this by instead matching the score of a *noised* distribution:
```
E_{x, x̃} [ ||s_θ(x̃, σ) - ∇_{x̃} log q_σ(x̃|x)||² ]
```
where x̃ = x + σε. This is exactly what DDPM training does — just viewed differently.

**3. SDE Formulation (Song et al., 2021)**

The continuous-time generalization: define a stochastic differential equation (SDE) for the forward process:
```
dx = f(x, t) dt  +  g(t) dw          (forward SDE)
```
The reverse SDE (Anderson, 1982) is:
```
dx = [f(x, t) - g(t)² ∇_x log p_t(x)] dt  +  g(t) dw̄
```
The term ∇_x log p_t(x) is the score function — and the DDPM denoising network learns exactly this.

This SDE framework:
- Unifies DDPM (VP-SDE), NCSN/SMLD (VE-SDE), and sub-VP-SDE under one formulation
- Enables **probability flow ODEs**: a deterministic version of the reverse process (related to DDIM)
- Opens the door to using numerical ODE/SDE solvers for sampling

**4. The Connection: DDPM = Score Matching**

The DDPM noise prediction network ε_θ(x_t, t) is related to the score by:
```
s_θ(x_t, t) = -ε_θ(x_t, t) / √(1 - ᾱ_t)
```
They are equivalent: training to predict ε is training to predict the score.

**Learning Activities**:
- [ ] ⭐ Read [Yang Song — Score-Based Generative Modeling](https://yang-song.net/blog/2021/score/)
- [ ] Read [Lilian Weng — Diffusion post](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) Section 3 (connection to score matching)
- [ ] Implement: train a simple score network on 2D toy data (spirals, moons), visualize the learned score field as vector arrows, run Langevin dynamics to sample

**Exercise — 2D Score Matching Visualization**:
```python
# Train score network on 2D data, visualize as vector field
# Data: sklearn.datasets.make_moons or make_circles
# Network: small MLP that takes (x, y, sigma) -> score (dx, dy)
# Training: denoising score matching at multiple sigma levels
# Visualize: quiver plot of ∇ log p(x), animate Langevin sampling
# Time: ~4 hours — great for building intuition
```

**Checkpoint**:
- [ ] Can you explain what the score function is and why it's useful?
- [ ] Can you explain how DDPM training is equivalent to denoising score matching?
- [ ] Can you write the SDE forward/reverse equations from memory?
- [ ] Can you explain the "probability flow ODE" and its relationship to DDIM?

---

## Phase 4 — Conditional Generation & Latent Diffusion (Week 6–7)

**Goal**: Understand how to condition diffusion models on external signals (class, text, image), and how Stable Diffusion works end-to-end.

### Core Concepts

**1. Classifier Guidance**

- Train a noisy classifier C_φ(y | x_t) — a classifier that works on noisy images at any timestep
- At inference, perturb the score toward higher probability of class y:
  ```
  ε̃_θ(x_t, t, y) = ε_θ(x_t, t) - √(1-ᾱ_t) · γ · ∇_{x_t} log C_φ(y | x_t)
  ```
- γ is the guidance scale — higher = more class-specific, less diverse
- **Limitation**: requires training a *separate noisy classifier*

**2. Classifier-Free Guidance (CFG)**

The dominant technique. Train a *single* model that handles both conditional and unconditional generation:
- During training: with probability p_uncond, drop the conditioning label/text (replace with null embedding ∅)
- At inference, extrapolate away from the unconditional prediction:
  ```
  ε̃_θ(x_t, t, c) = ε_θ(x_t, t, ∅)  +  w · (ε_θ(x_t, t, c) - ε_θ(x_t, t, ∅))
  ```
- w is the guidance scale (typically 7–9 for text-to-image)
- Each inference step requires **two forward passes**: conditional + unconditional

**CFG intuition**: The model learns "here's what makes this image belong to class c, and here's everything else." At inference, amplify the class-specific component by factor w.

**3. Text Conditioning via Cross-Attention**

How CLIP/T5 text embeddings enter the U-Net:
- Text encoder (CLIP ViT-L or T5) produces a sequence of token embeddings: shape [batch, seq_len, dim]
- In the U-Net's ResBlocks at each resolution: **cross-attention** between spatial features (queries) and text tokens (keys + values)
- ```
  Attention(Q, K, V) = softmax(QK^T / √d) · V
  Q = W_Q · h_spatial,   K = W_K · text_embed,   V = W_V · text_embed
  ```
- This lets every spatial location "attend to" relevant words in the prompt

**4. Latent Diffusion Models (Stable Diffusion)**

Pixel-space diffusion on 512×512 RGB = diffusion on a 512×512×3 tensor — expensive. The LDM solution:

1. **Train a VAE** (KL-regularized or VQ): encode 512×512×3 → 64×64×4 (8× spatial compression)
2. **Train diffusion in latent space**: ε_θ operates on 64×64×4 tensors — 64× fewer elements
3. **Inference**: sample latent z from diffusion → decode z through VAE decoder → 512×512 image

Architecture:
```
Text prompt
    ↓ CLIP Text Encoder
Text embeddings [77, 768]
    ↓ Cross-attention in U-Net

Noise z_T [64, 64, 4]
    ↓ U-Net (T denoising steps with text cross-attention)
Clean latent z_0 [64, 64, 4]
    ↓ VAE Decoder
Generated image [512, 512, 3]
```

**5. Other Conditioning Types**
- **ControlNet**: condition on depth maps, edge maps, pose, segmentation — adds a trainable copy of the U-Net encoder
- **IP-Adapter**: condition on reference images via cross-attention with CLIP image embeddings
- **Inpainting**: mask-conditioned generation by replacing unmasked regions during sampling

**Learning Activities**:
- [ ] ⭐ Watch [Umar Jamil — Coding Stable Diffusion from Scratch](https://www.youtube.com/watch?v=ZBKpAp_6TGI) — full implementation walkthrough (~5 hours)
- [ ] Read [Classifier-Free Guidance paper](https://arxiv.org/abs/2207.12598)
- [ ] Read [Latent Diffusion / Stable Diffusion paper](https://arxiv.org/abs/2112.10752) — skim, focus on Figure 3 and Section 3
- [ ] Complete [HuggingFace Diffusion Models Class](https://github.com/huggingface/diffusion-models-class) Units 3–4
- [ ] Run a HuggingFace `StableDiffusionPipeline` and experiment with guidance scale and sampling steps

**Exercise — CFG Implementation**:
```python
# Add class-conditional CFG to your DDPM from Phase 2
────────────────────────────────────────────────────
1. Modify U-Net to accept class label embedding (or null embedding)
   - Add class embedding table: nn.Embedding(num_classes + 1, time_dim)
   - Combine with time embedding via addition or concat
2. During training: with p=0.1, replace class label with null (class_id = num_classes)
3. Implement CFG sampling loop:
   - Each step: two forward passes (conditional + null)
   - Combine: eps = eps_uncond + w * (eps_cond - eps_uncond)
4. Generate grids: same noise, guidance scales w=[1, 3, 7, 15]
5. Document: quality vs diversity tradeoff

Goal: Class-conditional generation with visible CFG effect
Time: ~8 hours
```

**Checkpoint**:
- [ ] Can you implement CFG in ~10 lines given a trained conditional model?
- [ ] Can you explain why CFG needs two forward passes per step?
- [ ] Can you describe the full Stable Diffusion pipeline from prompt to pixel?
- [ ] Can you explain what ControlNet adds and how it works architecturally?

---

## Phase 5 — Modern Architectures & Advanced Topics (Week 8–10)

**Goal**: Understand cutting-edge diffusion architectures and techniques; be able to read new papers.

### Topics to Master

**1. Diffusion Transformers (DiT)**

Introduced by Peebles & Xie (2022). Replace the U-Net backbone with a **Vision Transformer**:
- Patchify input: split x_t into non-overlapping patches → token sequence
- Apply standard Transformer blocks (self-attention + MLP)
- Unpatchify output: reshape tokens back to image
- Time + class conditioning: **AdaLN-Zero** — modulate LayerNorm parameters (scale, shift) with sinusoidal time embedding

Key result: DiT-XL/2 outperforms all previous U-Net-based models on ImageNet 256×256. Now used in Stable Diffusion 3, Flux, Sora.

**2. Improved Sampling — DPM-Solvers**

DDPM: 1000 steps. DDIM: 50–250 steps. DPM-Solver++: **15–25 steps** with comparable quality.

The insight: the probability flow ODE from DDIM is a standard ODE. Use **higher-order ODE solvers** (like Runge-Kutta) instead of the first-order Euler method DDIM uses. DPM-Solver++ is now the default scheduler in many production pipelines.

**3. Flow Matching**

A cleaner alternative to DDPM training, gaining adoption in new models:
- Instead of a noising SDE, define a straight interpolation: x_t = (1-t)·x_0 + t·ε
- Train the network to predict the *vector field* (velocity) v = ε - x_0
- Training objective: L = E[||v_θ(x_t, t) - (ε - x_0)||²]
- At inference: integrate the ODE dx/dt = v_θ(x, t)

Flow matching produces straighter trajectories than DDPM → fewer integration steps, easier to train. Used in Stable Diffusion 3 (MM-DiT), Flux, and Lumina.

**4. Consistency Models**

Goal: single-step (or few-step) generation without distillation quality loss.

Key idea: train the model to predict x_0 directly from any x_t along a diffusion trajectory (self-consistency). Can be trained from scratch (consistency training) or distilled from a pre-trained diffusion model (consistency distillation). Enables 1–3 step generation.

**5. SDXL and Multi-Scale Conditioning**

SDXL adds:
- Larger U-Net (2.6B params), dual text encoders (CLIP ViT-L + OpenCLIP ViT-bigG)
- Multi-aspect training with original resolution conditioning
- Separate refinement model for upscaling/detail
- Micro-conditioning: original image size, crop coordinates as conditioning signals

**6. Video Diffusion**

Extension to temporal dimension:
- Add temporal attention layers between spatial attention layers
- 3D U-Net or DiT with temporal attention
- Key papers: Video Diffusion Models (Ho et al.), Imagen Video, Stable Video Diffusion, Sora (DiT-based)

**Learning Activities**:
- [ ] Read [DiT paper](https://arxiv.org/abs/2212.09748) — short, clear, important
- [ ] Read [Flow Matching paper](https://arxiv.org/abs/2210.02747)
- [ ] Complete [HuggingFace Diffusion Models Class](https://github.com/huggingface/diffusion-models-class) Unit 4 (fine-tuning, DreamBooth)
- [ ] Read [fast.ai Part 2 Lessons 9–10](https://course.fast.ai/) for practitioner perspective on Stable Diffusion internals
- [ ] Experiment: swap schedulers in a HuggingFace pipeline (PNDM → DPM-Solver++ → Euler), compare quality at 20/50 steps

**Exercise — Fine-tune with DreamBooth or LoRA**:
```
Fine-tune Stable Diffusion on a small custom dataset
──────────────────────────────────────────────────
1. Collect 10-20 images of a subject (your photos or a specific concept)
2. Use HuggingFace Diffusers + Accelerate:
   - DreamBooth: full fine-tune with prior preservation loss (needs 24GB VRAM)
   - LoRA: low-rank adaptation (works on 8GB VRAM, recommended)
3. Generate subject in diverse styles and contexts
4. Document: compare 20-step DPM-Solver++ vs 50-step DDIM on your fine-tuned model

Extension: implement ControlNet inference via HuggingFace pipeline
Time: 8-12 hours (LoRA approach)
```

**Checkpoint**:
- [ ] Can you explain the DiT architecture (patchify → transformer → unpatchify + AdaLN)?
- [ ] Can you describe flow matching and how it differs from DDPM?
- [ ] Can you swap schedulers in HuggingFace and compare 20-step vs 50-step quality?
- [ ] Can you read a new diffusion paper (e.g., Flux, SD3) and identify its key contributions?

---

## Curated Resources

### Foundation

| Resource | Format | Level |
|---|---|---|
| ⭐ [Lilian Weng — What are Diffusion Models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) | Article | Int |
| ⭐ [Annotated Diffusion Model (HuggingFace)](https://huggingface.co/blog/annotated-diffusion) | Article+Code | Int |
| [Yang Song — Score-Based Generative Modeling](https://yang-song.net/blog/2021/score/) | Article | Int-Adv |
| [fast.ai Part 2 — Lesson 9](https://course.fast.ai/Lessons/lesson9.html) | Video | Int |

### Videos

| Resource | Duration | Level |
|---|---|---|
| ⭐ [Umar Jamil — Stable Diffusion from Scratch in PyTorch](https://www.youtube.com/watch?v=ZBKpAp_6TGI) | ~5h | Int |
| ⭐ [Outlier — DDPM Paper Explanation + Math](https://www.youtube.com/watch?v=HoKDTa5jHvg) | ~1h | Int |
| [MIT 6.S191 — Deep Generative Modeling](https://www.youtube.com/watch?v=3G5hWM6jqPk) | ~1h | Beg |

### Courses

| Resource | Format | Notes |
|---|---|---|
| ⭐ [HuggingFace Diffusion Models Class](https://github.com/huggingface/diffusion-models-class) | 4-unit course + notebooks | Free, structured, hands-on |
| [fast.ai Part 2](https://course.fast.ai/) | Video course | Deep practitioner dive into SD internals |

### Papers (read in this order)

| Paper | Why |
|---|---|
| ⭐ [DDPM — Ho et al. 2020](https://arxiv.org/abs/2006.11239) | The foundational paper |
| ⭐ [DDIM — Song et al. 2020](https://arxiv.org/abs/2010.02502) | Fast sampling |
| [Score-based — Song & Ermon 2019](https://arxiv.org/abs/1907.05600) | Score-matching perspective |
| [Latent Diffusion (SD) — Rombach et al. 2022](https://arxiv.org/abs/2112.10752) | How Stable Diffusion works |
| ⭐ [Classifier-Free Guidance — Ho & Salimans 2022](https://arxiv.org/abs/2207.12598) | Required for conditional generation |
| [DiT — Peebles & Xie 2022](https://arxiv.org/abs/2212.09748) | Modern transformer-based backbone |
| [Flow Matching — Lipman et al. 2022](https://arxiv.org/abs/2210.02747) | Replacing DDPM in new models |

### Code & Libraries

| Resource | Notes |
|---|---|
| ⭐ [HuggingFace Diffusers](https://huggingface.co/docs/diffusers/index) | Standard library — learn its API |
| [Annotated Diffusion Colab](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/annotated_diffusion.ipynb) | Run it line by line |
| [CompVis Latent Diffusion repo](https://github.com/CompVis/latent-diffusion) | Original SD codebase |
| [Keras DDPM example](https://keras.io/examples/generative/ddpm/) | Clean minimal implementation |

---

## Practical Projects

### Project 1: Forward Process Visualizer
**Level**: Beginner | **Time**: 2–3 hours

Implement the noise scheduler and visualize the forward process on real images.

- Plot: x_0, x_{200}, x_{400}, x_{600}, x_{800}, x_{1000} for multiple images
- Plot: the ᾱ_t schedule (linear vs cosine) side by side
- Plot: signal-to-noise ratio SNR(t) = ᾱ_t / (1 - ᾱ_t) on log scale

**Insight gained**: Intuition for how information is destroyed and at what rate.

---

### Project 2: DDPM on MNIST
**Level**: Intermediate | **Time**: 12–18 hours

Train a full DDPM from scratch and implement both DDPM and DDIM sampling.

- U-Net with time embeddings (~5M params)
- Train on MNIST or Fashion-MNIST
- Compare DDPM (1000 steps) vs DDIM (50, 100, 250 steps) — quality vs speed table
- Bonus: DDIM latent interpolation between two images

**Insight gained**: Full pipeline understanding, DDIM mechanics.

---

### Project 3: Class-Conditional Generation with CFG
**Level**: Intermediate | **Time**: 8–12 hours

Extend Project 2 with classifier-free guidance on CIFAR-10.

- Conditional U-Net with class embedding
- Training with random label dropout (p_uncond = 0.1)
- Generate grids: same seed, labels 0–9, guidance w=1/3/7/15
- FID comparison: unconditional vs guided

**Insight gained**: CFG mechanics, guidance scale tradeoffs, conditional generation.

---

### Project 4: Use Stable Diffusion via Diffusers
**Level**: Intermediate | **Time**: 4–6 hours

Explore the production pipeline through the HuggingFace API.

- Run `StableDiffusionPipeline` for text-to-image
- Swap schedulers: compare DDIM, DPM-Solver++, Euler at 20 steps
- Explore img2img pipeline (noise and denoise an existing image)
- Run ControlNet pipeline with depth map or edge map conditioning

**Insight gained**: Production API proficiency, scheduler differences.

---

### Project 5: Fine-tune with LoRA
**Level**: Advanced | **Time**: 10–16 hours

Fine-tune Stable Diffusion on a custom concept using LoRA.

- Collect 15–20 images of a subject
- Set up training with HuggingFace Diffusers + PEFT
- Train LoRA adapters on U-Net cross-attention layers
- Generate subject in different styles, backgrounds, and compositions

**Insight gained**: Fine-tuning mechanics, LoRA, practical deployment considerations.

---

## Common Pitfalls

### Forgetting to Normalize Input to [-1, 1]
**Why**: Diffusion assumes a standard Gaussian prior N(0,I). If your data is in [0,1], the SNR at x_T won't be ~0 and the model learns a wrong distribution.
**Fix**: Always `x = 2*x - 1` before entering the diffusion process; undo with `x = (x + 1) / 2` after.

### Time Embedding Not Injected at Every Level
**Symptom**: Model generates blurry noise regardless of step; loss stagnates.
**Fix**: Verify `time_emb` is added (via linear projection + addition) inside *every* ResBlock in encoder and decoder.

### Guidance Scale Too High
**Symptom**: Oversaturated, artifact-heavy images; "crayon drawing" look.
**Why**: Extrapolating too far from the unconditional score overshoots the data manifold.
**Fix**: w=7–9 is typical for SD. Use dynamic thresholding (Imagen) or rescale guidance for very high w.

### Evaluating Only on Loss, Not on Samples
**Why**: Training loss measures noise prediction accuracy but doesn't directly reflect perceptual quality or diversity.
**Fix**: Visually inspect samples every N steps during training. Use FID for quantitative evaluation.

### DDIM Gives Different Results Than DDPM
**This is correct**: DDPM sampling is stochastic (adds noise at each step); DDIM is deterministic by default. They should produce different images from the same x_T.
**Note**: DDIM with η=1 recovers stochastic sampling (equivalent to DDPM).

### Training Loss Doesn't Decrease
**Common causes**:
- Learning rate too high (try 1e-4 or 2e-4 with AdamW)
- Time embeddings not added to ResBlocks
- GroupNorm groups incompatible with channel count (channels must be divisible by num_groups, typically 32)
- Batch size too small (use ≥64 if memory allows)

---

## Assessment Checkpoints

### After Phase 1 (Forward Process)
- [ ] Derive q(x_t | x_0) in closed form
- [ ] Implement `q_sample(x0, t)` in 5 lines of PyTorch
- [ ] Explain linear vs cosine schedules and when each is preferred
- [ ] Visualize the forward process and describe what happens to the signal

### After Phase 2 (DDPM)
- [ ] Implement the full training loop in ~25 lines
- [ ] Implement DDPM sampling loop in ~15 lines
- [ ] Implement DDIM sampling loop in ~15 lines
- [ ] Explain why the training objective simplifies to predicting ε
- [ ] Run both sampling methods and document the speed/quality tradeoff

### After Phase 3 (Score Matching)
- [ ] Explain the score function and why it doesn't need the normalization constant
- [ ] Explain how DDPM training = denoising score matching (show the equivalence)
- [ ] Write the forward and reverse SDE equations from memory
- [ ] Visualize a learned score field on 2D toy data

### After Phase 4 (Conditional Generation)
- [ ] Implement CFG in ~10 lines
- [ ] Describe the full SD pipeline (VAE → U-Net + CLIP → VAE decoder)
- [ ] Explain how cross-attention enables text conditioning
- [ ] Experiment with guidance scale and document the tradeoff

### Final Mastery Check
- [ ] Read a new diffusion paper (e.g., Flux, SD3, DiT) and summarize the key contributions
- [ ] Fine-tune a diffusion model on custom data using LoRA
- [ ] Swap schedulers in HuggingFace and explain the tradeoffs (DDIM vs DPM-Solver++ vs Euler)
- [ ] Explain what flow matching is and why it's replacing DDPM
- [ ] Connect diffusion models to the 3D generation branch: explain how DreamFusion uses diffusion as a prior for NeRF optimization

---

## Quick Reference: Key Equations

```
FORWARD PROCESS
───────────────
q(x_t | x_{t-1}) = N(x_t; √(1-β_t) x_{t-1},  β_t I)

Closed form (most important):
  x_t = √ᾱ_t · x_0  +  √(1-ᾱ_t) · ε,    ε ~ N(0, I)
  where  αt = 1-βt,   ᾱt = ∏αi

REVERSE POSTERIOR (tractable given x_0)
──────────────────────────────────────
q(x_{t-1} | x_t, x_0) = N(μ̃_t, β̃_t I)
μ̃_t = (√ᾱ_{t-1} βt)/(1-ᾱt) · x_0  +  (√αt (1-ᾱ_{t-1}))/(1-ᾱt) · x_t
β̃_t = (1-ᾱ_{t-1})/(1-ᾱt) · βt

TRAINING OBJECTIVE (simplified ELBO)
─────────────────────────────────────
L = E_{t, x_0, ε} [ ||ε - ε_θ(√ᾱt·x_0 + √(1-ᾱt)·ε,  t)||² ]

DDPM SAMPLING
─────────────
x_{t-1} = 1/√αt · (x_t - βt/√(1-ᾱt) · ε_θ(x_t, t))  +  √β̃t · z

DDIM SAMPLING (deterministic)
──────────────────────────────
x̂_0 = (x_t - √(1-ᾱt)·ε_θ(x_t,t)) / √ᾱt
x_{t-1} = √ᾱ_{t-1}·x̂_0  +  √(1-ᾱ_{t-1})·ε_θ(x_t,t)

CLASSIFIER-FREE GUIDANCE
─────────────────────────
ε̃ = ε_θ(x_t, ∅)  +  w·(ε_θ(x_t, c) - ε_θ(x_t, ∅))

SCORE FUNCTION CONNECTION
──────────────────────────
s_θ(x_t, t) = -ε_θ(x_t, t) / √(1-ᾱt)
```

---

## What's Next

### Directly from this knowledge tree
- **[3D Diffusion Models](../../../Computer-Graphics/3D-Generative-Models/3D-Diffusion-Models/)** — apply everything here to 3D: point clouds, meshes, SDFs
- **[Text to 3D Models](../../../Computer-Graphics/3D-Generative-Models/Text-to-3D/)** — DreamFusion (uses diffusion as prior for NeRF), Shap-E (diffusion over implicit functions)
- **[NeRF](../../../Computer-Graphics/Neural-Rendering/NeRF/)** — understand the representation that diffusion priors optimize over in DreamFusion

### Advanced Research Directions
- **Consistency Models** (Song et al., 2023) — single-step generation
- **Flow Matching** (Lipman et al., 2022) — the framework replacing DDPM
- **Rectified Flow** (Liu et al., 2022) — straight-path ODE flows, used in Flux
- **DiT variants** — Sora (video DiT), SD3 (MM-DiT), Flux
- **Diffusion for 3D**: DreamFusion, SJC, Magic3D, Prolific Dreamer

### Staying Current
- **Lilian Weng's blog** ([lilianweng.github.io](https://lilianweng.github.io)) — authoritative summaries of new techniques
- **Yannic Kilcher YouTube** — paper walkthroughs for major releases
- **HuggingFace blog** — practical techniques and model releases
- **arXiv cs.CV / cs.LG** — follow: Yang Song, Jonathan Ho, Robin Rombach, Tim Brooks, Bill Peebles
- **r/StableDiffusion**, **r/MachineLearning** — community experiments and practical findings

---

**Difficulty**: ⭐⭐⭐⭐ — mathematically demanding; the reward is understanding the foundations of modern generative AI
**Estimated time**: 8–10 weeks part-time
**Most critical resource**: [Annotated Diffusion Model](https://huggingface.co/blog/annotated-diffusion) — read it, run it, understand every line
**Last updated**: 2026-03-16



https://diffusion.csail.mit.edu/2026/index.html
