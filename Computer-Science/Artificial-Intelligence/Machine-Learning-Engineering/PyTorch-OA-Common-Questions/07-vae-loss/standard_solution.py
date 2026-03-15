"""
Solution: Implement VAE Loss (ELBO)
Difficulty: Medium-Hard
Expected Time: 20-28 minutes
"""

import torch
import torch.nn.functional as F


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
    batch_size = x.shape[0]

    # Flatten input if needed (for spatial data)
    x_flat = x.reshape(batch_size, -1)
    x_recon_flat = x_recon.reshape(batch_size, -1)

    # Reconstruction loss (MSE for continuous data)
    # Can also use BCE for binary data
    recon_loss = F.mse_loss(x_recon_flat, x_flat, reduction='mean')

    # KL divergence: KL(N(mu, var) || N(0, 1))
    # Closed form: -0.5 * sum(1 + log(var) - mu^2 - var)
    # We use logvar for numerical stability
    kl_divergence = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    # Average over batch
    kl_loss = kl_divergence / batch_size

    # Total loss (negative ELBO)
    total_loss = recon_loss + beta * kl_loss

    return total_loss, recon_loss, kl_loss


# Alternative: Binary Cross-Entropy for binary data (e.g., MNIST)
def vae_loss_bce(
    x: torch.Tensor,
    x_recon: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor,
    beta: float = 1.0
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """VAE loss with BCE reconstruction loss for binary data"""
    batch_size = x.shape[0]

    x_flat = x.reshape(batch_size, -1)
    x_recon_flat = x_recon.reshape(batch_size, -1)

    # BCE reconstruction loss
    recon_loss = F.binary_cross_entropy(x_recon_flat, x_flat, reduction='mean')

    # KL divergence
    kl_divergence = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    kl_loss = kl_divergence / batch_size

    total_loss = recon_loss + beta * kl_loss

    return total_loss, recon_loss, kl_loss


# Bonus: Reparameterization trick
def reparameterize(mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
    """
    Sample z from N(mu, var) using reparameterization trick.

    z = mu + sigma * epsilon, where epsilon ~ N(0, 1)
    sigma = exp(0.5 * logvar)

    Args:
        mu: Mean of shape [batch_size, latent_dim]
        logvar: Log variance of shape [batch_size, latent_dim]

    Returns:
        z: Sampled latent vector of shape [batch_size, latent_dim]
    """
    # Sample epsilon from standard normal
    epsilon = torch.randn_like(mu)

    # Compute std from logvar
    std = torch.exp(0.5 * logvar)

    # Reparameterization: z = mu + std * epsilon
    z = mu + std * epsilon

    return z


# Bonus: KL annealing
def vae_loss_with_annealing(
    x: torch.Tensor,
    x_recon: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor,
    epoch: int,
    max_epochs: int,
    annealing_type: str = 'linear'
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, float]:
    """
    VAE loss with KL annealing to prevent posterior collapse.

    Args:
        epoch: Current epoch (0-indexed)
        max_epochs: Total number of epochs for annealing
        annealing_type: 'linear' or 'cyclical'

    Returns:
        total_loss, recon_loss, kl_loss, kl_weight
    """
    batch_size = x.shape[0]

    x_flat = x.reshape(batch_size, -1)
    x_recon_flat = x_recon.reshape(batch_size, -1)

    recon_loss = F.mse_loss(x_recon_flat, x_flat, reduction='mean')

    kl_divergence = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    kl_loss = kl_divergence / batch_size

    # Compute KL weight based on annealing schedule
    if annealing_type == 'linear':
        # Linearly increase from 0 to 1
        kl_weight = min(1.0, epoch / max(1, max_epochs - 1))
    elif annealing_type == 'cyclical':
        # Cyclical annealing (useful for preventing local minima)
        cycle_length = max_epochs // 4
        cycle_position = epoch % cycle_length
        kl_weight = min(1.0, cycle_position / max(1, cycle_length - 1))
    else:
        kl_weight = 1.0

    total_loss = recon_loss + kl_weight * kl_loss

    return total_loss, recon_loss, kl_loss, kl_weight


# Test cases
def test_vae_loss():
    print("Running tests for vae_loss...\n")

    # Test 1: Loss decomposition
    print("Test 1: Loss decomposition (beta=1.0)")
    x = torch.randn(16, 1, 28, 28)
    x_recon = torch.randn(16, 1, 28, 28)
    mu = torch.randn(16, 32)
    logvar = torch.randn(16, 32)

    total, recon, kl = vae_loss(x, x_recon, mu, logvar, beta=1.0)

    assert torch.isclose(total, recon + kl, atol=1e-5)
    print(f"✓ Total loss: {total.item():.6f}")
    print(f"✓ Recon loss: {recon.item():.6f}")
    print(f"✓ KL loss: {kl.item():.6f}")
    print(f"✓ Total = Recon + KL: {torch.isclose(total, recon + kl)}")

    # Test 2: Beta-VAE weighting
    print("\nTest 2: Beta-VAE weighting (beta=2.0)")
    total_beta, recon_beta, kl_beta = vae_loss(x, x_recon, mu, logvar, beta=2.0)

    assert torch.isclose(total_beta, recon_beta + 2.0 * kl_beta, atol=1e-5)
    print(f"✓ Total loss: {total_beta.item():.6f}")
    print(f"✓ Total = Recon + 2.0 * KL: {torch.isclose(total_beta, recon_beta + 2.0 * kl_beta)}")

    # Test 3: Perfect reconstruction with standard normal latent
    print("\nTest 3: Perfect reconstruction + standard normal prior")
    x_perfect = torch.randn(8, 784)
    mu_zero = torch.zeros(8, 32)
    logvar_zero = torch.zeros(8, 32)

    total, recon, kl = vae_loss(x_perfect, x_perfect, mu_zero, logvar_zero)

    assert recon < 1e-6  # Nearly zero reconstruction loss
    assert kl < 1e-5     # KL should be ~0 for N(0, 1)
    print(f"✓ Reconstruction loss (should be ~0): {recon.item():.10f}")
    print(f"✓ KL loss (should be ~0): {kl.item():.10f}")

    # Test 4: KL divergence is always non-negative
    print("\nTest 4: KL divergence >= 0")
    for _ in range(10):
        mu = torch.randn(16, 32)
        logvar = torch.randn(16, 32)
        x = torch.randn(16, 784)

        total, recon, kl = vae_loss(x, x, mu, logvar)
        assert kl >= -1e-6  # Allow small numerical error
    print(f"✓ KL divergence is non-negative in all random tests")

    # Test 5: Different input shapes
    print("\nTest 5: Different input shapes")

    # Images
    x_img = torch.randn(4, 3, 64, 64)
    x_recon_img = torch.randn(4, 3, 64, 64)
    mu = torch.randn(4, 128)
    logvar = torch.randn(4, 128)

    total_img, _, _ = vae_loss(x_img, x_recon_img, mu, logvar)
    print(f"✓ Image input shape {x_img.shape}: loss = {total_img.item():.6f}")

    # Vectors
    x_vec = torch.randn(16, 512)
    x_recon_vec = torch.randn(16, 512)
    mu = torch.randn(16, 64)
    logvar = torch.randn(16, 64)

    total_vec, _, _ = vae_loss(x_vec, x_recon_vec, mu, logvar)
    print(f"✓ Vector input shape {x_vec.shape}: loss = {total_vec.item():.6f}")

    # Test 6: BCE reconstruction loss
    print("\nTest 6: Binary cross-entropy reconstruction loss")
    x_binary = torch.rand(16, 1, 28, 28)  # Binary data in [0, 1]
    x_recon_binary = torch.sigmoid(torch.randn(16, 1, 28, 28))  # Ensure [0, 1]
    mu = torch.randn(16, 32)
    logvar = torch.randn(16, 32)

    total_bce, recon_bce, kl_bce = vae_loss_bce(x_binary, x_recon_binary, mu, logvar)
    print(f"✓ BCE reconstruction loss: {recon_bce.item():.6f}")

    # Test 7: Reparameterization trick
    print("\nTest 7: Reparameterization trick")
    mu = torch.tensor([[0.0, 1.0, -1.0]])
    logvar = torch.tensor([[0.0, 0.0, 0.0]])  # var = 1

    # Sample multiple times
    samples = [reparameterize(mu, logvar) for _ in range(1000)]
    samples_stacked = torch.cat(samples, dim=0)

    # Check mean and std
    sample_mean = samples_stacked.mean(dim=0)
    sample_std = samples_stacked.std(dim=0)

    print(f"✓ Expected mean: {mu[0]}")
    print(f"✓ Sampled mean: {sample_mean}")
    print(f"✓ Expected std: {torch.exp(0.5 * logvar[0])}")
    print(f"✓ Sampled std: {sample_std}")

    assert torch.allclose(sample_mean, mu[0], atol=0.1)
    assert torch.allclose(sample_std, torch.ones(3), atol=0.1)

    # Test 8: KL annealing
    print("\nTest 8: KL annealing")
    x = torch.randn(8, 784)
    x_recon = torch.randn(8, 784)
    mu = torch.randn(8, 32)
    logvar = torch.randn(8, 32)

    max_epochs = 100
    kl_weights = []

    for epoch in [0, 25, 50, 75, 99]:
        total, recon, kl, kl_weight = vae_loss_with_annealing(
            x, x_recon, mu, logvar, epoch, max_epochs, annealing_type='linear'
        )
        kl_weights.append(kl_weight)
        print(f"  Epoch {epoch:3d}: KL weight = {kl_weight:.4f}")

    # Check that weights are increasing
    assert all(kl_weights[i] <= kl_weights[i+1] for i in range(len(kl_weights)-1))
    print(f"✓ KL weights increase monotonically")

    # Test 9: Point cloud VAE (3D AI application)
    print("\nTest 9: Point cloud VAE (3D AI)")
    batch_size, num_points, point_dim = 8, 2048, 3
    latent_dim = 128

    # Point clouds
    point_cloud = torch.randn(batch_size, num_points, point_dim)
    point_cloud_recon = torch.randn(batch_size, num_points, point_dim)

    mu = torch.randn(batch_size, latent_dim)
    logvar = torch.randn(batch_size, latent_dim)

    total, recon, kl = vae_loss(point_cloud, point_cloud_recon, mu, logvar)

    print(f"✓ Point cloud shape: {point_cloud.shape}")
    print(f"✓ Total loss: {total.item():.6f}")
    print(f"✓ Latent dim: {latent_dim}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_vae_loss()
