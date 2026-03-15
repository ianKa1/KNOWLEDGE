"""
Solution: Implement 2D Convolution Layer
Difficulty: Medium
Expected Time: 18-25 minutes
"""

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
    batch_size, in_channels, height, width = input.shape
    out_channels, _, kernel_h, kernel_w = weight.shape

    # Add padding if needed
    if padding > 0:
        input = F.pad(input, (padding, padding, padding, padding), mode='constant', value=0)

    # Recompute dimensions after padding
    _, _, padded_h, padded_w = input.shape

    # Compute output dimensions
    out_h = (padded_h - kernel_h) // stride + 1
    out_w = (padded_w - kernel_w) // stride + 1

    # Method 1: Using unfold (efficient)
    # Unfold creates sliding windows
    # [B, C_in, H, W] -> [B, C_in * kH * kW, num_windows]
    unfolded = F.unfold(input, kernel_size=(kernel_h, kernel_w), stride=stride)
    # unfolded shape: [B, in_channels * kH * kW, out_h * out_w]

    # Reshape weight for matrix multiplication
    # [C_out, C_in, kH, kW] -> [C_out, C_in * kH * kW]
    weight_reshaped = weight.reshape(out_channels, -1)

    # Matrix multiplication: [C_out, C_in*kH*kW] @ [B, C_in*kH*kW, out_h*out_w]
    # -> [B, C_out, out_h * out_w]
    output = weight_reshaped @ unfolded

    # Reshape to spatial dimensions
    output = output.reshape(batch_size, out_channels, out_h, out_w)

    # Add bias if provided
    if bias is not None:
        # bias shape: [C_out] -> [1, C_out, 1, 1] for broadcasting
        output = output + bias.reshape(1, -1, 1, 1)

    return output


# Alternative implementation: direct convolution (easier to understand but slower)
def conv2d_direct(
    input: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor = None,
    stride: int = 1,
    padding: int = 0
) -> torch.Tensor:
    """Direct implementation using loops (clearer but slower)"""
    batch_size, in_channels, height, width = input.shape
    out_channels, _, kernel_h, kernel_w = weight.shape

    # Add padding
    if padding > 0:
        input = F.pad(input, (padding, padding, padding, padding))

    _, _, padded_h, padded_w = input.shape

    # Compute output dimensions
    out_h = (padded_h - kernel_h) // stride + 1
    out_w = (padded_w - kernel_w) // stride + 1

    # Initialize output
    output = torch.zeros(batch_size, out_channels, out_h, out_w)

    # Convolve
    for h in range(out_h):
        for w in range(out_w):
            h_start = h * stride
            w_start = w * stride

            # Extract window: [B, C_in, kH, kW]
            window = input[:, :, h_start:h_start+kernel_h, w_start:w_start+kernel_w]

            # Compute convolution for all output channels
            # window: [B, C_in, kH, kW]
            # weight: [C_out, C_in, kH, kW]
            # We want: [B, C_out]

            # Expand dimensions for broadcasting
            # window: [B, 1, C_in, kH, kW]
            # weight: [1, C_out, C_in, kH, kW]
            conv_result = (window.unsqueeze(1) * weight.unsqueeze(0)).sum(dim=[2, 3, 4])
            output[:, :, h, w] = conv_result

    # Add bias
    if bias is not None:
        output = output + bias.reshape(1, -1, 1, 1)

    return output


# Test cases
def test_conv2d():
    print("Running tests for conv2d...\n")

    # Test 1: Output shape calculation
    print("Test 1: Output shape with padding")
    input_data = torch.randn(1, 3, 32, 32)
    kernel = torch.randn(16, 3, 3, 3)
    output = conv2d(input_data, kernel, stride=1, padding=1)
    assert output.shape == (1, 16, 32, 32)
    print(f"✓ Input: {input_data.shape}, Kernel: {kernel.shape}")
    print(f"✓ Output: {output.shape}")

    # Test 2: Compare with PyTorch F.conv2d
    print("\nTest 2: Compare with PyTorch F.conv2d")
    input_data = torch.randn(2, 3, 28, 28)
    kernel = torch.randn(8, 3, 5, 5)
    bias = torch.randn(8)

    our_output = conv2d(input_data, kernel, bias, stride=2, padding=2)
    torch_output = F.conv2d(input_data, kernel, bias, stride=2, padding=2)

    assert torch.allclose(our_output, torch_output, atol=1e-5)
    print(f"✓ Max difference: {(our_output - torch_output).abs().max().item():.10f}")

    # Test 3: No padding, stride=1
    print("\nTest 3: No padding, stride=1")
    input_data = torch.randn(1, 1, 5, 5)
    kernel = torch.randn(1, 1, 3, 3)

    our_output = conv2d(input_data, kernel, stride=1, padding=0)
    torch_output = F.conv2d(input_data, kernel, stride=1, padding=0)

    assert torch.allclose(our_output, torch_output, atol=1e-5)
    assert our_output.shape == (1, 1, 3, 3)
    print(f"✓ Output shape: {our_output.shape}")

    # Test 4: Strided convolution (downsampling)
    print("\nTest 4: Strided convolution")
    input_data = torch.randn(4, 3, 64, 64)
    kernel = torch.randn(16, 3, 3, 3)

    output = conv2d(input_data, kernel, stride=2, padding=1)
    assert output.shape == (4, 16, 32, 32)
    print(f"✓ Downsampled from {input_data.shape} to {output.shape}")

    # Test 5: Identity kernel
    print("\nTest 5: Identity kernel (should preserve center pixel)")
    input_data = torch.randn(1, 1, 5, 5)

    # Create identity kernel (1 at center, 0 elsewhere)
    kernel = torch.zeros(1, 1, 3, 3)
    kernel[0, 0, 1, 1] = 1.0

    output = conv2d(input_data, kernel, stride=1, padding=1)

    # With padding=1, output size should match input size
    # Center of each window should equal corresponding input pixel
    assert torch.allclose(output, input_data, atol=1e-5)
    print(f"✓ Identity kernel preserves input")

    # Test 6: Bias addition
    print("\nTest 6: Bias addition")
    input_data = torch.randn(2, 3, 28, 28)
    kernel = torch.randn(8, 3, 3, 3)
    bias = torch.randn(8)

    output_with_bias = conv2d(input_data, kernel, bias, stride=1, padding=1)
    output_no_bias = conv2d(input_data, kernel, None, stride=1, padding=1)

    # Difference should be exactly the bias (broadcasted)
    diff = output_with_bias - output_no_bias
    # Each channel should have constant difference equal to bias value
    for c in range(8):
        channel_diff = diff[:, c, :, :]
        assert torch.allclose(channel_diff, torch.full_like(channel_diff, bias[c]))
    print(f"✓ Bias correctly added to each channel")

    # Test 7: Compare both implementations
    print("\nTest 7: Compare unfold vs direct implementation")
    input_data = torch.randn(2, 3, 16, 16)
    kernel = torch.randn(4, 3, 3, 3)

    output_unfold = conv2d(input_data, kernel, stride=1, padding=1)
    output_direct = conv2d_direct(input_data, kernel, stride=1, padding=1)

    assert torch.allclose(output_unfold, output_direct, atol=1e-5)
    print(f"✓ Both implementations match")

    # Test 8: Large batch
    print("\nTest 8: Large batch processing")
    input_data = torch.randn(32, 3, 32, 32)
    kernel = torch.randn(64, 3, 7, 7)

    output = conv2d(input_data, kernel, stride=2, padding=3)
    assert output.shape == (32, 64, 16, 16)
    print(f"✓ Batch of {input_data.shape[0]} processed successfully")

    # Test 9: Different kernel sizes
    print("\nTest 9: Non-square kernel")
    input_data = torch.randn(1, 3, 28, 28)
    kernel = torch.randn(8, 3, 3, 5)  # 3x5 kernel

    our_output = conv2d(input_data, kernel, stride=1, padding=0)
    torch_output = F.conv2d(input_data, kernel, stride=1, padding=0)

    assert torch.allclose(our_output, torch_output, atol=1e-5)
    print(f"✓ Non-square kernel (3x5) works correctly")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_conv2d()
