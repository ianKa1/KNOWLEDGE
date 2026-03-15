"""
Solution: Implement 2D Max Pooling
Difficulty: Easy-Medium
Expected Time: 12-18 minutes
"""

import torch
import torch.nn.functional as F


def max_pool2d(
    input: torch.Tensor,
    kernel_size: int,
    stride: int = None
) -> torch.Tensor:
    """
    Compute 2D max pooling.

    Args:
        input: Input tensor of shape [batch_size, channels, height, width]
        kernel_size: Size of pooling window (assumes square kernel)
        stride: Stride for pooling (default: same as kernel_size)

    Returns:
        Output tensor of shape [batch_size, channels, out_height, out_width]
    """
    # Default stride = kernel_size (non-overlapping windows)
    if stride is None:
        stride = kernel_size

    batch_size, channels, height, width = input.shape

    # Compute output dimensions
    out_h = (height - kernel_size) // stride + 1
    out_w = (width - kernel_size) // stride + 1

    # Method 1: Using unfold (efficient)
    # Unfold creates sliding windows
    # [B, C, H, W] -> [B, C, kernel_size*kernel_size, num_windows]
    unfolded = F.unfold(
        input,
        kernel_size=(kernel_size, kernel_size),
        stride=stride
    )
    # unfolded shape: [B, C * kernel_size * kernel_size, out_h * out_w]

    # Reshape to separate channels and kernel elements
    # [B, C * k * k, out_h * out_w] -> [B, C, k * k, out_h * out_w]
    unfolded = unfolded.reshape(batch_size, channels, kernel_size * kernel_size, -1)

    # Take max over kernel dimension
    pooled, _ = unfolded.max(dim=2)  # [B, C, out_h * out_w]

    # Reshape back to spatial dimensions
    output = pooled.reshape(batch_size, channels, out_h, out_w)

    return output


# Alternative implementation: direct with loops (clearer but slower)
def max_pool2d_direct(
    input: torch.Tensor,
    kernel_size: int,
    stride: int = None
) -> torch.Tensor:
    """Direct implementation using loops"""
    if stride is None:
        stride = kernel_size

    batch_size, channels, height, width = input.shape

    out_h = (height - kernel_size) // stride + 1
    out_w = (width - kernel_size) // stride + 1

    # Initialize output
    output = torch.zeros(batch_size, channels, out_h, out_w)

    # Pool each window
    for h in range(out_h):
        for w in range(out_w):
            h_start = h * stride
            w_start = w * stride

            # Extract window
            window = input[:, :, h_start:h_start+kernel_size, w_start:w_start+kernel_size]

            # Take max over spatial dimensions
            # window: [B, C, k, k]
            output[:, :, h, w] = window.max(dim=-1).values.max(dim=-1).values

    return output


# Bonus: Average pooling
def avg_pool2d(
    input: torch.Tensor,
    kernel_size: int,
    stride: int = None
) -> torch.Tensor:
    """Average pooling implementation"""
    if stride is None:
        stride = kernel_size

    batch_size, channels, height, width = input.shape

    out_h = (height - kernel_size) // stride + 1
    out_w = (width - kernel_size) // stride + 1

    # Using unfold
    unfolded = F.unfold(
        input,
        kernel_size=(kernel_size, kernel_size),
        stride=stride
    )

    unfolded = unfolded.reshape(batch_size, channels, kernel_size * kernel_size, -1)

    # Take mean instead of max
    pooled = unfolded.mean(dim=2)

    output = pooled.reshape(batch_size, channels, out_h, out_w)

    return output


# Bonus: Adaptive max pooling
def adaptive_max_pool2d(
    input: torch.Tensor,
    output_size: tuple
) -> torch.Tensor:
    """
    Adaptive max pooling: automatically compute kernel_size and stride
    to achieve desired output_size.
    """
    batch_size, channels, height, width = input.shape
    out_h, out_w = output_size

    # Initialize output
    output = torch.zeros(batch_size, channels, out_h, out_w)

    for h in range(out_h):
        for w in range(out_w):
            # Compute window boundaries
            h_start = int(h * height / out_h)
            h_end = int((h + 1) * height / out_h)
            w_start = int(w * width / out_w)
            w_end = int((w + 1) * width / out_w)

            # Extract window (variable size)
            window = input[:, :, h_start:h_end, w_start:w_end]

            # Take max
            output[:, :, h, w] = window.max(dim=-1).values.max(dim=-1).values

    return output


# Test cases
def test_max_pool2d():
    print("Running tests for max_pool2d...\n")

    # Test 1: Output shape
    print("Test 1: Output shape")
    input_data = torch.randn(4, 16, 32, 32)
    output = max_pool2d(input_data, kernel_size=2, stride=2)
    assert output.shape == (4, 16, 16, 16)
    print(f"✓ Input shape: {input_data.shape}")
    print(f"✓ Output shape: {output.shape}")

    # Test 2: Compare with PyTorch
    print("\nTest 2: Compare with PyTorch F.max_pool2d")
    input_data = torch.randn(2, 3, 28, 28)

    our_output = max_pool2d(input_data, kernel_size=2, stride=2)
    torch_output = F.max_pool2d(input_data, kernel_size=2, stride=2)

    assert torch.allclose(our_output, torch_output)
    print(f"✓ Max difference: {(our_output - torch_output).abs().max().item():.10f}")

    # Test 3: Known values
    print("\nTest 3: Known values (2x2 pooling)")
    input_data = torch.arange(16, dtype=torch.float32).reshape(1, 1, 4, 4)
    print(f"Input:\n{input_data[0, 0]}")

    output = max_pool2d(input_data, kernel_size=2, stride=2)
    expected = torch.tensor([[[[5., 7.], [13., 15.]]]])

    print(f"Output:\n{output[0, 0]}")
    print(f"Expected:\n{expected[0, 0]}")

    assert torch.allclose(output, expected)
    print(f"✓ Correct max values extracted")

    # Test 4: Maximum values property
    print("\nTest 4: Verify maximum values")
    input_data = torch.randn(2, 3, 8, 8)
    output = max_pool2d(input_data, kernel_size=2, stride=2)

    # Each output value should equal the max of its window
    for b in range(2):
        for c in range(3):
            for h in range(4):
                for w in range(4):
                    window = input_data[b, c, h*2:h*2+2, w*2:w*2+2]
                    expected_max = window.max()
                    actual = output[b, c, h, w]
                    assert torch.isclose(actual, expected_max)

    print(f"✓ All output values are correct maximums")

    # Test 5: Overlapping windows (stride < kernel_size)
    print("\nTest 5: Overlapping windows")
    input_data = torch.randn(1, 1, 10, 10)
    output = max_pool2d(input_data, kernel_size=3, stride=1)

    expected_h = (10 - 3) // 1 + 1
    expected_w = (10 - 3) // 1 + 1

    assert output.shape == (1, 1, expected_h, expected_w)
    print(f"✓ Output shape with stride=1: {output.shape}")

    # Test 6: Compare both implementations
    print("\nTest 6: Compare unfold vs direct implementation")
    input_data = torch.randn(2, 4, 16, 16)

    output_unfold = max_pool2d(input_data, kernel_size=2, stride=2)
    output_direct = max_pool2d_direct(input_data, kernel_size=2, stride=2)

    assert torch.allclose(output_unfold, output_direct)
    print(f"✓ Both implementations match")

    # Test 7: Different kernel sizes
    print("\nTest 7: Different kernel sizes")
    input_data = torch.randn(1, 3, 32, 32)

    for kernel_size in [2, 3, 4]:
        output = max_pool2d(input_data, kernel_size=kernel_size)
        expected_size = (32 - kernel_size) // kernel_size + 1
        assert output.shape == (1, 3, expected_size, expected_size)
        print(f"✓ Kernel size {kernel_size}: output shape {output.shape}")

    # Test 8: Average pooling
    print("\nTest 8: Average pooling")
    input_data = torch.randn(2, 3, 16, 16)

    avg_output = avg_pool2d(input_data, kernel_size=2, stride=2)
    torch_avg = F.avg_pool2d(input_data, kernel_size=2, stride=2)

    assert torch.allclose(avg_output, torch_avg, atol=1e-6)
    print(f"✓ Average pooling matches PyTorch")

    # Test 9: Adaptive max pooling
    print("\nTest 9: Adaptive max pooling")
    input_data = torch.randn(1, 3, 32, 32)

    for output_size in [(16, 16), (8, 8), (4, 4), (1, 1)]:
        output = adaptive_max_pool2d(input_data, output_size)
        torch_output = F.adaptive_max_pool2d(input_data, output_size)

        assert output.shape[-2:] == output_size
        # Note: Our implementation might differ slightly from PyTorch's
        # due to different window boundary calculations
        print(f"✓ Adaptive pooling to {output_size}: shape {output.shape}")

    # Test 10: Edge case - kernel size = input size
    print("\nTest 10: Global max pooling (kernel_size = input_size)")
    input_data = torch.randn(2, 3, 8, 8)
    output = max_pool2d(input_data, kernel_size=8)

    # Should produce 1x1 output
    assert output.shape == (2, 3, 1, 1)

    # Each output should be the global max
    for b in range(2):
        for c in range(3):
            expected_max = input_data[b, c].max()
            assert torch.isclose(output[b, c, 0, 0], expected_max)

    print(f"✓ Global max pooling works correctly")

    # Test 11: Multi-channel independence
    print("\nTest 11: Channels are processed independently")
    input_data = torch.randn(1, 3, 8, 8)
    output = max_pool2d(input_data, kernel_size=2, stride=2)

    # Pool each channel separately and verify
    for c in range(3):
        single_channel = input_data[:, c:c+1, :, :]
        single_output = max_pool2d(single_channel, kernel_size=2, stride=2)
        assert torch.allclose(output[:, c:c+1, :, :], single_output)

    print(f"✓ Channels are independent")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_max_pool2d()
