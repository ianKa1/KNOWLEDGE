import torch
import torch.nn.functional as F

def conv2d(
    input: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor = None,
    stride: int = 1,
    padding: int = 0
) -> torch.Tensor:
    """
    Compute 2D convolution.

    Args:
        input: Input tensor of shape [batch_size, in_channels, height, width]
        weight: Kernel tensor of shape [out_channels, in_channels, kernel_h, kernel_w]
        bias: Optional bias of shape [out_channels]
        stride: Stride for convolution (default: 1)
        padding: Zero padding added to both sides (default: 0)

    Returns:
        Output tensor of shape [batch_size, out_channels, out_height, out_width]
    """
    _, _, kernel_h, kernel_w = weight.shape
    padded_input = F.pad(input, (padding, padding, padding, padding), mode='constant')
    unfold_input = padded_input.unfold(2, kernel_h, stride)
    unfold_input = unfold_input.unfold(3, kernel_w, stride)
    unfold_input = unfold_input.flatten(-2) # batch_size, in_channels, out_height, out_width, kernel_size
    print(unfold_input.shape)
    unfold_input = unfold_input.permute(0, 2, 3, 1, -1)
    unfold_input = unfold_input.flatten(-2) # batch_size, out_height, out_width, in_
    weight = weight.flatten(-3)
    output = unfold_input @ weight.T
    if bias is not None:
        output = output + bias
    output = output.permute(0, -1, 1, 2)
    return output

    pass


if __name__ == "__main__":
    batch_size, in_channels, height, width = 1, 2, 9, 9
    out_channels, kernel_size = 3, 3

    input_data = torch.randn(batch_size, in_channels, height, width)
    kernel = torch.randn(out_channels, in_channels, kernel_size, kernel_size)

    output = conv2d(input_data, kernel, stride=1, padding=0)
    print(output)