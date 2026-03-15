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
    delta_ab = points_a[: , None, :] - points_b[None, :, :] # [m,n,d]
    return torch.norm(delta_ab, dim=-1)

    pass


if __name__ == '__main__':
    points_a = torch.rand(10,3)
    points_b = torch.rand(20,3)
    print(pairwise_distance(points_a, points_b))