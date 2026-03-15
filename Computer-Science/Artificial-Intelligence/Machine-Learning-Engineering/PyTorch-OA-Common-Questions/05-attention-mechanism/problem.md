# Problem 5: Implement Attention Mechanism

## Difficulty: Medium-Hard

## Problem Description

Implement the scaled dot-product attention mechanism used in Transformers. This is a core component of modern deep learning architectures and very relevant for 3D AI (many NeRF variants use attention).

## Function Signature

```python
import torch

def scaled_dot_product_attention(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    mask: torch.Tensor = None
) -> torch.Tensor:
    """
    Compute scaled dot-product attention.

    Args:
        Q: Query tensor of shape [batch_size, num_queries, d_k]
        K: Key tensor of shape [batch_size, num_keys, d_k]
        V: Value tensor of shape [batch_size, num_keys, d_v]
        mask: Optional mask of shape [batch_size, num_queries, num_keys]
              (True/1 where attention should be masked out)

    Returns:
        Output tensor of shape [batch_size, num_queries, d_v]
    """
    pass
```

## Mathematical Formula

```
Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

where:
- Q @ K^T: [batch, num_q, num_k] attention scores
- sqrt(d_k): scaling factor (d_k is the key dimension)
- softmax applied along the last dimension
- Result @ V: [batch, num_q, d_v] output
```

## Examples

```python
# Example 1: Simple attention
batch_size, num_q, num_k, d_k, d_v = 1, 3, 4, 8, 16
Q = torch.randn(batch_size, num_q, d_k)
K = torch.randn(batch_size, num_k, d_k)
V = torch.randn(batch_size, num_k, d_v)

output = scaled_dot_product_attention(Q, K, V)
# Expected shape: [1, 3, 16]

# Example 2: Self-attention (Q = K = V)
x = torch.randn(2, 10, 64)  # [batch, seq_len, dim]
output = scaled_dot_product_attention(x, x, x)
# Expected shape: [2, 10, 64]

# Example 3: With masking (e.g., causal mask for language models)
batch_size, seq_len, d_model = 2, 5, 64
Q = K = V = torch.randn(batch_size, seq_len, d_model)

# Causal mask: prevent attending to future positions
mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
mask = mask.unsqueeze(0).expand(batch_size, -1, -1)

output = scaled_dot_product_attention(Q, K, V, mask)
# Expected shape: [2, 5, 64]
```

## Test Cases

```python
def test_attention():
    # Test 1: Shape preservation
    B, N_q, N_k, D_k, D_v = 4, 10, 20, 32, 64
    Q = torch.randn(B, N_q, D_k)
    K = torch.randn(B, N_k, D_k)
    V = torch.randn(B, N_k, D_v)

    output = scaled_dot_product_attention(Q, K, V)
    assert output.shape == (B, N_q, D_v)

    # Test 2: Attention weights sum to 1
    # (You might want to return attention weights for verification)

    # Test 3: Masked attention
    mask = torch.zeros(B, N_q, N_k).bool()
    mask[:, :, -5:] = True  # Mask last 5 keys
    output_masked = scaled_dot_product_attention(Q, K, V, mask)
    assert output_masked.shape == (B, N_q, D_v)
```

## Hints

1. **Compute attention scores**:
   ```python
   scores = Q @ K.transpose(-2, -1)  # [B, num_q, num_k]
   scores = scores / torch.sqrt(torch.tensor(d_k, dtype=torch.float32))
   ```

2. **Apply mask** (before softmax):
   ```python
   if mask is not None:
       scores = scores.masked_fill(mask, float('-inf'))
   ```

3. **Softmax** along the last dimension:
   ```python
   attn_weights = torch.softmax(scores, dim=-1)
   ```

4. **Weighted sum of values**:
   ```python
   output = attn_weights @ V  # [B, num_q, d_v]
   ```

5. **Handle dimensions**: Use `.transpose(-2, -1)` instead of `.T` for batched tensors

## Expected Time

15-25 minutes

## Key Concepts

- Matrix multiplication with batches
- Scaling for numerical stability
- Softmax along specific dimension
- Masked attention (setting -inf before softmax)
- Understanding attention mechanism conceptually

## Why This Matters for 3D AI

Attention is used in:
- **Transformer-based 3D generation** (e.g., Shap-E)
- **Point cloud processing** (Point Transformer, Point-BERT)
- **NeRF variants** (using attention for view aggregation)
- **Text-to-3D models** (CLIP attention for text-image alignment)

## Bonus Challenge

Implement multi-head attention:
```python
def multi_head_attention(Q, K, V, num_heads=8):
    # Split into multiple heads
    # Apply scaled_dot_product_attention to each head
    # Concatenate results
    pass
```
