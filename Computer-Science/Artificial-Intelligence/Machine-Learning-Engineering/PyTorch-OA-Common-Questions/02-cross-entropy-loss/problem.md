# Problem 2: Implement Cross Entropy Loss

## Difficulty: Medium

## Problem Description

Implement the cross-entropy loss function from scratch using PyTorch. This is one of the most common loss functions for classification tasks.

## Function Signature

```python
import torch

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
    pass
```

## Mathematical Formula

```
CE = -1/N * sum(log(softmax(logits)[i, targets[i]]))

where:
- N is batch size
- logits[i, targets[i]] is the logit for the true class
```

## Examples

```python
# Example 1: Simple case
logits = torch.tensor([[2.0, 1.0, 0.1],
                       [0.5, 2.5, 0.2]])
targets = torch.tensor([0, 1])  # First sample: class 0, second: class 1
loss = cross_entropy_loss(logits, targets)
# Expected: scalar tensor around 0.4-0.5

# Example 2: Perfect prediction
logits = torch.tensor([[10.0, 0.0, 0.0],
                       [0.0, 10.0, 0.0]])
targets = torch.tensor([0, 1])
loss = cross_entropy_loss(logits, targets)
# Expected: very small value (close to 0)

# Example 3: Batch processing
logits = torch.randn(64, 10)  # 64 samples, 10 classes
targets = torch.randint(0, 10, (64,))
loss = cross_entropy_loss(logits, targets)
# Expected: positive scalar
```

## Test Cases

```python
def test_cross_entropy():
    # Test 1: Compare with PyTorch built-in
    logits = torch.randn(32, 10)
    targets = torch.randint(0, 10, (32,))

    your_loss = cross_entropy_loss(logits, targets)
    pytorch_loss = torch.nn.functional.cross_entropy(logits, targets)

    assert torch.allclose(your_loss, pytorch_loss, atol=1e-5)

    # Test 2: Loss should be non-negative
    assert your_loss >= 0

    # Test 3: Perfect prediction
    logits = torch.eye(5) * 100  # One-hot with large values
    targets = torch.arange(5)
    loss = cross_entropy_loss(logits, targets)
    assert loss < 0.01  # Should be very small
```

## Hints

1. First apply softmax to logits
2. Use `torch.gather()` or indexing to select the probability for the correct class
3. Take the negative log: `-torch.log(probs)`
4. Average over the batch
5. For numerical stability, use log-softmax instead of softmax + log:
   ```python
   log_probs = logits - torch.logsumexp(logits, dim=1, keepdim=True)
   ```

## Expected Time

10-15 minutes

## Key Concepts

- Softmax computation
- Indexing/gathering tensors
- Logarithm for numerical stability
- Reduction (mean) over batches
- Log-sum-exp trick
