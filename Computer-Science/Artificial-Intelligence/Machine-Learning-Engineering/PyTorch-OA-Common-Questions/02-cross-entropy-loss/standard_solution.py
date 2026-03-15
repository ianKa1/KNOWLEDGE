"""
Solution: Implement Cross Entropy Loss
Difficulty: Medium
Expected Time: 10-15 minutes
"""

import torch
import torch.nn.functional as F


def cross_entropy_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """
    Compute cross-entropy loss between logits and targets.

    Args:
        logits: Raw model outputs of shape [batch_size, num_classes]
        targets: Ground truth class indices of shape [batch_size]
                 (integer values in range [0, num_classes-1])

    Returns:
        Scalar tensor representing the mean loss across the batch
    """
    # Method 1: Using log-softmax for numerical stability
    # This is more stable than computing softmax then log
    log_probs = logits - torch.logsumexp(logits, dim=1, keepdim=True)

    # Gather the log probabilities for the correct classes
    # targets: [batch_size] -> [batch_size, 1]
    # log_probs: [batch_size, num_classes]
    batch_size = logits.shape[0]
    target_log_probs = log_probs[torch.arange(batch_size), targets]

    # Negative log likelihood, averaged over batch
    loss = -target_log_probs.mean()

    return loss


# Alternative implementation using torch.gather
def cross_entropy_loss_v2(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """Alternative implementation using torch.gather"""
    # Log-softmax
    log_probs = torch.log_softmax(logits, dim=1)

    # Gather correct class probabilities
    target_log_probs = torch.gather(log_probs, 1, targets.unsqueeze(1))

    # Negative log likelihood
    loss = -target_log_probs.mean()

    return loss


# Test cases
def test_cross_entropy():
    print("Running tests for cross_entropy_loss...\n")

    # Test 1: Compare with PyTorch built-in
    print("Test 1: Compare with PyTorch F.cross_entropy")
    logits = torch.randn(32, 10)
    targets = torch.randint(0, 10, (32,))

    our_loss = cross_entropy_loss(logits, targets)
    pytorch_loss = F.cross_entropy(logits, targets)

    assert torch.allclose(our_loss, pytorch_loss, atol=1e-5)
    print(f"✓ Our loss: {our_loss.item():.6f}")
    print(f"✓ PyTorch loss: {pytorch_loss.item():.6f}")
    print(f"✓ Difference: {abs(our_loss.item() - pytorch_loss.item()):.10f}")

    # Test 2: Loss should be non-negative
    print("\nTest 2: Loss should be non-negative")
    assert our_loss >= 0
    print(f"✓ Loss: {our_loss.item():.6f} >= 0")

    # Test 3: Perfect prediction
    print("\nTest 3: Perfect prediction should give very small loss")
    logits = torch.eye(5) * 100  # One-hot with large values
    targets = torch.arange(5)
    loss = cross_entropy_loss(logits, targets)
    assert loss < 0.01
    print(f"✓ Loss for perfect prediction: {loss.item():.10f}")

    # Test 4: Completely wrong prediction
    print("\nTest 4: Wrong prediction should give larger loss")
    logits = torch.zeros(5, 5)
    logits[:, 0] = 100  # Always predict class 0
    targets = torch.tensor([1, 2, 3, 4, 4])  # Never class 0
    loss = cross_entropy_loss(logits, targets)
    print(f"✓ Loss for wrong prediction: {loss.item():.6f}")
    assert loss > 1.0

    # Test 5: Compare v2 implementation
    print("\nTest 5: Compare both implementations")
    logits = torch.randn(64, 20)
    targets = torch.randint(0, 20, (64,))

    loss_v1 = cross_entropy_loss(logits, targets)
    loss_v2 = cross_entropy_loss_v2(logits, targets)

    assert torch.allclose(loss_v1, loss_v2, atol=1e-6)
    print(f"✓ V1 loss: {loss_v1.item():.6f}")
    print(f"✓ V2 loss: {loss_v2.item():.6f}")

    # Test 6: Random prediction baseline
    print("\nTest 6: Random prediction baseline")
    logits = torch.randn(100, 10)
    targets = torch.randint(0, 10, (100,))
    loss = cross_entropy_loss(logits, targets)
    # For random predictions on 10 classes, loss should be around -log(0.1) ≈ 2.3
    print(f"✓ Loss for random logits: {loss.item():.6f}")
    print(f"✓ Expected ~{-torch.log(torch.tensor(0.1)).item():.2f} for uniform distribution over 10 classes")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_cross_entropy()
