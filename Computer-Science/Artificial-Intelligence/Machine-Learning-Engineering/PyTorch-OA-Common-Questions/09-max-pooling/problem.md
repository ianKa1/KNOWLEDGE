# Problem 9: Implement 2D Max Pooling

## Difficulty: Easy-Medium

## Problem Description

Implement 2D max pooling operation from scratch. Max pooling is a fundamental CNN operation used for downsampling and achieving translation invariance. Common in multi-view 3D networks.

## Function Signature

```python
import torch

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
    pass
```

## Mathematical Formula

```
For each pooling window:
output[b, c, h, w] = max(input[b, c, h*s:h*s+k, w*s:w*s+k])

where:
- k = kernel_size
- s = stride (default: kernel_size)

Output dimensions:
out_height = (height - kernel_size) // stride + 1
out_width = (width - kernel_size) // stride + 1
```

## Examples

```python
# Example 1: 2x2 max pooling (typical downsampling)
batch_size, channels, height, width = 1, 1, 4, 4
input_data = torch.tensor([[[[1, 2, 3, 4],
                             [5, 6, 7, 8],
                             [9, 10, 11, 12],
                             [13, 14, 15, 16]]]], dtype=torch.float32)

output = max_pool2d(input_data, kernel_size=2)
# Expected output:
# [[[[6, 8],
#    [14, 16]]]]
# Shape: [1, 1, 2, 2]

# Example 2: Multi-channel with custom stride
batch_size, channels, height, width = 2, 3, 28, 28
input_data = torch.randn(batch_size, channels, height, width)

output = max_pool2d(input_data, kernel_size=2, stride=2)
# Expected shape: [2, 3, 14, 14]

# Example 3: Overlapping windows (stride < kernel_size)
output = max_pool2d(input_data, kernel_size=3, stride=1)
# Expected shape: [2, 3, 26, 26]
```

## Test Cases

```python
def test_max_pool2d():
    # Test 1: Output shape
    input_data = torch.randn(4, 16, 32, 32)
    output = max_pool2d(input_data, kernel_size=2, stride=2)
    assert output.shape == (4, 16, 16, 16)

    # Test 2: Compare with PyTorch
    import torch.nn.functional as F
    input_data = torch.randn(2, 3, 28, 28)

    our_output = max_pool2d(input_data, kernel_size=2, stride=2)
    torch_output = F.max_pool2d(input_data, kernel_size=2, stride=2)

    assert torch.allclose(our_output, torch_output)

    # Test 3: Known values
    input_data = torch.arange(16, dtype=torch.float32).reshape(1, 1, 4, 4)
    output = max_pool2d(input_data, kernel_size=2, stride=2)
    expected = torch.tensor([[[[5., 7.], [13., 15.]]]])
    assert torch.allclose(output, expected)

    # Test 4: Maximum values
    # Output should contain only maximum values from each window
    input_data = torch.randn(2, 3, 8, 8)
    output = max_pool2d(input_data, kernel_size=2, stride=2)
    # Each output value should be >= corresponding input region
    for b in range(2):
        for c in range(3):
            for h in range(4):
                for w in range(4):
                    window = input_data[b, c, h*2:h*2+2, w*2:w*2+2]
                    assert output[b, c, h, w] == window.max()
```

## Hints

1. **Compute output dimensions**:
   ```python
   if stride is None:
       stride = kernel_size

   out_h = (height - kernel_size) // stride + 1
   out_w = (width - kernel_size) // stride + 1
   ```

2. **Initialize output tensor**:
   ```python
   output = torch.zeros(batch_size, channels, out_h, out_w)
   ```

3. **Extract windows and compute max**:
   ```python
   for h in range(out_h):
       for w in range(out_w):
           h_start = h * stride
           w_start = w * stride
           window = input[:, :, h_start:h_start+kernel_size, w_start:w_start+kernel_size]
           output[:, :, h, w] = window.max(dim=-1).values.max(dim=-1).values
   ```

4. **Alternative using unfold** (more efficient):
   ```python
   unfolded = torch.nn.functional.unfold(
       input,
       kernel_size=(kernel_size, kernel_size),
       stride=stride
   )
   # unfolded shape: [B, C*k*k, num_windows]
   # Take max over kernel dimension
   ```

5. **Vectorized approach** (advanced):
   ```python
   # Reshape to expose pooling windows
   # Then use .max() along appropriate dimensions
   ```

## Expected Time

12-18 minutes

## Key Concepts

- Sliding window operations
- Downsampling
- Max reduction operations
- Efficient tensor indexing
- Understanding pooling vs convolution

## Why This Matters for 3D AI

Max pooling is used in:
- **Multi-view CNNs**: Pool features from 2D views before 3D fusion
- **Feature pyramids**: Build multi-scale representations for 3D detection
- **Encoder networks**: Downsample before 3D decoding (e.g., in NeRF encoders)
- **Point cloud networks**: Adapted for point cloud feature aggregation
- **Texture processing**: Downsample texture maps

## Related Operations

After implementing max pooling, you might also implement:

1. **Average pooling**:
```python
def avg_pool2d(input, kernel_size, stride=None):
    # Similar but use .mean() instead of .max()
    pass
```

2. **Adaptive max pooling** (output size specified):
```python
def adaptive_max_pool2d(input, output_size):
    # Automatically compute kernel_size and stride
    # to achieve desired output_size
    pass
```

3. **Max unpooling** (upsampling):
```python
def max_unpool2d(input, indices, kernel_size):
    # Reverse of max pooling
    # Used in segmentation networks
    pass
```
