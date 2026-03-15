# Problem 3: Implement Cosine Similarity

## Difficulty: Easy-Medium

## Problem Description

Implement pairwise cosine similarity between two sets of vectors using PyTorch. Cosine similarity is commonly used in ML for measuring vector similarity.

## Function Signature

```python
import torch

def cosine_similarity(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """
    Compute pairwise cosine similarity between vectors in A and B.

    Args:
        A: Tensor of shape [m, d] (m vectors of dimension d)
        B: Tensor of shape [n, d] (n vectors of dimension d)

    Returns:
        Tensor of shape [m, n] where output[i, j] is the cosine similarity
        between A[i] and B[j]
    """
    pass
```

## Mathematical Formula

```
cosine_sim(a, b) = (a · b) / (||a|| * ||b||)

where:
- a · b is the dot product
- ||a|| is the L2 norm of vector a
```

## Examples

```python
# Example 1: Same vectors -> similarity = 1
A = torch.tensor([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0]])
B = torch.tensor([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0]])
sim = cosine_similarity(A, B)
# Expected:
# tensor([[1.0, 0.0],
#         [0.0, 1.0]])

# Example 2: Orthogonal vectors -> similarity = 0
A = torch.tensor([[1.0, 0.0]])
B = torch.tensor([[0.0, 1.0]])
sim = cosine_similarity(A, B)
# Expected: tensor([[0.0]])

# Example 3: Opposite vectors -> similarity = -1
A = torch.tensor([[1.0, 0.0]])
B = torch.tensor([[-1.0, 0.0]])
sim = cosine_similarity(A, B)
# Expected: tensor([[-1.0]])

# Example 4: Batch processing
A = torch.randn(100, 512)  # 100 embeddings
B = torch.randn(50, 512)   # 50 embeddings
sim = cosine_similarity(A, B)
# Expected shape: [100, 50]
```

## Test Cases

```python
def test_cosine_similarity():
    # Test 1: Range check [-1, 1]
    A = torch.randn(20, 64)
    B = torch.randn(30, 64)
    sim = cosine_similarity(A, B)
    assert sim.min() >= -1.0 and sim.max() <= 1.0

    # Test 2: Identical vectors
    A = torch.randn(10, 32)
    sim = cosine_similarity(A, A)
    assert torch.allclose(torch.diag(sim), torch.ones(10))

    # Test 3: Shape
    assert sim.shape == (20, 30)
```

## Hints

1. Compute dot products: `A @ B.T` gives you all pairwise dot products
2. Compute norms: `torch.norm(A, dim=1)` for row-wise L2 norm
3. Combine: `(A @ B.T) / (norm_A.unsqueeze(1) * norm_B.unsqueeze(0))`
4. Handle edge case: add small epsilon to avoid division by zero
5. Alternative: Use `torch.nn.functional.normalize()` first

## Expected Time

8-12 minutes

## Key Concepts

- Matrix multiplication (`@` or `torch.matmul`)
- Broadcasting
- L2 norm computation
- Dimension handling with `unsqueeze`
- Numerical stability (epsilon)
