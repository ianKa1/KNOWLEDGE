"""
Solution: Implement Softmax
Difficulty: Easy
Expected Time: 5-10 minutes
"""

import torch


def softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    """
    Compute softmax values for tensor x along the specified dimension.

    Args:
        x: Input tensor of shape [..., n, ...]
        dim: Dimension along which to compute softmax (default: -1)

    Returns:
        Tensor of same shape as x with softmax applied along dim
    """
    # Numerical stability: subtract max value before exponential
    # This prevents overflow when computing exp of large numbers
    x_max = x.max(dim=dim, keepdim=True).values
    x_shifted = x - x_max

    # Compute exponentials
    exp_x = torch.exp(x_shifted)

    # Normalize by sum
    sum_exp = exp_x.sum(dim=dim, keepdim=True)

    return exp_x / sum_exp


# Test cases
def test_softmax():
    print("Running tests for softmax...\n")

    # Test 1: Sum to 1
    print("Test 1: Output should sum to 1")
    x = torch.randn(100)
    out = softmax(x)
    assert torch.allclose(out.sum(), torch.tensor(1.0))
    print(f"✓ Sum: {out.sum().item():.6f}")

    # Test 2: Non-negative
    print("\nTest 2: All values should be non-negative")
    assert (out >= 0).all()
    print(f"✓ Min value: {out.min().item():.6f}")

    # Test 3: Batch dimension
    print("\nTest 3: Batch processing")
    x = torch.randn(16, 20)
    out = softmax(x, dim=1)
    assert out.shape == x.shape
    assert torch.allclose(out.sum(dim=1), torch.ones(16))
    print(f"✓ Shape: {out.shape}")
    print(f"✓ Row sums: {out.sum(dim=1)[:5]}")

    # Test 4: Compare with PyTorch implementation
    print("\nTest 4: Compare with torch.softmax")
    x = torch.randn(32, 10)
    our_result = softmax(x, dim=1)
    torch_result = torch.softmax(x, dim=1)
    assert torch.allclose(our_result, torch_result)
    print(f"✓ Max difference: {(our_result - torch_result).abs().max().item():.10f}")

    # Test 5: Numerical stability
    print("\nTest 5: Numerical stability with large values")
    x = torch.tensor([[1000.0, 2000.0, 3000.0]])
    out = softmax(x)
    assert not torch.isnan(out).any()
    assert not torch.isinf(out).any()
    print(f"✓ Output: {out}")
    print(f"✓ No NaN or Inf values")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_softmax()
