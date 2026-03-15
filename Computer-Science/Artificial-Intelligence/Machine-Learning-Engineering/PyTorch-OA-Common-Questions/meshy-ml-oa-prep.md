# PyTorch OA Common Questions - ML Engineering Interview Prep

## Overview

This guide covers typical PyTorch coding patterns for ML engineering online assessments (OA), based on 3D generative AI startup interviews (e.g., Meshy). These 42-minute assessments test ML engineering coding ability rather than complex algorithms.

## Common Question Categories (By Probability)

<!-- numpy, torch(broadcast)
[Tensor Manipulation], [Neural Network Layer], [Loss Function], [Graident],  -->

### 1️⃣ PyTorch Tensor Manipulation (Highest Probability)

Most common in ML OAs.

**Examples:**
```python
# Implement masked mean
def masked_mean(x, mask):
    ...

# Compute pairwise cosine similarity
def cosine_sim(A, B):
    ...

# Batch matrix multiplication
```

**Key Concepts:**
- Tensor shape manipulation
- Broadcasting
- `torch.matmul`
- `torch.norm`
- `torch.softmax`

**Typical Problem:**
```python
# x: [B, N, D]
# Compute attention scores
```

### 2️⃣ Neural Network Layer Implementation

**Examples:**
```python
# Implement linear layer
class Linear(nn.Module):
    def __init__(self, in_dim, out_dim):
        ...
    def forward(self, x):
        ...

# Implement MLP forward pass
def forward(self, x):
    ...
```

**Key Concepts:**
- `nn.Module`
- Parameters
- Forward pass
- ReLU / Softmax activation

### 3️⃣ Loss Function Implementation

Very common in ML OAs.

**Examples:**
```python
# Cross entropy
def cross_entropy(logits, targets):
    ...

# Contrastive loss
def contrastive_loss(z1, z2):
    ...
```

### 4️⃣ Autograd / Gradient

**Examples:**
```python
# Why use torch.no_grad()?

# Training loop
for x, y in loader:
    optimizer.zero_grad()
    loss = ...
    loss.backward()
    optimizer.step()
```

### 5️⃣ Simple ML Algorithm Implementation

**Examples:**
```python
# Logistic regression
def train_step(X, y):
    ...

# k-Nearest Neighbors
def knn(query, dataset):
    ...
```

### 6️⃣ 3D / Geometry (Domain-Specific)

For 3D AI companies like Meshy.

**Examples:**
```python
# Point cloud - compute pairwise distance
# points: [N, 3]

# Normalize vertices to unit sphere
def normalize_mesh(vertices):
    ...
```

### 7️⃣ NumPy → PyTorch Conversion

**Example:**
```python
# Convert numpy implementation to PyTorch
```

## Assessment Format (42 minutes)

**Typical Structure:**
- 2 questions total
- 1 easy + 1 medium
- Example breakdown:

| Question | Difficulty |
|----------|-----------|
| Tensor manipulation | Easy |
| Loss function / Layer | Medium |

**What's NOT tested:**
- ❌ Graph algorithms
- ❌ Dynamic programming
- ❌ LeetCode hard problems

## Top 5 Focus Areas for 3D AI Companies

Based on Meshy's business (text-to-3D, diffusion, NeRF):

1. **Torch tensor shape manipulation**
2. **Pairwise distance / cosine similarity**
3. **Cross entropy / MSE**
4. **Simple neural network forward**
5. **Attention computation**

**Example:**
```python
def attention(Q, K, V):
    # Compute scaled dot-product attention
    ...
```

## Recommended Practice Problems

High probability questions to prepare:

1. ✅ Implement softmax
2. ✅ Implement cross entropy
3. ✅ Implement cosine similarity
4. ✅ Implement pairwise distance
5. ✅ Implement attention mechanism

## Domain-Specific Patterns (3D AI)

For candidates with CG/physics/generative AI background:

**Common patterns:**
- Point cloud operations
- 3D tensor manipulation
- Batch matrix multiplication

**Typical problem:**
```python
# points: [B, N, 3]
# Compute pairwise distance matrix
```

## Related Topics

- Deep Learning Frameworks
- Neural Networks
- 3D Geometry processing

## References

- PyTorch documentation
- Common ML engineering interview patterns
- 3D generative AI technical requirements
