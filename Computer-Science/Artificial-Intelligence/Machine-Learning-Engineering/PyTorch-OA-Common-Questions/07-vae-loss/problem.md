# Problem 7: Implement VAE Loss (ELBO)

## Difficulty: Medium-Hard

## Problem Description

Implement the Evidence Lower Bound (ELBO) loss for Variational Autoencoders (VAE). VAEs are widely used in generative 3D AI for learning latent representations of 3D shapes.

## Function Signature

```python
import torch

def vae_loss(
    x: torch.Tensor,
    x_recon: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor,
    beta: float = 1.0
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Compute VAE loss (negative ELBO).

    Args:
        x: Original input of shape [batch_size, *input_dims]
        x_recon: Reconstructed input of shape [batch_size, *input_dims]
        mu: Mean of latent distribution of shape [batch_size, latent_dim]
        logvar: Log variance of latent distribution of shape [batch_size, latent_dim]
        beta: Weight for KL divergence term (beta-VAE) (default: 1.0)

    Returns:
        total_loss: Total VAE loss (scalar)
        recon_loss: Reconstruction loss (scalar)
        kl_loss: KL divergence loss (scalar)
    """
    pass
```

## Mathematical Formula

```
ELBO = E[log p(x|z)] - KL(q(z|x) || p(z))

VAE Loss = -ELBO = Reconstruction Loss + KL Divergence

Reconstruction Loss = MSE(x, x_recon) or BCE(x, x_recon)
    For continuous data: MSE = mean((x - x_recon)^2)
    For binary data: BCE = -mean(x*log(x_recon) + (1-x)*log(1-x_recon))

KL Divergence (Gaussian):
    KL(q(z|x) || N(0,I)) = -0.5 * mean(1 + logvar - mu^2 - exp(logvar))

Beta-VAE:
    Total Loss = Reconstruction Loss + beta * KL Divergence
    (beta > 1 encourages more disentangled representations)
```

## Examples

```python
# Example 1: Image VAE
batch_size, channels, height, width = 16, 1, 28, 28
latent_dim = 32

# Original and reconstructed images
x = torch.randn(batch_size, channels, height, width)
x_recon = torch.randn(batch_size, channels, height, width)

# Latent distribution parameters
mu = torch.randn(batch_size, latent_dim)
logvar = torch.randn(batch_size, latent_dim)

total_loss, recon_loss, kl_loss = vae_loss(x, x_recon, mu, logvar)
# Expected: all scalars, total_loss = recon_loss + kl_loss

# Example 2: Beta-VAE (disentangled representations)
total_loss, recon_loss, kl_loss = vae_loss(x, x_recon, mu, logvar, beta=4.0)
# Expected: total_loss = recon_loss + 4.0 * kl_loss

# Example 3: 3D shape VAE
batch_size, num_points, point_dim = 8, 2048, 3
latent_dim = 128

# Point clouds
point_cloud = torch.randn(batch_size, num_points, point_dim)
point_cloud_recon = torch.randn(batch_size, num_points, point_dim)

mu = torch.randn(batch_size, latent_dim)
logvar = torch.randn(batch_size, latent_dim)

total_loss, recon_loss, kl_loss = vae_loss(
    point_cloud, point_cloud_recon, mu, logvar
)
```

## Test Cases

```python
def test_vae_loss():
    # Test 1: Loss decomposition
    x = torch.randn(16, 1, 28, 28)
    x_recon = torch.randn(16, 1, 28, 28)
    mu = torch.randn(16, 32)
    logvar = torch.randn(16, 32)

    total, recon, kl = vae_loss(x, x_recon, mu, logvar, beta=1.0)
    assert torch.isclose(total, recon + kl)

    # Test 2: Beta-VAE weighting
    total_beta, recon_beta, kl_beta = vae_loss(x, x_recon, mu, logvar, beta=2.0)
    assert torch.isclose(total_beta, recon_beta + 2.0 * kl_beta)

    # Test 3: Perfect reconstruction
    x_perfect = torch.randn(8, 784)
    mu_zero = torch.zeros(8, 32)
    logvar_zero = torch.zeros(8, 32)

    total, recon, kl = vae_loss(x_perfect, x_perfect, mu_zero, logvar_zero)
    assert recon < 1e-6  # Nearly zero reconstruction loss
    assert kl < 1e-6     # KL should be zero for N(0,1)

    # Test 4: KL divergence properties
    # KL >= 0 always
    total, recon, kl = vae_loss(x, x_recon, mu, logvar)
    assert kl >= 0

    # Test 5: Standard normal prior
    # mu=0, logvar=0 should give KL ≈ 0
    mu_standard = torch.zeros(16, 32)
    logvar_standard = torch.zeros(16, 32)
    total, recon, kl = vae_loss(x, x_recon, mu_standard, logvar_standard)
    assert kl < 1e-5
```

## Hints

1. **Reconstruction loss** (MSE for continuous data):
   ```python
   recon_loss = torch.nn.functional.mse_loss(x_recon, x, reduction='mean')
   # Or for binary data:
   # recon_loss = torch.nn.functional.binary_cross_entropy(x_recon, x, reduction='mean')
   ```

2. **KL divergence** (closed form for Gaussian):
   ```python
   # KL(N(mu, var) || N(0, 1))
   kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
   kl = kl / batch_size  # Average over batch
   ```

3. **Alternative KL computation**:
   ```python
   kl_per_latent = -0.5 * (1 + logvar - mu**2 - torch.exp(logvar))
   kl = kl_per_latent.sum(dim=1).mean()
   ```

4. **Flattening input** (if needed):
   ```python
   x_flat = x.reshape(batch_size, -1)
   x_recon_flat = x_recon.reshape(batch_size, -1)
   ```

5. **Beta weighting**:
   ```python
   total_loss = recon_loss + beta * kl_loss
   ```

## Expected Time

20-28 minutes

## Key Concepts

- Variational inference
- KL divergence (closed form for Gaussian)
- ELBO (Evidence Lower Bound)
- Reconstruction vs regularization trade-off
- Beta-VAE for disentanglement
- Log variance parameterization for numerical stability

## Why This Matters for 3D AI

VAEs are used in:
- **3D shape generation**: Learn latent space of 3D shapes (e.g., occupancy grids, point clouds)
- **Shape interpolation**: Smooth transitions between 3D models in latent space
- **Disentangled representations**: Beta-VAE for controllable 3D generation
- **Texture generation**: Generate textures for 3D models
- **Compression**: Compress 3D assets using learned latent codes
- **Foundation models**: Many 3D diffusion models use VAE-like encoders

## Bonus Challenge

1. Implement the reparameterization trick for sampling:
```python
def reparameterize(mu, logvar):
    """
    Sample z from N(mu, var) using reparameterization trick.
    z = mu + sigma * epsilon, where epsilon ~ N(0, 1)
    """
    pass
```

2. Implement KL annealing schedule:
```python
def vae_loss_with_annealing(x, x_recon, mu, logvar, epoch, max_epochs):
    """
    Gradually increase KL weight from 0 to 1 over training.
    Helps prevent posterior collapse.
    """
    pass
```
