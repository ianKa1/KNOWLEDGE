# Problem 1: Implement Softmax

## Difficulty: Easy

## Problem Description

Implement the softmax function using PyTorch. The softmax function converts a vector of real numbers into a probability distribution.

## Function Signature

```python
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
    pass
```

## Mathematical Formula

```
softmax(x_i) = exp(x_i) / sum(exp(x_j)) for all j
```

**Numerical Stability**: Subtract max(x) before computing exponentials to avoid overflow.

## Examples

```python
# Example 1: 1D tensor
x = torch.tensor([1.0, 2.0, 3.0])
output = softmax(x)
# Expected: tensor([0.0900, 0.2447, 0.6652])

# Example 2: 2D tensor, apply along last dimension
x = torch.tensor([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])
output = softmax(x, dim=1)
# Expected:
# tensor([[0.0900, 0.2447, 0.6652],
#         [0.0900, 0.2447, 0.6652]])

# Example 3: Batch processing
x = torch.randn(32, 10)  # [batch_size, num_classes]
output = softmax(x, dim=1)
assert output.sum(dim=1).allclose(torch.ones(32))  # Should sum to 1
```

## Test Cases

```python
def test_softmax():
    # Test 1: Sum to 1
    x = torch.randn(100)
    out = softmax(x)
    assert torch.allclose(out.sum(), torch.tensor(1.0))

    # Test 2: Non-negative
    assert (out >= 0).all()

    # Test 3: Batch dimension
    x = torch.randn(16, 20)
    out = softmax(x, dim=1)
    assert out.shape == x.shape
    assert torch.allclose(out.sum(dim=1), torch.ones(16))
```

## Hints

1. Use `torch.exp()` for exponentials
2. For numerical stability: `x = x - x.max(dim=dim, keepdim=True)`
3. Use `torch.sum()` with `keepdim=True` to maintain tensor dimensions
4. Don't forget to handle the `dim` parameter correctly

## Expected Time

5-10 minutes

## Key Concepts

- Tensor operations
- Broadcasting
- Numerical stability
- Dimension handling with `keepdim`
