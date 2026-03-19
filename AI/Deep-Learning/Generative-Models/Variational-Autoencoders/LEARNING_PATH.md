# Learning Path: Variational Autoencoders (VAE)

> **Context in the knowledge tree**: VAE sits under Generative Models → alongside Diffusion Models and GANs. Understanding VAEs is also a prerequisite for Latent Diffusion (Stable Diffusion uses a VAE as its image encoder/decoder). If you plan to study diffusion models next, complete this guide first.

**Estimated total time**: 4–5 weeks part-time (8–10 hrs/week)
**Target level**: Intermediate (assumes Python, PyTorch basics, neural networks, basic probability)
**Last updated**: 2026-03-16

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1 — Autoencoders & Representation Learning](#phase-1--autoencoders--representation-learning-week-1)
4. [Phase 2 — Variational Inference & the ELBO](#phase-2--variational-inference--the-elbo-week-2)
5. [Phase 3 — VAE: Architecture & Training](#phase-3--vae-architecture--training-week-3)
6. [Phase 4 — Variants & Applications](#phase-4--variants--applications-week-45)
7. [Curated Resources](#curated-resources)
8. [Practical Projects](#practical-projects)
9. [Common Pitfalls](#common-pitfalls)
10. [Assessment Checkpoints](#assessment-checkpoints)
11. [Quick Reference: Key Equations](#quick-reference-key-equations)
12. [What's Next](#whats-next)

---

## Overview

### What is a VAE?

A **Variational Autoencoder** is a generative model that learns to encode data into a structured probabilistic latent space, then decode samples from that space back into data. Unlike a standard autoencoder — which maps each input to a single fixed point in latent space — a VAE maps each input to a *distribution* (typically a Gaussian parameterized by mean μ and variance σ²). This probabilistic structure, enforced via a KL divergence regularization term, makes the latent space continuous and well-organized: you can sample any point and decode a meaningful output.

The training objective is the **Evidence Lower Bound (ELBO)**, a principled derivation from Bayesian variational inference:
```
ELBO = E[log p(x|z)]  −  KL(q(z|x) || p(z))
     = reconstruction_quality  −  latent_regularization
```

Maximizing the ELBO pushes the model to both reconstruct inputs faithfully and keep the latent distribution close to a standard Gaussian prior.

### Why Learn VAEs?

- **Generative modeling foundation**: VAEs are the clearest introduction to the probabilistic generative modeling framework — the same concepts (latent variables, ELBO, variational inference) appear in flow-based models, diffusion models, and beyond
- **Latent Diffusion prerequisite**: Stable Diffusion's VAE (`AutoencoderKL`) compresses images into the latent space where diffusion runs — understanding this component deeply unlocks the full SD architecture
- **Disentangled representations**: β-VAE and its descendants are the primary framework for learning human-interpretable latent factors (e.g., independently controllable pose, lighting, color)
- **Downstream use**: Encoders trained as VAEs produce continuous, interpolatable embeddings usable for retrieval, clustering, and downstream generation tasks

### When to Use a VAE

- You need a **continuous, structured latent space** you can sample from, interpolate through, or manipulate
- You want **controllable generation** with interpretable latent dimensions (β-VAE, CVAE)
- You need an encoder that produces **uncertainty estimates** (probabilistic encoder)
- You are building a **latent diffusion system** (VAE as the compression stage)
- You need **anomaly detection** (high reconstruction error + high KL → out-of-distribution)

### When NOT to Use a VAE

- You need **maximum sample sharpness** — VAEs tend toward blurry outputs due to MSE/pixel-wise reconstruction; use GAN or diffusion for sharp images
- You only need **reconstruction** (no generation needed) — a standard deterministic autoencoder is simpler
- You need **exact likelihood** — VAEs provide a lower bound; use normalizing flows for exact log-likelihood

### Advantages
- ✅ Stable, easy to train (no adversarial dynamics)
- ✅ Principled probabilistic framework with tractable training
- ✅ Continuous latent space → smooth interpolation
- ✅ Encoders produce meaningful, generalizable representations
- ✅ Foundation for understanding all latent variable generative models

### Disadvantages
- ⚠️ Blurry samples due to reconstruction loss averaging
- ⚠️ Posterior collapse: encoder can learn to ignore the input
- ⚠️ ELBO is a lower bound — exact log p(x) remains intractable
- ⚠️ KL weighting (β) requires tuning per dataset

### Alternatives

| Model | When to Prefer |
|---|---|
| **Standard Autoencoder** | Only need compression/reconstruction, no generation |
| **GAN** | Need sharp, high-fidelity samples; willing to deal with training instability |
| **Normalizing Flow** | Need exact likelihood or perfectly invertible mapping |
| **Diffusion Model** | State-of-the-art generation quality; slower inference |
| **VQ-VAE** | Need discrete latent codes (for autoregressive modeling on top) |

---

## Prerequisites

### Required
- [ ] **Python & PyTorch** — `nn.Module`, `nn.Linear`, `nn.Conv2d`, `nn.ConvTranspose2d`, training loop
- [ ] **Neural networks** — forward pass, backpropagation, loss functions, optimizers
- [ ] **Gaussian distribution** — mean, variance, sampling, PDF shape
- [ ] **Basic probability** — conditional probability P(A|B), Bayes' theorem, expectation E[X]
- [ ] **Calculus** — partial derivatives, chain rule

### Recommended
- Basic information theory (entropy, KL divergence concept)
- Familiarity with CNNs (for image VAEs)
- Basic linear algebra (matrix operations, vector spaces)

### Setup
```bash
pip install torch torchvision
pip install matplotlib numpy tqdm
pip install scikit-learn  # for t-SNE visualization
pip install jupyter       # optional
```

---

## Phase 1 — Autoencoders & Representation Learning (Week 1)

**Goal**: Build intuition for the encoder-decoder structure and understand why deterministic autoencoders fail as generative models. This phase sets up the *motivation* for the probabilistic extension.

### Topics to Master

**1. Standard Autoencoder (AE)**

Architecture:
- **Encoder** f_φ: x → z (deterministic, typically a bottleneck MLP or CNN)
- **Decoder** g_θ: z → x̂ (mirrors the encoder)
- Loss: reconstruction loss only — L = ||x - x̂||² (MSE) or BCE

What it learns: a compressed representation z that retains the information needed to reconstruct x. The bottleneck forces the network to discard noise and keep only essential structure.

**2. The Latent Space Problem**

Build and train an AE on MNIST. Encode the test set, plot the 2D latent codes colored by digit class. Observe:
- Clusters form (digits are separated)
- But the space *between* clusters is empty and unstructured

Now try: sample a random point z between two clusters. Decode it. The output is garbage.

**Why**: There is no constraint forcing the latent space to be dense or continuous. The encoder learns a mapping that only works for the specific points it's seen — arbitrary interpolation fails.

**3. The Fix: Learn a Distribution, Not a Point**

The VAE insight: instead of mapping x → z (a point), map x → (μ, σ) (parameters of a distribution). Then sample z ~ N(μ, σ²) and decode.

Add a regularization term that pushes every encoding distribution toward a shared prior N(0, I). Now the latent space is filled in: every point near the origin corresponds to a valid decoded output.

**Learning Activities**:
- [ ] Implement a simple MLP autoencoder on MNIST (encoder: 784→256→2, decoder: 2→256→784)
- [ ] Plot the 2D latent space: scatter plot colored by digit class
- [ ] Sample random 2D points from the unit square, decode them — observe the "gaps"
- [ ] Watch [MIT 6.S191 — Deep Generative Modeling](https://www.youtube.com/watch?v=3G5hWM6jqPk) (first 30 min, AE→VAE motivation)

**Exercise — AE Latent Space Exploration**:
```python
import torch, torch.nn as nn
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 256), nn.ReLU(),
            nn.Linear(256, 2)   # 2D for visualization
        )
    def forward(self, x):
        return self.net(x.view(-1, 784))

class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 256), nn.ReLU(),
            nn.Linear(256, 784), nn.Sigmoid()
        )
    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)

# Train with MSE loss, then:
# 1. Plot 2D latent space of test set (plt.scatter)
# 2. Sample grid of z values from [-3,3]x[-3,3], decode each
# Goal: observe that AE latent space has "dead zones"
# Time: ~2 hours
```

**Checkpoint**:
- [ ] Can you explain why a standard AE's latent space is problematic for generation?
- [ ] Can you implement and train a basic AE in PyTorch?
- [ ] Can you visualize the 2D latent space and identify the cluster gaps?

---

## Phase 2 — Variational Inference & the ELBO (Week 2)

**Goal**: Understand the mathematical framework behind VAEs — why we maximize the ELBO, what KL divergence measures, and why the reparameterization trick is necessary.

### Topics to Master

**1. The Generative Model**

We want to model the data distribution p(x) using a latent variable z:
```
p(x) = ∫ p(x|z) p(z) dz
```
- Prior: p(z) = N(0, I) — we choose this
- Likelihood: p(x|z) = Decoder(z) — this is learned
- Problem: the integral is intractable for deep networks

**2. Variational Inference**

Since we can't compute p(z|x) exactly (posterior is intractable), we *approximate* it with a learned distribution q_φ(z|x) = N(μ_φ(x), σ²_φ(x)):

This is the **encoder**. Its job is not to find the single best z for each x, but to approximate the posterior distribution over z given x.

**3. The ELBO Derivation**

Starting from log p(x):
```
log p(x) = E_q[log p(x|z)]  −  KL(q(z|x) || p(z))  +  KL(q(z|x) || p(z|x))
                                                           ≥ 0 (always)
```
Since the last term is ≥ 0:
```
log p(x)  ≥  E_q[log p(x|z)]  −  KL(q(z|x) || p(z))
          =  ELBO
```

Maximizing ELBO maximizes a lower bound on log p(x). The two terms have clear interpretations:
- **Reconstruction term** E_q[log p(x|z)]: the encoder should produce z values from which the decoder can reconstruct x well
- **KL term** KL(q(z|x) || p(z)): the encoder distribution should not deviate too far from the prior N(0, I)

**4. KL Divergence Between Two Gaussians**

For q = N(μ, σ²) and p = N(0, 1), the KL has a closed form:
```
KL(q || p) = -½ · Σ(1 + log(σ²) - μ² - σ²)
```
This is summed over all latent dimensions. This formula is used directly in the VAE loss — no Monte Carlo approximation needed for the KL term.

**5. The Reparameterization Trick**

Problem: we need to backpropagate through z ~ N(μ, σ²), but sampling is not differentiable.

Solution: express sampling as a deterministic transformation of a fixed noise source:
```
z = μ  +  σ · ε,    ε ~ N(0, I)    (sample ε first, then compute z)
```
Now gradients flow through μ and σ (deterministic), and ε is just a fixed input. This is **the key technical contribution** of the VAE paper.

**Learning Activities**:
- [ ] ⭐ Read [Lilian Weng — From Autoencoder to Beta-VAE](https://lilianweng.github.io/posts/2018-08-12-vae/) — Sections 1–3
- [ ] ⭐ Watch [Arxiv Insights — Variational Autoencoders](https://www.youtube.com/watch?v=9zKuYvjFFS8) (~30 min) — the best visual explanation
- [ ] Read [Jeremy Jordan — Variational Autoencoders](https://www.jeremyjordan.me/variational-autoencoders/) — clear beginner-friendly walkthrough
- [ ] Derive the closed-form KL formula yourself: start from the definition D_KL(q||p) = E_q[log q - log p], substitute the Gaussian PDFs, and simplify
- [ ] Implement the reparameterization trick in isolation:
  ```python
  def reparameterize(mu, log_var):
      std = torch.exp(0.5 * log_var)
      eps = torch.randn_like(std)    # sample from N(0,I)
      return mu + eps * std           # z is differentiable w.r.t. mu, std
  ```

**Checkpoint**:
- [ ] Can you derive the ELBO from log p(x) using Jensen's inequality?
- [ ] Can you explain what the KL term "does" during training?
- [ ] Can you compute KL(N(μ, σ²) || N(0,1)) with the closed-form formula?
- [ ] Can you explain *why* the reparameterization trick works?
- [ ] Can you implement `reparameterize()` from memory?

---

## Phase 3 — VAE: Architecture & Training (Week 3)

**Goal**: Implement a complete VAE from scratch. Understand the architecture choices, the full training loop, and the resulting latent space.

### Topics to Master

**1. VAE Architecture**

```
Input x
   ↓ Encoder
(μ, log σ²)          ← two separate linear heads
   ↓ Reparameterize
z = μ + σ·ε           ← differentiable
   ↓ Decoder
x̂ (reconstructed)
```

Key design decisions:
- **Shared encoder body**: the encoder CNN/MLP computes shared features, then two separate linear layers produce μ and log_var
- **log σ²** is predicted (not σ directly) because it can be any real number — no positivity constraint needed
- **Decoder**: can be symmetric to encoder. Final activation: sigmoid for binary (MNIST), or linear + clamp for continuous images

**2. VAE Loss Function**

```python
def vae_loss(x, x_recon, mu, log_var, beta=1.0):
    # Reconstruction: pixel-wise BCE (for binary images) or MSE
    recon_loss = F.binary_cross_entropy(x_recon, x, reduction='sum')

    # KL divergence (closed form, per-dimension sum)
    kl_loss = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())

    return recon_loss + beta * kl_loss
```

**Critical detail**: use `reduction='sum'` not `'mean'` for the reconstruction loss. The KL term sums over all dimensions, so the reconstruction must also sum (not average) over pixels for the balance to be correct.

**3. Latent Space Visualization**

After training, encode the test set and plot:
- **2D scatter**: if latent_dim=2, plot (μ₁, μ₂) colored by class → should show smooth, overlapping clusters centered near origin
- **t-SNE**: for higher-dim latent, reduce to 2D with t-SNE before plotting
- **Interpolation**: pick two test images A and B, encode to z_A and z_B, linearly interpolate z = (1-t)·z_A + t·z_B for t ∈ [0,1], decode each
- **Random sampling**: sample z ~ N(0, I) and decode → should produce realistic samples

**4. Effect of β (KL Weight)**

The β controls the tradeoff:
- **β too small** (→ 0): KL is ignored, model becomes a standard AE. Sharp reconstructions but random samples are garbage.
- **β = 1**: standard VAE
- **β > 1** (β-VAE): stronger regularization, more disentangled latent space, but blurrier reconstructions

**5. Convolutional VAE (for images)**

For images larger than MNIST, replace MLP with CNN:
```python
# Encoder
Conv2d(1, 32, 4, stride=2)  → ReLU
Conv2d(32, 64, 4, stride=2) → ReLU
Flatten
Linear(64*5*5, latent_dim*2)  # → [mu | log_var]

# Decoder (mirror)
Linear(latent_dim, 64*5*5)
Reshape to [64, 5, 5]
ConvTranspose2d(64, 32, 4, stride=2) → ReLU
ConvTranspose2d(32, 1, 4, stride=2)  → Sigmoid
```

**Learning Activities**:
- [ ] ⭐ Implement a complete VAE on MNIST from scratch (MLP or CNN encoder/decoder)
- [ ] Use [Keras VAE example](https://keras.io/examples/generative/vae/) or [PyTorch official example](https://github.com/pytorch/examples/tree/main/vae) as reference — but write it yourself first
- [ ] Produce the four visualizations: scatter, interpolation strip, random samples, reconstruction comparison
- [ ] Run with β ∈ {0.1, 1, 4} — document the change in reconstruction quality and latent space structure

**Exercise — Full VAE on MNIST**:
```python
import torch, torch.nn as nn, torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class VAE(nn.Module):
    def __init__(self, latent_dim=2):
        super().__init__()
        # Encoder
        self.encoder = nn.Sequential(nn.Linear(784, 400), nn.ReLU())
        self.mu_head = nn.Linear(400, latent_dim)
        self.logvar_head = nn.Linear(400, latent_dim)
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 400), nn.ReLU(),
            nn.Linear(400, 784), nn.Sigmoid()
        )

    def encode(self, x):
        h = self.encoder(x.view(-1, 784))
        return self.mu_head(h), self.logvar_head(h)

    def reparameterize(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        return mu + std * torch.randn_like(std)

    def decode(self, z):
        return self.decoder(z).view(-1, 1, 28, 28)

    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        return self.decode(z), mu, log_var

def loss_fn(x_recon, x, mu, log_var, beta=1.0):
    recon = F.binary_cross_entropy(x_recon, x, reduction='sum')
    kl = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
    return recon + beta * kl

# Train: AdamW, lr=1e-3, batch=128, ~20 epochs
# Visualize: latent scatter, interpolation, random samples
# Goal: smooth latent space, meaningful interpolations
# Time: ~5 hours
```

**Checkpoint**:
- [ ] Can you implement a complete VAE in PyTorch without reference?
- [ ] Can you explain why `reduction='sum'` matters for the reconstruction loss?
- [ ] Can you produce a smooth latent space interpolation between two digits?
- [ ] Can you explain what changes when you increase β?
- [ ] Can you generate new samples by sampling z ~ N(0,I)?

---

## Phase 4 — Variants & Applications (Week 4–5)

**Goal**: Understand the key VAE variants, connect VAE to modern systems (Stable Diffusion), and build a real application.

### Topics to Master

**1. β-VAE: Disentangled Representations**

Higgins et al. (2017) showed that using β > 1 encourages the latent space to be **disentangled**: individual latent dimensions correspond to independent, interpretable factors of variation (e.g., one dimension for rotation, one for scale, one for color).

Intuition: high β forces the encoder to compress information more aggressively into the prior N(0,I). To satisfy this constraint while still being useful for reconstruction, the model is encouraged to use each dimension for a single independent factor.

Evaluation: the **β-VAE disentanglement metric** — train a simple linear classifier to predict ground-truth factors from latent codes; higher accuracy → more disentangled.

Read: [β-VAE paper (Higgins et al., 2017)](https://openreview.net/forum?id=Sy2fchgBb)

**2. Conditional VAE (CVAE)**

Condition both the encoder and decoder on a label y:
- Encoder: q_φ(z|x, y) — encode x given its label
- Decoder: p_θ(x|z, y) — decode z into the correct class

Implementation: concatenate the label embedding to the encoder input and to z before decoding.

Use case: generate samples of a *specific* class (e.g., generate the digit "7" by conditioning on y=7).

**3. VQ-VAE: Vector Quantized VAE**

Van den Oord et al. (2017). Replace the continuous Gaussian latent with a **discrete codebook**:
- Encoder output is projected to the nearest vector in a learned codebook of K embeddings
- Quantized vector (closest codebook entry) is passed to the decoder
- Training trick: straight-through estimator for gradients through the discrete lookup

Why this matters:
- Discrete latents are natural for language models and autoregressive generation (DALL·E 1 used VQ-VAE + GPT)
- No KL term needed — uses commitment loss and codebook loss instead
- Enables hierarchical generation (VQ-VAE-2)

Read: [VQ-VAE paper](https://arxiv.org/abs/1711.00937)

**4. VAE in Stable Diffusion (AutoencoderKL)**

The VAE in Latent Diffusion / Stable Diffusion:
- Architecture: large CNN encoder-decoder (similar to a deep U-Net without skip connections)
- Trained with KL regularization (weak, small β) → approximate Gaussian latent
- Also trained with a perceptual loss (LPIPS) and adversarial discriminator loss → sharp reconstructions
- At inference: encoder is not needed (start from noise in latent space); only the decoder runs

The latent space is 64×64×4 for a 512×512×3 image (8× spatial downscaling, 4 channels). The diffusion U-Net operates entirely in this compressed space.

```python
from diffusers import AutoencoderKL
import torch

vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")
vae.eval()

# Encode an image to latent
latent = vae.encode(image_tensor).latent_dist.sample() * 0.18215

# Decode latent back to pixel space
reconstructed = vae.decode(latent / 0.18215).sample
```

Read: [HuggingFace AutoencoderKL docs](https://huggingface.co/docs/diffusers/api/models/autoencoderkl)

**5. Anomaly Detection with VAEs**

A trained VAE assigns high reconstruction error and high KL divergence to out-of-distribution inputs. This makes it a natural anomaly detector:
- Score: L_anomaly(x) = reconstruction_loss(x) + KL(q(z|x) || p(z))
- In-distribution x: both terms are low
- Anomalous x: high reconstruction error and/or the encoder can't find a good posterior

Application areas: industrial defect detection, medical imaging, fraud detection.

**Learning Activities**:
- [ ] Read [Lilian Weng — VAE blog](https://lilianweng.github.io/posts/2018-08-12-vae/) Sections 4–6 (β-VAE, VQ-VAE, CVAE)
- [ ] Implement a CVAE on MNIST: condition on digit label, generate specific digits
- [ ] Run the HuggingFace `AutoencoderKL` on real images: encode → inspect latent → decode
- [ ] Watch [Umar Jamil — VAE in PyTorch](https://www.youtube.com/watch?v=iwEzwTTalbg) for a code walkthrough
- [ ] Read [VQ-VAE paper](https://arxiv.org/abs/1711.00937) — focus on Section 3 (architecture) and the straight-through estimator

**Exercise — CVAE with Controlled Generation**:
```python
# Extend your VAE to condition on digit class
──────────────────────────────────────────
1. Add label embedding: nn.Embedding(10, label_dim)
2. Encoder: concatenate label_embed to input → encode
3. Decoder: concatenate label_embed to z → decode
4. At inference:
   - Sample z ~ N(0, I)
   - Choose any label y (e.g., y=7)
   - Decode (z, y_embed) → should generate a "7"
5. Produce a 10×10 grid: each row = one digit class,
   each column = different random z sample
   → should show class-specific generation

Extension: train on CelebA with attributes as conditioning
Goal: controlled, class-specific image generation
Time: ~6 hours
```

**Checkpoint**:
- [ ] Can you explain what disentanglement means and how β-VAE achieves it?
- [ ] Can you implement a CVAE with class conditioning?
- [ ] Can you explain the VQ-VAE quantization step and the straight-through estimator?
- [ ] Can you use the HuggingFace VAE to encode and decode images?
- [ ] Can you describe the role of the VAE in Stable Diffusion's architecture?

---

## Curated Resources

### Must-Read Articles

| Resource | Level | Why |
|---|---|---|
| ⭐ [Lilian Weng — From Autoencoder to Beta-VAE](https://lilianweng.github.io/posts/2018-08-12-vae/) | Int | Most comprehensive single reference, covers all variants |
| ⭐ [Jeremy Jordan — Variational Autoencoders](https://www.jeremyjordan.me/variational-autoencoders/) | Beg | Best beginner-friendly explanation with diagrams |
| [Towards Data Science — Understanding VAEs](https://towardsdatascience.com/understanding-variational-autoencoders-vaes-f70510919f73) | Beg | Approachable introduction |

### Videos

| Resource | Duration | Level | Why |
|---|---|---|---|
| ⭐ [Arxiv Insights — Variational Autoencoders](https://www.youtube.com/watch?v=9zKuYvjFFS8) | ~30m | Beg-Int | Best visual explanation on YouTube, very highly rated |
| ⭐ [Umar Jamil — VAE in PyTorch](https://www.youtube.com/watch?v=iwEzwTTalbg) | ~1h | Int | Solid code walkthrough |
| [MIT 6.S191 — Deep Generative Modeling](https://www.youtube.com/watch?v=3G5hWM6jqPk) | ~1h | Beg | Free MIT lecture, good AE→VAE motivation |

### Papers (read in this order)

| Paper | Why |
|---|---|
| ⭐ [Auto-Encoding Variational Bayes — Kingma & Welling 2013](https://arxiv.org/abs/1312.6114) | The original VAE paper; short (~14 pages) and readable |
| [β-VAE — Higgins et al. 2017](https://openreview.net/forum?id=Sy2fchgBb) | Disentangled representations; key extension |
| [VQ-VAE — van den Oord et al. 2017](https://arxiv.org/abs/1711.00937) | Discrete latents; used in DALL·E 1 |
| [VQ-VAE-2 — Razavi et al. 2019](https://arxiv.org/abs/1906.00446) | Hierarchical VQ-VAE for high-quality images |

### Code References

| Resource | Notes |
|---|---|
| ⭐ [Keras VAE Example](https://keras.io/examples/generative/vae/) | Clean, minimal, well-documented |
| ⭐ [PyTorch Official VAE Example](https://github.com/pytorch/examples/tree/main/vae) | Standard reference implementation |
| [HuggingFace AutoencoderKL](https://huggingface.co/docs/diffusers/api/models/autoencoderkl) | Production VAE inside Stable Diffusion |
| [Google disentanglement_lib](https://github.com/google-research/disentanglement_lib) | Research library for β-VAE and disentanglement benchmarks |
| [VAE from Scratch Colab](https://colab.research.google.com/github/smartgeometry-ucl/dl4g/blob/master/variational_autoencoder.ipynb) | Interactive notebook |

---

## Practical Projects

### Project 1: Latent Space Explorer
**Level**: Beginner | **Time**: 3–4 hours

Train an MLP-VAE with 2D latent on MNIST. Build a visualization showing:
- 2D scatter of encoded test set (colored by class)
- Interactive decoder grid: map a 20×20 grid of z ∈ [-3,3]² through the decoder

**Deliverables**: scatter plot + decoder grid side-by-side.
**Key insight**: The structured, smooth latent space that VAE creates vs. AE.

---

### Project 2: VAE on MNIST — Full Implementation
**Level**: Intermediate | **Time**: 5–8 hours

Implement a complete VAE with all four visualizations + β ablation study.

**Deliverables**:
- Training curves (total loss, KL term, reconstruction term plotted separately)
- β ∈ {0.1, 1, 4, 8}: latent scatter + random sample grid for each
- Interpolation strip: 8 steps between two test images
- Comparison table: reconstruction quality (MSE) vs sample quality (visual) vs latent structure

**Key insight**: The fundamental KL ↔ reconstruction tradeoff.

---

### Project 3: Conditional VAE (CVAE) on MNIST
**Level**: Intermediate | **Time**: 5–6 hours

Add class conditioning. Demonstrate controlled generation: produce a 10×8 grid (10 classes × 8 random samples per class).

**Deliverables**: 10×8 generated grid + comparison of CVAE vs unconditional VAE samples.
**Key insight**: Label conditioning makes generation controllable.

---

### Project 4: Convolutional VAE on CelebA
**Level**: Advanced | **Time**: 15–20 hours

Train a deep CNN-VAE on CelebA (celebrity face dataset, 64×64).

**Deliverables**:
- Compare with perceptual loss vs MSE loss (sharpness difference)
- Latent arithmetic: encode two faces, average their latents, decode
- Find interpretable latent directions: encode faces with/without glasses, compute mean latent difference, apply to new faces
- FID score comparison: β=1 vs β=4

**Key insight**: Perceptual loss dramatically improves sharpness; latent space supports attribute arithmetic.

---

## Common Pitfalls

### Posterior Collapse
**What**: The encoder outputs μ≈0, σ≈1 for all inputs — it learns to ignore x and just samples from the prior. The decoder becomes unconditional.
**Why**: If the decoder is powerful enough to generate reasonable images without using z, the model learns to "give up" on the encoder.
**Symptoms**: KL term → 0 during training; reconstructions look like random samples.
**Fixes**:
- KL annealing: start with β=0, gradually increase to β=1 over training
- Free bits: set a minimum KL per dimension (e.g., max(KL_j, λ) with λ=2 nats)
- Weaker decoder: reduce capacity, add dropout

### Using `reduction='mean'` for Reconstruction Loss
**What**: Training appears to work but the KL term dominates inappropriately.
**Why**: `F.binary_cross_entropy(..., reduction='mean')` divides by N×H×W, but the KL term sums over latent_dim only. The scales are mismatched by a factor of ~784 (for MNIST).
**Fix**: Use `reduction='sum'` for reconstruction loss, so both terms scale proportionally with batch size.

### Forgetting to Scale by Batch Size in KL
**What**: KL term is much larger or smaller than expected.
**Fix**: `kl_loss` should sum over latent dimensions *and* batch items: `-0.5 * torch.sum(...)` where the sum covers both.

### Blurry Outputs — Expecting Sharp Images
**What**: Generated images look blurry.
**Why**: MSE/BCE reconstruction loss averages over pixels — the model hedges by outputting the mean of plausible values, which is blurry.
**Fix**: For sharp outputs, add a perceptual loss (LPIPS), adversarial discriminator, or switch to VQ-VAE + autoregressive decoder.

### Sampling vs. Reconstructing
**What**: Reconstructions look great but random samples look poor.
**Why**: If β is too low, the encoder maps inputs to very narrow posteriors clustered far from origin. The prior N(0,I) doesn't cover those clusters.
**Fix**: Increase β until random samples match reconstruction quality.

---

## Assessment Checkpoints

### After Phase 1 (Autoencoders)
- [ ] Can you implement a standard AE in PyTorch in ~20 lines?
- [ ] Can you explain the latent space gap problem?
- [ ] Can you visualize the 2D latent space and identify where generation fails?

### After Phase 2 (Math & ELBO)
- [ ] Can you derive the ELBO from log p(x) with pen and paper?
- [ ] Can you compute KL(N(μ, σ²) || N(0, 1)) using the closed-form formula?
- [ ] Can you explain the reparameterization trick and why it's necessary?
- [ ] Can you implement `reparameterize(mu, log_var)` from memory?

### After Phase 3 (VAE Implementation)
- [ ] Can you implement a complete VAE from scratch without reference?
- [ ] Can you explain what each term in the loss function does?
- [ ] Can you generate smooth interpolations between two images?
- [ ] Can you explain the effect of β on reconstructions vs. sample quality?

### Final Mastery Check
- [ ] Can you implement a CVAE with class conditioning?
- [ ] Can you explain posterior collapse and at least two ways to fix it?
- [ ] Can you describe the VQ-VAE quantization step and the straight-through estimator?
- [ ] Can you use the HuggingFace `AutoencoderKL` and explain its role in Stable Diffusion?
- [ ] Can you read the original VAE paper (Kingma & Welling 2013) and identify each component in your implementation?

---

## Quick Reference: Key Equations

```
ELBO OBJECTIVE (maximize)
─────────────────────────
ELBO = E_{z~q(z|x)}[log p(x|z)]  −  KL(q(z|x) || p(z))
     = reconstruction_term         −  regularization_term

ENCODER OUTPUT
──────────────
q_φ(z|x) = N(z; μ_φ(x), σ²_φ(x) · I)
Encoder predicts: (μ, log σ²)

REPARAMETERIZATION TRICK
─────────────────────────
z = μ  +  σ · ε,    ε ~ N(0, I)
σ = exp(0.5 · log_var)

KL DIVERGENCE (closed form, per dimension)
──────────────────────────────────────────
KL(N(μ, σ²) || N(0,1)) = -½ · Σ_j (1 + log σ²_j - μ²_j - σ²_j)

PYTORCH LOSS FUNCTION
─────────────────────
recon_loss = F.binary_cross_entropy(x_recon, x, reduction='sum')
kl_loss    = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
total_loss = recon_loss + beta * kl_loss

β-VAE
──────
Same as VAE but beta > 1 → stronger latent regularization → disentanglement

VQ-VAE QUANTIZATION
────────────────────
z_q = argmin_k ||z_e - e_k||    (nearest codebook vector)
Loss = ||z_e - sg[z_q]||²  +  β·||sg[z_e] - z_q||²
(sg = stop-gradient; straight-through estimator for decoder gradients)
```

---

## What's Next

### Direct continuation in this knowledge tree
- **[Diffusion Models](../Diffusion-Models/LEARNING_PATH.md)** — VAE is a prerequisite; latent diffusion (Stable Diffusion) uses the VAE you now understand as its image encoder/decoder
- **[3D Diffusion Models](../../../Computer-Graphics/3D-Generative-Models/3D-Diffusion-Models/)** — VAE concepts extend to 3D latent spaces (e.g., point cloud VAEs, mesh VAEs)
- **GANs** — the other major image generation paradigm; comparing VAE vs GAN trade-offs is a useful exercise

### Advanced Topics
- **Hierarchical VAEs** (NVAE, VDVAE): multiple levels of latent variables for higher quality generation
- **Flow-based models**: exact likelihood computation (complementary to VAE's lower bound)
- **VAE + Diffusion** (LSGM, latent score matching): combine the structured latent space of VAE with the generation quality of diffusion
- **Disentanglement metrics** (FactorVAE, MIG score): formal evaluation of β-VAE's disentanglement

### Staying Current
- **Lilian Weng's blog** — her VAE post is already the definitive reference; new posts cover downstream developments
- **Papers with Code** (paperswithcode.com/task/image-generation) — VAE benchmarks and new models
- **r/MachineLearning** — discussion of new generative model papers

---

**Difficulty**: ⭐⭐⭐ — mathematically demanding (ELBO derivation, KL divergence) but more accessible than diffusion
**Estimated time**: 4–5 weeks part-time
**Most critical resource**: [Arxiv Insights VAE video](https://www.youtube.com/watch?v=9zKuYvjFFS8) for intuition + [Lilian Weng's post](https://lilianweng.github.io/posts/2018-08-12-vae/) for depth
**Last updated**: 2026-03-16
