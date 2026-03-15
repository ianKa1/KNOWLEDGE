"""
Solution: Implement Scaled Dot-Product Attention
Difficulty: Medium-Hard
Expected Time: 15-25 minutes
"""

import torch
import torch.nn.functional as F


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
    # Get d_k for scaling
    d_k = Q.shape[-1]

    # Compute attention scores: Q @ K^T / sqrt(d_k)
    # Q: [B, num_q, d_k], K: [B, num_k, d_k]
    # scores: [B, num_q, num_k]
    scores = Q @ K.transpose(-2, -1) / torch.sqrt(torch.tensor(d_k, dtype=torch.float32))

    # Apply mask (set masked positions to -inf before softmax)
    if mask is not None:
        scores = scores.masked_fill(mask, float('-inf'))

    # Apply softmax to get attention weights
    attn_weights = torch.softmax(scores, dim=-1)

    # Handle NaN from softmax over all -inf (all positions masked)
    # This can happen if an entire query has all keys masked
    attn_weights = torch.nan_to_num(attn_weights, nan=0.0)

    # Compute weighted sum of values
    # attn_weights: [B, num_q, num_k], V: [B, num_k, d_v]
    # output: [B, num_q, d_v]
    output = attn_weights @ V

    return output


def scaled_dot_product_attention_with_weights(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    mask: torch.Tensor = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """Version that also returns attention weights for visualization"""
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / torch.sqrt(torch.tensor(d_k, dtype=torch.float32))

    if mask is not None:
        scores = scores.masked_fill(mask, float('-inf'))

    attn_weights = torch.softmax(scores, dim=-1)
    attn_weights = torch.nan_to_num(attn_weights, nan=0.0)

    output = attn_weights @ V

    return output, attn_weights


# Bonus: Multi-head attention implementation
def multi_head_attention(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    num_heads: int = 8,
    mask: torch.Tensor = None
) -> torch.Tensor:
    """
    Multi-head attention implementation.

    Args:
        Q, K, V: [batch_size, seq_len, d_model]
        num_heads: Number of attention heads
        mask: Optional mask

    Returns:
        Output tensor of shape [batch_size, seq_len, d_model]
    """
    batch_size, seq_len, d_model = Q.shape

    # Check that d_model is divisible by num_heads
    assert d_model % num_heads == 0, f"d_model ({d_model}) must be divisible by num_heads ({num_heads})"

    d_k = d_model // num_heads

    # Split into multiple heads
    # [B, seq_len, d_model] -> [B, num_heads, seq_len, d_k]
    Q_heads = Q.reshape(batch_size, seq_len, num_heads, d_k).transpose(1, 2)
    K_heads = K.reshape(batch_size, seq_len, num_heads, d_k).transpose(1, 2)
    V_heads = V.reshape(batch_size, seq_len, num_heads, d_k).transpose(1, 2)

    # Apply attention to each head
    # Reshape for batch processing: [B * num_heads, seq_len, d_k]
    Q_heads = Q_heads.reshape(batch_size * num_heads, seq_len, d_k)
    K_heads = K_heads.reshape(batch_size * num_heads, seq_len, d_k)
    V_heads = V_heads.reshape(batch_size * num_heads, seq_len, d_k)

    # Expand mask if provided
    if mask is not None:
        # [B, seq_len, seq_len] -> [B * num_heads, seq_len, seq_len]
        mask = mask.unsqueeze(1).repeat(1, num_heads, 1, 1).reshape(batch_size * num_heads, seq_len, seq_len)

    # Apply attention
    attn_output = scaled_dot_product_attention(Q_heads, K_heads, V_heads, mask)

    # Concatenate heads
    # [B * num_heads, seq_len, d_k] -> [B, num_heads, seq_len, d_k] -> [B, seq_len, d_model]
    attn_output = attn_output.reshape(batch_size, num_heads, seq_len, d_k)
    attn_output = attn_output.transpose(1, 2).reshape(batch_size, seq_len, d_model)

    return attn_output


# Test cases
def test_attention():
    print("Running tests for scaled_dot_product_attention...\n")

    # Test 1: Shape preservation
    print("Test 1: Shape preservation")
    B, N_q, N_k, D_k, D_v = 4, 10, 20, 32, 64
    Q = torch.randn(B, N_q, D_k)
    K = torch.randn(B, N_k, D_k)
    V = torch.randn(B, N_k, D_v)

    output = scaled_dot_product_attention(Q, K, V)
    assert output.shape == (B, N_q, D_v)
    print(f"✓ Input shapes: Q{Q.shape}, K{K.shape}, V{V.shape}")
    print(f"✓ Output shape: {output.shape}")

    # Test 2: Attention weights sum to 1
    print("\nTest 2: Attention weights sum to 1")
    output, attn_weights = scaled_dot_product_attention_with_weights(Q, K, V)
    weights_sum = attn_weights.sum(dim=-1)
    assert torch.allclose(weights_sum, torch.ones_like(weights_sum), atol=1e-5)
    print(f"✓ Attention weights shape: {attn_weights.shape}")
    print(f"✓ Weights sum per query: {weights_sum[0, :5]}")

    # Test 3: Self-attention (Q = K = V)
    print("\nTest 3: Self-attention")
    x = torch.randn(2, 10, 64)
    output = scaled_dot_product_attention(x, x, x)
    assert output.shape == x.shape
    print(f"✓ Self-attention output shape: {output.shape}")

    # Test 4: Masked attention
    print("\nTest 4: Masked attention (causal mask)")
    batch_size, seq_len, d_model = 2, 5, 64
    Q = K = V = torch.randn(batch_size, seq_len, d_model)

    # Create causal mask (prevent attending to future positions)
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
    mask = mask.unsqueeze(0).expand(batch_size, -1, -1)

    output, attn_weights = scaled_dot_product_attention_with_weights(Q, K, V, mask)

    # Check that attention weights are 0 for masked positions
    masked_weights = attn_weights[0, :, :]
    print(f"✓ Masked output shape: {output.shape}")
    print(f"✓ Attention weights (first batch, causal mask):")
    print(masked_weights)
    # Verify causal property: position i only attends to positions <= i
    for i in range(seq_len):
        future_weights = masked_weights[i, i+1:]
        assert torch.allclose(future_weights, torch.zeros_like(future_weights), atol=1e-5)
    print(f"✓ Causal mask verified: no attention to future positions")

    # Test 5: Masking specific positions
    print("\nTest 5: Masking last 5 keys")
    B, N_q, N_k = 4, 10, 20
    Q = torch.randn(B, N_q, 32)
    K = torch.randn(B, N_k, 32)
    V = torch.randn(B, N_k, 64)

    mask = torch.zeros(B, N_q, N_k).bool()
    mask[:, :, -5:] = True  # Mask last 5 keys

    output, attn_weights = scaled_dot_product_attention_with_weights(Q, K, V, mask)

    # Check that masked positions have zero attention
    assert torch.allclose(attn_weights[:, :, -5:], torch.zeros(B, N_q, 5), atol=1e-5)
    print(f"✓ Attention to masked positions: {attn_weights[0, 0, -5:].sum().item():.10f}")

    # Test 6: Compare with PyTorch implementation (PyTorch 2.0+)
    print("\nTest 6: Compare with torch.nn.functional.scaled_dot_product_attention")
    Q = torch.randn(2, 8, 10, 64)  # [B, num_heads, seq_len, d_k]
    K = torch.randn(2, 8, 10, 64)
    V = torch.randn(2, 8, 10, 64)

    # Our implementation (needs to be reshaped)
    Q_flat = Q.reshape(16, 10, 64)
    K_flat = K.reshape(16, 10, 64)
    V_flat = V.reshape(16, 10, 64)
    our_output = scaled_dot_product_attention(Q_flat, K_flat, V_flat)
    our_output = our_output.reshape(2, 8, 10, 64)

    # PyTorch implementation (if available)
    try:
        torch_output = F.scaled_dot_product_attention(Q, K, V)
        assert torch.allclose(our_output, torch_output, atol=1e-5)
        print(f"✓ Matches PyTorch implementation")
    except AttributeError:
        print(f"⚠ PyTorch 2.0+ required for comparison, skipping")

    # Test 7: Different d_k and d_v
    print("\nTest 7: Different dimensions for keys and values")
    Q = torch.randn(2, 5, 32)   # d_k = 32
    K = torch.randn(2, 8, 32)   # d_k = 32
    V = torch.randn(2, 8, 128)  # d_v = 128

    output = scaled_dot_product_attention(Q, K, V)
    assert output.shape == (2, 5, 128)
    print(f"✓ Q shape: {Q.shape}, V shape: {V.shape}")
    print(f"✓ Output shape: {output.shape}")

    print("\n✅ All tests passed!")

    # Bonus: Test multi-head attention
    print("\n" + "="*50)
    print("BONUS: Testing multi-head attention")
    print("="*50)

    batch_size, seq_len, d_model = 2, 10, 512
    num_heads = 8

    Q = K = V = torch.randn(batch_size, seq_len, d_model)
    output = multi_head_attention(Q, K, V, num_heads=num_heads)

    assert output.shape == (batch_size, seq_len, d_model)
    print(f"✓ Multi-head attention output shape: {output.shape}")
    print(f"✓ Number of heads: {num_heads}")
    print(f"✓ d_k per head: {d_model // num_heads}")

    print("\n✅ Multi-head attention test passed!")


if __name__ == "__main__":
    test_attention()
