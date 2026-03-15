# Problem 4: Implement Pairwise Euclidean Distance

## Difficulty: Medium

## Problem Description

Implement pairwise Euclidean distance between two sets of points using PyTorch. This is commonly used in 3D geometry processing, clustering, and k-NN algorithms.

## Function Signature

```python
import torch

def pairwise_distance(points_a: torch.Tensor, points_b: torch.Tensor) -> torch.Tensor:
    """
    Compute pairwise Euclidean distances between points in two sets.

    Args:
        points_a: Tensor of shape [m, d] (m points in d-dimensional space)
        points_b: Tensor of shape [n, d] (n points in d-dimensional space)

    Returns:
        Tensor of shape [m, n] where output[i, j] is the Euclidean distance
        between points_a[i] and points_b[j]
    """
    
    pass
```

## Mathematical Formula

```
dist(a, b) = sqrt(sum((a - b)^2))

Or equivalently (expansion of squared L2 distance):
dist(a, b)^2 = ||a||^2 + ||b||^2 - 2 * (a · b)
```

## Examples

```python
# Example 1: 2D points
points_a = torch.tensor([[0.0, 0.0],
                         [1.0, 1.0]])
points_b = torch.tensor([[0.0, 0.0],
                         [3.0, 4.0]])
dist = pairwise_distance(points_a, points_b)
# Expected:
# tensor([[0.0000, 5.0000],
#         [1.4142, 3.6056]])

# Example 2: 3D point cloud (typical in 3D AI)
points_a = torch.randn(100, 3)  # 100 3D points
points_b = torch.randn(50, 3)   # 50 3D points
dist = pairwise_distance(points_a, points_b)
# Expected shape: [100, 50]

# Example 3: Batch of point clouds
batch_size, num_points, dim = 16, 1024, 3
points_a = torch.randn(batch_size, num_points, dim)
# For batched version, you might need to adapt the function
```

## Test Cases

```python
def test_pairwise_distance():
    # Test 1: Distance to self should be 0
    points = torch.randn(20, 3)
    dist = pairwise_distance(points, points)
    assert torch.allclose(torch.diag(dist), torch.zeros(20), atol=1e-5)

    # Test 2: Non-negative
    points_a = torch.randn(30, 3)
    points_b = torch.randn(40, 3)
    dist = pairwise_distance(points_a, points_b)
    assert (dist >= 0).all()

    # Test 3: Symmetric
    # dist(a, b) should equal dist(b, a)
    points_a = torch.randn(10, 5)
    points_b = torch.randn(10, 5)
    dist_ab = pairwise_distance(points_a, points_b)
    dist_ba = pairwise_distance(points_b, points_a)
    assert torch.allclose(dist_ab, dist_ba.T)
```

## Hints

**Method 1: Expansion formula (more efficient)**
```python
# ||a||^2: [m, 1]
# ||b||^2: [n, 1]
# 2 * (a · b): [m, n]
a_squared = (points_a ** 2).sum(dim=1, keepdim=True)
b_squared = (points_b ** 2).sum(dim=1, keepdim=True)
ab = points_a @ points_b.T
dist_squared = a_squared + b_squared.T - 2 * ab
dist = torch.sqrt(torch.clamp(dist_squared, min=0))  # clamp for numerical stability
```

**Method 2: Direct computation (simpler but slower)**
```python
# Use broadcasting to compute all pairwise differences
# points_a: [m, d] -> [m, 1, d]
# points_b: [n, d] -> [1, n, d]
# diff: [m, n, d]
```

## Expected Time

12-18 minutes

## Key Concepts

- Matrix multiplication for dot products
- Broadcasting
- Numerical stability (`torch.clamp` before `sqrt`)
- Memory efficiency (avoid creating large intermediate tensors)
- Understanding the expansion formula

## 3D AI Context

This is especially important for 3D geometry processing:
- **Point cloud nearest neighbor**: Find closest points
- **Mesh vertex distance**: Compute distances between mesh vertices
- **Chamfer distance**: Used in 3D reconstruction metrics
