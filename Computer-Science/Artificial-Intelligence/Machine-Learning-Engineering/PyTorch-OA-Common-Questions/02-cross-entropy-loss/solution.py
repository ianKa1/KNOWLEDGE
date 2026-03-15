import torch
import torch.nn.functional as F

def softmax(logits: torch.Tensor, dim=-1) -> torch.Tensor:

    exp_logits = torch.exp(logits - logits.max(dim=dim, keepdim=True).values)
    return exp_logits / exp_logits.sum(dim=dim, keepdim=True)

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
    _, num_classes = logits.shape
    y = F.one_hot(targets, num_classes=num_classes) # [batch_size, num_classes]
    x = softmax(logits)
    ce_loss = -(y*(torch.log(x))).sum(dim=-1)
    return ce_loss.mean()

if __name__ == '__main__':
    num_classes = 10
    logits = torch.rand(5, num_classes)
    targets = torch.randint(0, num_classes, (5,))

    ce_loss = cross_entropy_loss(logits, targets)
    print(ce_loss.item())
