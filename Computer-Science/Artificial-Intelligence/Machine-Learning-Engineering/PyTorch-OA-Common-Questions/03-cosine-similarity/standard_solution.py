"""
Solution: Implement Cosine Similarity
Difficulty: Easy-Medium
Expected Time: 8-12 minutes
"""

import torch
import torch.nn.functional as F


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
    # Method 1: Manual computation
    # Compute L2 norms
    norm_A = torch.norm(A, dim=1, keepdim=True)  # [m, 1]
    norm_B = torch.norm(B, dim=1, keepdim=True)  # [n, 1]

    # Compute dot products (all pairs)
    dot_products = A @ B.T  # [m, n]

    # Normalize by product of norms
    # Add small epsilon to avoid division by zero
    epsilon = 1e-8
    similarity = dot_products / (norm_A * norm_B.T + epsilon)

    return similarity


# Alternative implementation using normalization first
def cosine_similarity_v2(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """Alternative implementation: normalize first, then dot product"""
    # Normalize vectors to unit length
    A_normalized = F.normalize(A, p=2, dim=1)
    B_normalized = F.normalize(B, p=2, dim=1)

    # Cosine similarity is just dot product of normalized vectors
    similarity = A_normalized @ B_normalized.T

    return similarity


# Test cases
def test_cosine_similarity():
    print("Running tests for cosine_similarity...\n")

    # Test 1: Range check [-1, 1]
    print("Test 1: Output should be in range [-1, 1]")
    A = torch.randn(20, 64)
    B = torch.randn(30, 64)
    sim = cosine_similarity(A, B)
    print(f"✓ Shape: {sim.shape}")
    print(f"✓ Min: {sim.min().item():.6f}, Max: {sim.max().item():.6f}")
    assert sim.min() >= -1.0 and sim.max() <= 1.0

    # Test 2: Identical vectors
    print("\nTest 2: Identical vectors should have similarity 1.0")
    A = torch.randn(10, 32)
    sim = cosine_similarity(A, A)
    diagonal = torch.diag(sim)
    assert torch.allclose(diagonal, torch.ones(10), atol=1e-5)
    print(f"✓ Diagonal values: {diagonal[:5]}")

    # Test 3: Orthogonal vectors
    print("\nTest 3: Orthogonal vectors should have similarity ~0")
    A = torch.tensor([[1.0, 0.0, 0.0]])
    B = torch.tensor([[0.0, 1.0, 0.0]])
    sim = cosine_similarity(A, B)
    assert torch.allclose(sim, torch.zeros_like(sim), atol=1e-5)
    print(f"✓ Similarity: {sim.item():.10f}")

    # Test 4: Opposite vectors
    print("\nTest 4: Opposite vectors should have similarity -1.0")
    A = torch.tensor([[1.0, 0.0, 0.0]])
    B = torch.tensor([[-1.0, 0.0, 0.0]])
    sim = cosine_similarity(A, B)
    assert torch.allclose(sim, torch.tensor([[-1.0]]), atol=1e-5)
    print(f"✓ Similarity: {sim.item():.6f}")

    # Test 5: Same direction vectors (different magnitude)
    print("\nTest 5: Same direction vectors should have similarity 1.0")
    A = torch.tensor([[1.0, 2.0, 3.0]])
    B = torch.tensor([[2.0, 4.0, 6.0]])  # Scaled version
    sim = cosine_similarity(A, B)
    assert torch.allclose(sim, torch.ones_like(sim), atol=1e-5)
    print(f"✓ Similarity: {sim.item():.6f}")

    # Test 6: Compare both implementations
    print("\nTest 6: Compare both implementations")
    A = torch.randn(50, 128)
    B = torch.randn(40, 128)

    sim_v1 = cosine_similarity(A, B)
    sim_v2 = cosine_similarity_v2(A, B)

    assert torch.allclose(sim_v1, sim_v2, atol=1e-5)
    print(f"✓ Max difference: {(sim_v1 - sim_v2).abs().max().item():.10f}")

    # Test 7: Compare with PyTorch's cosine_similarity (for single pairs)
    print("\nTest 7: Compare with PyTorch F.cosine_similarity")
    A = torch.randn(10, 64)
    B = torch.randn(10, 64)

    # PyTorch's cosine_similarity computes pairwise (not all pairs)
    our_diagonal = torch.diag(cosine_similarity(A, A))
    torch_result = F.cosine_similarity(A, A, dim=1)

    assert torch.allclose(our_diagonal, torch_result, atol=1e-5)
    print(f"✓ Results match for diagonal elements")

    # Test 8: Batch processing
    print("\nTest 8: Large batch processing")
    A = torch.randn(100, 512)
    B = torch.randn(50, 512)
    sim = cosine_similarity(A, B)
    assert sim.shape == (100, 50)
    print(f"✓ Output shape: {sim.shape}")
    print(f"✓ Memory efficient computation completed")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_cosine_similarity()
