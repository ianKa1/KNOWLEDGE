"""
Solution: Implement Pairwise Euclidean Distance
Difficulty: Medium
Expected Time: 12-18 minutes
"""

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
    # Method 1: Efficient expansion formula
    # ||a - b||^2 = ||a||^2 + ||b||^2 - 2(a · b)

    # Compute squared norms
    a_squared = (points_a ** 2).sum(dim=1, keepdim=True)  # [m, 1]
    b_squared = (points_b ** 2).sum(dim=1, keepdim=True)  # [n, 1]

    # Compute dot products
    ab = points_a @ points_b.T  # [m, n]

    # Compute squared distances
    dist_squared = a_squared + b_squared.T - 2 * ab  # [m, n]

    # Take square root (clamp to avoid numerical errors)
    # Small negative values can occur due to floating point precision
    dist = torch.sqrt(torch.clamp(dist_squared, min=0.0))

    return dist


# Alternative implementation: direct computation (slower but clearer)
def pairwise_distance_v2(points_a: torch.Tensor, points_b: torch.Tensor) -> torch.Tensor:
    """Alternative implementation using broadcasting"""
    # Expand dimensions for broadcasting
    # points_a: [m, d] -> [m, 1, d]
    # points_b: [n, d] -> [1, n, d]
    a_expanded = points_a.unsqueeze(1)  # [m, 1, d]
    b_expanded = points_b.unsqueeze(0)  # [1, n, d]

    # Compute all pairwise differences
    diff = a_expanded - b_expanded  # [m, n, d]

    # Compute Euclidean distance
    dist = torch.norm(diff, dim=2)  # [m, n]

    return dist


# Test cases
def test_pairwise_distance():
    print("Running tests for pairwise_distance...\n")

    # Test 1: Distance to self should be 0
    print("Test 1: Distance to self should be 0")
    points = torch.randn(20, 3)
    dist = pairwise_distance(points, points)
    diagonal = torch.diag(dist)
    assert torch.allclose(diagonal, torch.zeros(20), atol=1e-5)
    print(f"✓ Diagonal distances: {diagonal[:5]}")

    # Test 2: Non-negative
    print("\nTest 2: All distances should be non-negative")
    points_a = torch.randn(30, 3)
    points_b = torch.randn(40, 3)
    dist = pairwise_distance(points_a, points_b)
    assert (dist >= 0).all()
    print(f"✓ Min distance: {dist.min().item():.6f}")
    print(f"✓ Max distance: {dist.max().item():.6f}")

    # Test 3: Symmetric (dist(a, b) == dist(b, a))
    print("\nTest 3: Symmetry check")
    points_a = torch.randn(10, 5)
    points_b = torch.randn(10, 5)
    dist_ab = pairwise_distance(points_a, points_b)
    dist_ba = pairwise_distance(points_b, points_a)
    assert torch.allclose(dist_ab, dist_ba.T, atol=1e-5)
    print(f"✓ dist(a, b) == dist(b, a)")

    # Test 4: Known distances (2D)
    print("\nTest 4: Known 2D distances")
    points_a = torch.tensor([[0.0, 0.0],
                             [1.0, 1.0]])
    points_b = torch.tensor([[0.0, 0.0],
                             [3.0, 4.0]])
    dist = pairwise_distance(points_a, points_b)

    # Expected:
    # [0,0] to [0,0] = 0
    # [0,0] to [3,4] = 5
    # [1,1] to [0,0] = sqrt(2) ≈ 1.414
    # [1,1] to [3,4] = sqrt(4+9) ≈ 3.606
    expected = torch.tensor([[0.0, 5.0],
                            [1.4142, 3.6056]])
    assert torch.allclose(dist, expected, atol=1e-3)
    print(f"✓ Distance matrix:\n{dist}")

    # Test 5: Compare both implementations
    print("\nTest 5: Compare both implementations")
    points_a = torch.randn(50, 10)
    points_b = torch.randn(30, 10)

    dist_v1 = pairwise_distance(points_a, points_b)
    dist_v2 = pairwise_distance_v2(points_a, points_b)

    assert torch.allclose(dist_v1, dist_v2, atol=1e-5)
    print(f"✓ Max difference: {(dist_v1 - dist_v2).abs().max().item():.10f}")

    # Test 6: 3D point clouds (typical in 3D AI)
    print("\nTest 6: 3D point clouds")
    points_a = torch.randn(100, 3)  # 100 3D points
    points_b = torch.randn(50, 3)   # 50 3D points
    dist = pairwise_distance(points_a, points_b)
    assert dist.shape == (100, 50)
    print(f"✓ Output shape: {dist.shape}")
    print(f"✓ Mean distance: {dist.mean().item():.6f}")

    # Test 7: High-dimensional embeddings
    print("\nTest 7: High-dimensional embeddings")
    points_a = torch.randn(200, 512)
    points_b = torch.randn(150, 512)
    dist = pairwise_distance(points_a, points_b)
    assert dist.shape == (200, 150)
    print(f"✓ Output shape: {dist.shape}")

    # Test 8: Triangle inequality
    print("\nTest 8: Triangle inequality: d(a,c) <= d(a,b) + d(b,c)")
    points = torch.randn(3, 5)
    dist = pairwise_distance(points, points)
    # Check d(0,2) <= d(0,1) + d(1,2)
    d_02 = dist[0, 2]
    d_01 = dist[0, 1]
    d_12 = dist[1, 2]
    assert d_02 <= d_01 + d_12 + 1e-5  # Small epsilon for numerical errors
    print(f"✓ d(0,2)={d_02:.4f} <= d(0,1)={d_01:.4f} + d(1,2)={d_12:.4f} = {d_01+d_12:.4f}")

    # Test 9: Compare with torch.cdist
    print("\nTest 9: Compare with torch.cdist")
    points_a = torch.randn(20, 8)
    points_b = torch.randn(15, 8)

    our_dist = pairwise_distance(points_a, points_b)
    torch_dist = torch.cdist(points_a, points_b, p=2)

    assert torch.allclose(our_dist, torch_dist, atol=1e-5)
    print(f"✓ Max difference with torch.cdist: {(our_dist - torch_dist).abs().max().item():.10f}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_pairwise_distance()
