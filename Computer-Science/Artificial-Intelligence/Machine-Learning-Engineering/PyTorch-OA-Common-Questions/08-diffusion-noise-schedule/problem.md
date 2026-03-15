# Problem 8: Implement Diffusion Noise Schedule

## Difficulty: Medium

## Problem Description

Implement the forward diffusion process (noise scheduling) used in diffusion models like DDPM. This is crucial for understanding how diffusion models work, which are state-of-the-art for text-to-3D generation.

## Function Signature

```python
import torch

def linear_beta_schedule(timesteps: int, beta_start: float = 0.0001, beta_end: float = 0.02) -> torch.Tensor:
    """
    Create a linear beta schedule for diffusion.

    Args:
        timesteps: Number of diffusion steps (e.g., 1000)
        beta_start: Starting beta value (variance at t=0)
        beta_end: Ending beta value (variance at t=T)

    Returns:
        Tensor of shape [timesteps] containing beta values
    """
    pass


def get_alpha_schedule(betas: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Compute alpha, alpha_hat (cumulative product), and related values.

    Args:
        betas: Beta schedule of shape [timesteps]

    Returns:
        alphas: 1 - betas
        alphas_cumprod: Cumulative product of alphas (alpha_hat)
        alphas_cumprod_prev: alpha_hat shifted by 1 (for denoising)
    """
    pass


def forward_diffusion(
    x0: torch.Tensor,
    t: torch.Tensor,
    alphas_cumprod: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Add noise to x0 according to the diffusion schedule at timestep t.

    Args:
        x0: Clean images of shape [batch_size, channels, height, width]
        t: Timesteps of shape [batch_size] (values in range [0, timesteps-1])
        alphas_cumprod: Cumulative product of alphas [timesteps]

    Returns:
        xt: Noisy images at timestep t
        noise: The noise that was added (for training loss)
    """
    pass
```

## Mathematical Formula

```
Forward diffusion process (adding noise):

q(x_t | x_0) = N(x_t; sqrt(alpha_hat_t) * x_0, (1 - alpha_hat_t) * I)

where:
- beta_t: variance schedule (how much noise to add at step t)
- alpha_t = 1 - beta_t
- alpha_hat_t = prod(alpha_s for s=1 to t)  # cumulative product

Reparameterization (efficient sampling):
x_t = sqrt(alpha_hat_t) * x_0 + sqrt(1 - alpha_hat_t) * epsilon
where epsilon ~ N(0, I)

Beta schedules:
- Linear: beta_t = beta_start + (beta_end - beta_start) * t / T
- Cosine: more sophisticated, slower noise addition
```

## Examples

```python
# Example 1: Create noise schedule
timesteps = 1000
betas = linear_beta_schedule(timesteps, beta_start=0.0001, beta_end=0.02)
# Expected shape: [1000]

alphas, alphas_cumprod, alphas_cumprod_prev = get_alpha_schedule(betas)
# All shapes: [1000]

# Example 2: Add noise to images at different timesteps
batch_size, channels, height, width = 8, 3, 32, 32
x0 = torch.randn(batch_size, channels, height, width)  # Clean images

# Add noise at t=100
t = torch.tensor([100] * batch_size)
xt, noise = forward_diffusion(x0, t, alphas_cumprod)
# xt shape: [8, 3, 32, 32] - noisy images
# noise shape: [8, 3, 32, 32] - the noise that was added

# Example 3: Different timesteps in same batch
t = torch.tensor([0, 100, 500, 999, 250, 750, 50, 900])
xt, noise = forward_diffusion(x0, t, alphas_cumprod)
# Each sample in batch has different noise level

# Example 4: Visualize noise schedule
import matplotlib.pyplot as plt
plt.plot(betas.numpy())
plt.title("Beta schedule")
plt.plot(alphas_cumprod.numpy())
plt.title("Alpha cumulative product")
```

## Test Cases

```python
def test_diffusion_schedule():
    # Test 1: Beta schedule shape and values
    timesteps = 1000
    betas = linear_beta_schedule(timesteps)
    assert betas.shape == (timesteps,)
    assert betas[0] < betas[-1]  # Increasing
    assert (betas > 0).all() and (betas < 1).all()  # Valid range

    # Test 2: Alpha schedule properties
    alphas, alphas_cumprod, alphas_cumprod_prev = get_alpha_schedule(betas)
    assert torch.allclose(alphas, 1 - betas)
    assert alphas_cumprod[0] == alphas[0]
    assert alphas_cumprod[-1] < alphas_cumprod[0]  # Decreasing

    # Test 3: Forward diffusion shape
    x0 = torch.randn(4, 3, 32, 32)
    t = torch.tensor([0, 250, 500, 999])
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)
    assert xt.shape == x0.shape
    assert noise.shape == x0.shape

    # Test 4: t=0 should add minimal noise
    t = torch.zeros(4, dtype=torch.long)
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)
    # x_t should be very close to x_0
    assert torch.allclose(xt, x0, atol=0.1)

    # Test 5: t=T-1 should be mostly noise
    t = torch.tensor([timesteps - 1] * 4)
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)
    # x_t should have small correlation with x_0
    correlation = torch.cosine_similarity(
        xt.flatten(1), x0.flatten(1), dim=1
    ).abs().mean()
    assert correlation < 0.5  # Mostly decorrelated

    # Test 6: Noise distribution
    # epsilon should be standard normal N(0, 1)
    assert torch.allclose(noise.mean(), torch.tensor(0.0), atol=0.1)
    assert torch.allclose(noise.std(), torch.tensor(1.0), atol=0.1)
```

## Hints

1. **Linear beta schedule**:
   ```python
   betas = torch.linspace(beta_start, beta_end, timesteps)
   ```

2. **Cumulative product**:
   ```python
   alphas = 1.0 - betas
   alphas_cumprod = torch.cumprod(alphas, dim=0)
   ```

3. **Shifted cumulative product**:
   ```python
   alphas_cumprod_prev = torch.cat([torch.tensor([1.0]), alphas_cumprod[:-1]])
   ```

4. **Extract values for specific timesteps**:
   ```python
   # t is [batch_size], alphas_cumprod is [timesteps]
   # Extract alphas_cumprod[t] for each sample
   alpha_t = alphas_cumprod[t]
   # Reshape to [batch_size, 1, 1, 1] for broadcasting
   alpha_t = alpha_t.reshape(-1, 1, 1, 1)
   ```

5. **Forward diffusion**:
   ```python
   noise = torch.randn_like(x0)
   sqrt_alpha_hat = torch.sqrt(alpha_t)
   sqrt_one_minus_alpha_hat = torch.sqrt(1 - alpha_t)
   xt = sqrt_alpha_hat * x0 + sqrt_one_minus_alpha_hat * noise
   ```

## Expected Time

15-22 minutes

## Key Concepts

- Noise scheduling (beta, alpha)
- Cumulative products
- Reparameterization trick
- Broadcasting for batched operations
- Gaussian diffusion process
- Understanding variance schedules

## Why This Matters for 3D AI

Diffusion models are used in:
- **Text-to-3D**: DreamFusion, Magic3D, Point-E use diffusion
- **3D shape generation**: Generate 3D shapes directly
- **Texture synthesis**: Diffusion models for 3D texture generation
- **Point cloud generation**: Diffuse point clouds
- **NeRF distillation**: Use 2D diffusion models (Stable Diffusion) to guide 3D generation
- **Multi-view consistency**: Diffusion for consistent multi-view generation

## Bonus Challenge

1. Implement cosine beta schedule (more gradual noise addition):
```python
def cosine_beta_schedule(timesteps, s=0.008):
    """
    Cosine schedule as proposed in "Improved Denoising Diffusion Probabilistic Models"
    """
    pass
```

2. Implement the reverse process (denoising one step):
```python
def reverse_diffusion_step(xt, t, predicted_noise, betas, alphas_cumprod):
    """
    Denoise xt to get x_{t-1} given predicted noise.
    """
    pass
```

3. Implement DDIM (deterministic) sampling:
```python
def ddim_step(xt, t, predicted_noise, alphas_cumprod, eta=0.0):
    """
    DDIM sampling: faster sampling with fewer steps.
    eta=0 is deterministic, eta=1 is DDPM.
    """
    pass
```
