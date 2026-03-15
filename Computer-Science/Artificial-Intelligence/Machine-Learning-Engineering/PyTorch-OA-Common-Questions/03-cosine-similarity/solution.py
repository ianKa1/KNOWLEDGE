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

    A = F.normalize(A, dim=-1)
    B = F.normalize(B, dim=-1)
    return A @ B.T



if __name__ == '__main__':
    a = torch.rand(3,5)
    b = torch.rand(4,5)
    print(cosine_similarity(a, b))