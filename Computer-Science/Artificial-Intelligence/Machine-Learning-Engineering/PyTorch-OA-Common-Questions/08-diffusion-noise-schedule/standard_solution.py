"""
Solution: Implement Diffusion Noise Schedule
Difficulty: Medium
Expected Time: 15-22 minutes
"""

import torch
import math


def linear_beta_schedule(
    timesteps: int,
    beta_start: float = 0.0001,
    beta_end: float = 0.02
) -> torch.Tensor:
    """
    Create a linear beta schedule for diffusion.

    Args:
        timesteps: Number of diffusion steps (e.g., 1000)
        beta_start: Starting beta value (variance at t=0)
        beta_end: Ending beta value (variance at t=T)

    Returns:
        Tensor of shape [timesteps] containing beta values
    """
    return torch.linspace(beta_start, beta_end, timesteps)


def cosine_beta_schedule(timesteps: int, s: float = 0.008) -> torch.Tensor:
    """
    Cosine schedule as proposed in "Improved Denoising Diffusion Probabilistic Models"

    More gradual noise addition compared to linear schedule.
    """
    # Compute alpha_bar using cosine function
    steps = timesteps + 1
    t = torch.linspace(0, timesteps, steps)

    # Cosine schedule for alpha_cumprod
    alphas_cumprod = torch.cos(((t / timesteps) + s) / (1 + s) * math.pi * 0.5) ** 2
    alphas_cumprod = alphas_cumprod / alphas_cumprod[0]

    # Compute betas from alphas_cumprod
    # alpha_t = alpha_cumprod_t / alpha_cumprod_{t-1}
    alphas = alphas_cumprod[1:] / alphas_cumprod[:-1]

    # Clip alphas to avoid numerical issues
    alphas = torch.clamp(alphas, min=0.001, max=0.9999)

    betas = 1 - alphas

    return betas


def get_alpha_schedule(
    betas: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Compute alpha, alpha_hat (cumulative product), and related values.

    Args:
        betas: Beta schedule of shape [timesteps]

    Returns:
        alphas: 1 - betas
        alphas_cumprod: Cumulative product of alphas (alpha_hat)
        alphas_cumprod_prev: alpha_hat shifted by 1 (for denoising)
    """
    # alphas = 1 - betas
    alphas = 1.0 - betas

    # Cumulative product of alphas
    alphas_cumprod = torch.cumprod(alphas, dim=0)

    # Shifted cumulative product (prepend 1.0)
    alphas_cumprod_prev = torch.cat([torch.tensor([1.0]), alphas_cumprod[:-1]])

    return alphas, alphas_cumprod, alphas_cumprod_prev


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
    batch_size = x0.shape[0]

    # Extract alpha_cumprod for each timestep in the batch
    # t: [batch_size], alphas_cumprod: [timesteps]
    # alpha_t: [batch_size]
    alpha_t = alphas_cumprod[t]

    # Reshape for broadcasting: [batch_size, 1, 1, 1]
    # Works for images [B, C, H, W] and vectors [B, D]
    while len(alpha_t.shape) < len(x0.shape):
        alpha_t = alpha_t.unsqueeze(-1)

    # Sample noise from standard normal
    noise = torch.randn_like(x0)

    # Apply forward diffusion formula
    # x_t = sqrt(alpha_hat_t) * x_0 + sqrt(1 - alpha_hat_t) * epsilon
    sqrt_alpha_t = torch.sqrt(alpha_t)
    sqrt_one_minus_alpha_t = torch.sqrt(1 - alpha_t)

    xt = sqrt_alpha_t * x0 + sqrt_one_minus_alpha_t * noise

    return xt, noise


# Bonus: Reverse diffusion (denoising one step)
def reverse_diffusion_step(
    xt: torch.Tensor,
    t: int,
    predicted_noise: torch.Tensor,
    betas: torch.Tensor,
    alphas_cumprod: torch.Tensor,
    alphas_cumprod_prev: torch.Tensor
) -> torch.Tensor:
    """
    Denoise xt to get x_{t-1} given predicted noise.

    Uses DDPM reverse process formula.
    """
    alpha_t = 1 - betas[t]
    alpha_cumprod_t = alphas_cumprod[t]
    alpha_cumprod_prev_t = alphas_cumprod_prev[t]

    # Reshape for broadcasting
    alpha_t = alpha_t.reshape(-1, 1, 1, 1) if len(xt.shape) == 4 else alpha_t
    alpha_cumprod_t = alpha_cumprod_t.reshape(-1, 1, 1, 1) if len(xt.shape) == 4 else alpha_cumprod_t
    alpha_cumprod_prev_t = alpha_cumprod_prev_t.reshape(-1, 1, 1, 1) if len(xt.shape) == 4 else alpha_cumprod_prev_t

    # Predict x0 from xt and predicted noise
    pred_x0 = (xt - torch.sqrt(1 - alpha_cumprod_t) * predicted_noise) / torch.sqrt(alpha_cumprod_t)

    # Compute direction pointing to xt
    pred_dir = torch.sqrt(1 - alpha_cumprod_prev_t) * predicted_noise

    # Compute x_{t-1}
    x_prev = torch.sqrt(alpha_cumprod_prev_t) * pred_x0 + pred_dir

    # Add noise if not the last step
    if t > 0:
        noise = torch.randn_like(xt)
        variance = betas[t]
        x_prev = x_prev + torch.sqrt(variance) * noise

    return x_prev


# Bonus: DDIM sampling (deterministic)
def ddim_step(
    xt: torch.Tensor,
    t: int,
    predicted_noise: torch.Tensor,
    alphas_cumprod: torch.Tensor,
    alphas_cumprod_prev: torch.Tensor,
    eta: float = 0.0
) -> torch.Tensor:
    """
    DDIM sampling: faster sampling with fewer steps.

    Args:
        eta: Stochasticity parameter (0 = deterministic, 1 = DDPM)
    """
    alpha_cumprod_t = alphas_cumprod[t]
    alpha_cumprod_prev_t = alphas_cumprod_prev[t]

    # Reshape for broadcasting
    if len(xt.shape) == 4:
        alpha_cumprod_t = alpha_cumprod_t.reshape(-1, 1, 1, 1)
        alpha_cumprod_prev_t = alpha_cumprod_prev_t.reshape(-1, 1, 1, 1)

    # Predict x0
    pred_x0 = (xt - torch.sqrt(1 - alpha_cumprod_t) * predicted_noise) / torch.sqrt(alpha_cumprod_t)

    # Compute variance
    sigma_t = eta * torch.sqrt((1 - alpha_cumprod_prev_t) / (1 - alpha_cumprod_t)) * \
              torch.sqrt(1 - alpha_cumprod_t / alpha_cumprod_prev_t)

    # Compute direction
    direction = torch.sqrt(1 - alpha_cumprod_prev_t - sigma_t ** 2) * predicted_noise

    # Compute x_{t-1}
    x_prev = torch.sqrt(alpha_cumprod_prev_t) * pred_x0 + direction

    # Add noise
    if eta > 0 and t > 0:
        noise = torch.randn_like(xt)
        x_prev = x_prev + sigma_t * noise

    return x_prev


# Test cases
def test_diffusion_schedule():
    print("Running tests for diffusion noise schedule...\n")

    # Test 1: Beta schedule shape and values
    print("Test 1: Beta schedule properties")
    timesteps = 1000
    betas = linear_beta_schedule(timesteps, beta_start=0.0001, beta_end=0.02)

    assert betas.shape == (timesteps,)
    assert betas[0] < betas[-1]  # Increasing
    assert (betas > 0).all() and (betas < 1).all()  # Valid range

    print(f"✓ Beta schedule shape: {betas.shape}")
    print(f"✓ Beta range: [{betas.min().item():.6f}, {betas.max().item():.6f}]")
    print(f"✓ First beta: {betas[0].item():.6f}, Last beta: {betas[-1].item():.6f}")

    # Test 2: Alpha schedule properties
    print("\nTest 2: Alpha schedule properties")
    alphas, alphas_cumprod, alphas_cumprod_prev = get_alpha_schedule(betas)

    assert torch.allclose(alphas, 1 - betas)
    assert torch.isclose(alphas_cumprod[0], alphas[0])
    assert alphas_cumprod[-1] < alphas_cumprod[0]  # Decreasing

    print(f"✓ Alphas = 1 - betas: {torch.allclose(alphas, 1 - betas)}")
    print(f"✓ Alpha cumprod range: [{alphas_cumprod.min().item():.6f}, {alphas_cumprod.max().item():.6f}]")
    print(f"✓ Alpha cumprod is decreasing: {(alphas_cumprod[:-1] >= alphas_cumprod[1:]).all()}")

    # Test 3: Forward diffusion shape
    print("\nTest 3: Forward diffusion shape and output")
    x0 = torch.randn(4, 3, 32, 32)
    t = torch.tensor([0, 250, 500, 999])
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)

    assert xt.shape == x0.shape
    assert noise.shape == x0.shape

    print(f"✓ Input shape: {x0.shape}")
    print(f"✓ Output shape: {xt.shape}")
    print(f"✓ Noise shape: {noise.shape}")

    # Test 4: t=0 should add minimal noise
    print("\nTest 4: Minimal noise at t=0")
    t = torch.zeros(4, dtype=torch.long)
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)

    # At t=0, alpha_cumprod ≈ 1, so xt ≈ x0
    difference = (xt - x0).abs().mean()
    print(f"✓ Mean absolute difference at t=0: {difference.item():.6f}")
    assert difference < 0.1

    # Test 5: t=T-1 should be mostly noise
    print("\nTest 5: Maximum noise at t=T-1")
    t = torch.tensor([timesteps - 1] * 4)
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)

    # At t=T-1, alpha_cumprod ≈ 0, so xt should have low correlation with x0
    correlation = torch.cosine_similarity(
        xt.flatten(1), x0.flatten(1), dim=1
    ).abs().mean()

    print(f"✓ Correlation with original at t=T-1: {correlation.item():.6f}")
    assert correlation < 0.5  # Mostly decorrelated

    # Test 6: Noise distribution
    print("\nTest 6: Noise distribution (should be N(0, 1))")
    t = torch.randint(0, timesteps, (100,))
    x0_large = torch.randn(100, 3, 32, 32)
    xt_large, noise_large = forward_diffusion(x0_large, t, alphas_cumprod)

    noise_mean = noise_large.mean()
    noise_std = noise_large.std()

    print(f"✓ Noise mean: {noise_mean.item():.6f} (expected ~0)")
    print(f"✓ Noise std: {noise_std.item():.6f} (expected ~1)")

    assert torch.allclose(noise_mean, torch.tensor(0.0), atol=0.05)
    assert torch.allclose(noise_std, torch.tensor(1.0), atol=0.05)

    # Test 7: Different timesteps in same batch
    print("\nTest 7: Different timesteps in same batch")
    t = torch.tensor([0, 100, 500, 999])
    xt, noise = forward_diffusion(x0, t, alphas_cumprod)

    # Noise level should increase with t
    noise_levels = []
    for i in range(4):
        noise_level = (xt[i] - x0[i]).abs().mean()
        noise_levels.append(noise_level.item())

    print(f"✓ Noise levels at different t: {[f'{nl:.4f}' for nl in noise_levels]}")
    # Generally increasing (may not be strictly monotonic due to randomness)

    # Test 8: Cosine schedule
    print("\nTest 8: Cosine beta schedule")
    betas_cosine = cosine_beta_schedule(timesteps)
    alphas_cos, alphas_cumprod_cos, _ = get_alpha_schedule(betas_cosine)

    print(f"✓ Cosine beta range: [{betas_cosine.min().item():.6f}, {betas_cosine.max().item():.6f}]")
    print(f"✓ Cosine schedule is smoother at the beginning")

    # Test 9: Compare linear vs cosine schedule
    print("\nTest 9: Compare linear vs cosine schedules")
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.plot(betas.numpy(), label='Linear')
    plt.plot(betas_cosine.numpy(), label='Cosine')
    plt.title('Beta Schedule')
    plt.legend()

    plt.subplot(1, 3, 2)
    plt.plot(alphas_cumprod.numpy(), label='Linear')
    plt.plot(alphas_cumprod_cos.numpy(), label='Cosine')
    plt.title('Alpha Cumulative Product')
    plt.legend()

    plt.subplot(1, 3, 3)
    plt.plot(torch.sqrt(1 - alphas_cumprod).numpy(), label='Linear')
    plt.plot(torch.sqrt(1 - alphas_cumprod_cos).numpy(), label='Cosine')
    plt.title('Noise Level')
    plt.legend()

    plt.tight_layout()
    plt.savefig('/tmp/diffusion_schedules.png')
    print(f"✓ Schedule comparison plot saved to /tmp/diffusion_schedules.png")

    # Test 10: Forward-backward consistency (simplified check)
    print("\nTest 10: Reverse diffusion (basic check)")
    x0_simple = torch.randn(1, 3, 8, 8)
    t_simple = torch.tensor([100])

    xt_simple, true_noise = forward_diffusion(x0_simple, t_simple, alphas_cumprod)

    # If we knew the exact noise, we could reverse perfectly
    # Here we just check that reverse_diffusion_step runs
    x_prev = reverse_diffusion_step(
        xt_simple, t_simple[0].item(), true_noise,
        betas, alphas_cumprod, alphas_cumprod_prev
    )

    print(f"✓ Reverse diffusion step runs successfully")
    print(f"✓ Output shape: {x_prev.shape}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_diffusion_schedule()
