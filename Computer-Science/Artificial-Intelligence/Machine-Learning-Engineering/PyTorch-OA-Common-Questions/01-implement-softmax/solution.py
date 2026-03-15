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
    # e^{x} / sum(e^{x})
    exp_x = torch.exp(x - x.max(dim=dim, keepdim=True).values)
    return exp_x / exp_x.sum(dim=dim, keepdim=True)

if __name__ == '__main__':
    logits = torch.rand(10, 16)
    print(softmax(logits))


