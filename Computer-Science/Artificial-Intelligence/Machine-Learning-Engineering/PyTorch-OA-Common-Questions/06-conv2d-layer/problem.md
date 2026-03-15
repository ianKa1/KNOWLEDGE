# Problem 6: Implement 2D Convolution Layer

## Difficulty: Medium

## Problem Description

Implement a 2D convolutional layer from scratch using PyTorch. This is a fundamental building block of CNNs used extensively in computer vision and increasingly in 3D AI (e.g., multi-view 3D reconstruction, texture generation).

## Function Signature

```python
import torch

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
    pass
```

## Mathematical Formula

```
output[b, c_out, h, w] = sum over (c_in, kh, kw) of:
    input[b, c_in, h*stride + kh - padding, w*stride + kw - padding] * weight[c_out, c_in, kh, kw]
+ bias[c_out]

Output dimensions:
out_height = (height + 2*padding - kernel_h) // stride + 1
out_width = (width + 2*padding - kernel_w) // stride + 1
```

## Examples

```python
# Example 1: Simple 3x3 convolution
batch_size, in_channels, height, width = 1, 1, 5, 5
out_channels, kernel_size = 1, 3

input_data = torch.randn(batch_size, in_channels, height, width)
kernel = torch.randn(out_channels, in_channels, kernel_size, kernel_size)

output = conv2d(input_data, kernel, stride=1, padding=0)
# Expected shape: [1, 1, 3, 3]

# Example 2: Multi-channel convolution with padding
batch_size, in_channels, height, width = 2, 3, 28, 28
out_channels, kernel_size = 16, 3

input_data = torch.randn(batch_size, in_channels, height, width)
kernel = torch.randn(out_channels, in_channels, kernel_size, kernel_size)
bias = torch.randn(out_channels)

output = conv2d(input_data, kernel, bias, stride=1, padding=1)
# Expected shape: [2, 16, 28, 28]  # Same size due to padding=1

# Example 3: Strided convolution (downsampling)
output = conv2d(input_data, kernel, bias, stride=2, padding=1)
# Expected shape: [2, 16, 14, 14]  # Half size due to stride=2
```

## Test Cases

```python
def test_conv2d():
    # Test 1: Output shape calculation
    input_data = torch.randn(1, 3, 32, 32)
    kernel = torch.randn(16, 3, 3, 3)
    output = conv2d(input_data, kernel, stride=1, padding=1)
    assert output.shape == (1, 16, 32, 32)

    # Test 2: Compare with PyTorch F.conv2d
    import torch.nn.functional as F
    input_data = torch.randn(2, 3, 28, 28)
    kernel = torch.randn(8, 3, 5, 5)
    bias = torch.randn(8)

    our_output = conv2d(input_data, kernel, bias, stride=2, padding=2)
    torch_output = F.conv2d(input_data, kernel, bias, stride=2, padding=2)

    assert torch.allclose(our_output, torch_output, atol=1e-5)

    # Test 3: Identity kernel (should preserve input)
    # For single channel, 3x3 kernel with center=1, rest=0
```

## Hints

1. **Add padding**: Use `torch.nn.functional.pad()` or `torch.pad()`
   ```python
   if padding > 0:
       input = torch.nn.functional.pad(input, (padding, padding, padding, padding))
   ```

2. **Use unfold for efficiency** (advanced approach):
   ```python
   # Unfold creates sliding windows
   unfolded = torch.nn.functional.unfold(input, kernel_size=(kh, kw), stride=stride)
   ```

3. **Direct approach** (easier to understand):
   ```python
   # Loop over output positions
   for h in range(out_height):
       for w in range(out_width):
           h_start = h * stride
           w_start = w * stride
           window = input[:, :, h_start:h_start+kh, w_start:w_start+kw]
           output[:, :, h, w] = (window * kernel).sum(dim=[2, 3])
   ```

4. **For batch and channel dimensions**, use broadcasting or reshape operations

5. **Add bias at the end** after convolution computation

## Expected Time

18-25 minutes

## Key Concepts

- Sliding window operations
- Padding and stride
- Multi-channel operations
- Efficient tensor reshaping
- Understanding conv output size formula

## Why This Matters for 3D AI

Convolutions are used in:
- **Multi-view 3D reconstruction**: Process 2D images before 3D fusion
- **Texture generation**: Generate textures for 3D models
- **2D feature extraction**: Extract features from rendered views (NeRF, etc.)
- **UV map processing**: Apply convolutions on unwrapped 3D textures
- **Depth map processing**: Convolve depth maps for 3D understanding

## Bonus Challenge

Implement 3D convolution for volumetric data:
```python
def conv3d(input, weight, bias=None, stride=1, padding=0):
    # input: [B, C_in, D, H, W]
    # weight: [C_out, C_in, kD, kH, kW]
    # output: [B, C_out, D_out, H_out, W_out]
    pass
```
