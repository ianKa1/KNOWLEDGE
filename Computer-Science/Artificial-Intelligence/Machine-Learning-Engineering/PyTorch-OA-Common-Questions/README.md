# PyTorch OA Common Questions - Practice Problems

A comprehensive collection of 9 practice problems for ML engineering online assessments, specifically tailored for 3D AI companies like Meshy.

## 📁 Structure

Each problem directory contains:
- `problem.md` - Problem description, examples, hints, and test cases
- `standard_solution.py` - Reference solution with comprehensive tests
- `solution.py` - **YOUR solution goes here** (you create this file)

## 🎯 Problems

| # | Problem | Difficulty | Time | Topics |
|---|---------|------------|------|--------|
| 01 | Implement Softmax | Easy | 5-10 min | Tensor ops, numerical stability |
| 02 | Cross Entropy Loss | Medium | 10-15 min | Loss functions, log-sum-exp |
| 03 | Cosine Similarity | Easy-Medium | 8-12 min | Similarity metrics, broadcasting |
| 04 | Pairwise Distance | Medium | 12-18 min | 3D geometry, efficient computation |
| 05 | Attention Mechanism | Medium-Hard | 15-25 min | Transformers, masking |
| 06 | 2D Convolution | Medium | 18-25 min | CNN, unfold operations |
| 07 | VAE Loss (ELBO) | Medium-Hard | 20-28 min | Generative models, KL divergence |
| 08 | Diffusion Noise Schedule | Medium | 15-22 min | Diffusion models, noise scheduling |
| 09 | 2D Max Pooling | Easy-Medium | 12-18 min | CNN, downsampling |

## 🚀 How to Use

### 1. Read the Problem
```bash
cd 01-implement-softmax
cat problem.md
```

### 2. Write Your Solution
Create `solution.py` in the problem directory:

```python
# 01-implement-softmax/solution.py
import torch

def softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    # Your implementation here
    pass
```

### 3. Test Your Solution

**Test a specific problem:**
```bash
python test_solutions.py 01
```

**Test multiple problems:**
```bash
python test_solutions.py 01 03 05
```

**Test all problems:**
```bash
python test_solutions.py
```

**Verbose output:**
```bash
python test_solutions.py --verbose
python test_solutions.py 01 --verbose
```

### 4. Check the Standard Solution
After attempting the problem, review the reference implementation:
```bash
cat 01-implement-softmax/standard_solution.py
```

## 📊 Test Output Examples

### ✅ Success
```
Testing: 01-implement-softmax
  ✅ All 3 tests passed!

Testing: 02-cross-entropy-loss
  ✅ All 2 tests passed!
```

### ❌ Failure
```
Testing: 03-cosine-similarity
  ❌ 1/3 tests failed
  Errors:
    - Random vectors: Shape mismatch: torch.Size([20, 30]) vs torch.Size([30, 20])
```

### ⊘ No Solution
```
Testing: 04-pairwise-distance
  ⊘ No solution file found (skipped)
```

## 💡 Tips

1. **Start with easier problems** (01, 03, 09) to build confidence
2. **Time yourself** to simulate real interview conditions
3. **Don't look at standard_solution.py** until you've attempted the problem
4. **Read hints incrementally** - try solving first, then use hints if stuck
5. **Run tests frequently** as you develop your solution
6. **Compare implementations** - learn from the alternative approaches in standard solutions

## 🎓 Learning Path

### Beginner Path
1. Problem 01 (Softmax) - Learn basic tensor operations
2. Problem 09 (Max Pooling) - Understand sliding windows
3. Problem 03 (Cosine Similarity) - Practice broadcasting

### Intermediate Path
4. Problem 02 (Cross Entropy) - Master loss functions
5. Problem 04 (Pairwise Distance) - Efficient pairwise operations
6. Problem 06 (Conv2D) - Deep dive into convolutions

### Advanced Path
7. Problem 05 (Attention) - Implement transformer components
8. Problem 08 (Diffusion) - Understand diffusion models
9. Problem 07 (VAE Loss) - Generative model theory

## 🔧 Troubleshooting

### Import Errors
If you see `Import "torch" could not be resolved`:
```bash
pip install torch
```

### Module Not Found
Make sure you're running the test script from the `PyTorch-OA-Common-Questions` directory:
```bash
cd /path/to/PyTorch-OA-Common-Questions
python test_solutions.py
```

### Test Failures
- Check the error message for specific issues (shape mismatches, value differences)
- Use `--verbose` flag to see detailed test output
- Review the hints in `problem.md`
- Compare your approach with `standard_solution.py`

## 📚 Additional Resources

Each problem includes:
- **Mathematical formulas** - Understand the theory
- **Examples** - See expected inputs and outputs
- **Test cases** - Verify correctness
- **Hints** - Step-by-step implementation guidance
- **Key concepts** - What you're learning
- **Why it matters for 3D AI** - Real-world applications
- **Bonus challenges** - Extend your knowledge

## 🎯 Preparing for OA

**Recommended Practice Schedule:**

**Week 1 - Fundamentals (30-45 min/day)**
- Day 1: Problem 01 (Softmax)
- Day 2: Problem 02 (Cross Entropy)
- Day 3: Problem 03 (Cosine Similarity)
- Day 4: Review and retry problems 01-03
- Day 5: Problem 09 (Max Pooling)

**Week 2 - Intermediate (45-60 min/day)**
- Day 1: Problem 04 (Pairwise Distance)
- Day 2: Problem 06 (Conv2D)
- Day 3: Problem 08 (Diffusion)
- Day 4: Review and retry problems 04, 06, 08
- Day 5: Timed practice (2 problems in 42 minutes)

**Week 3 - Advanced (60+ min/day)**
- Day 1: Problem 05 (Attention)
- Day 2: Problem 07 (VAE Loss)
- Day 3: Review and retry problems 05, 07
- Day 4: Mock OA (2 random problems in 42 minutes)
- Day 5: Mock OA (2 different problems in 42 minutes)

**Before the OA:**
- Do a final mock: Pick 1 easy + 1 medium problem
- Set a 42-minute timer
- Use only problem.md (no hints initially)
- Test your solution

## 🏆 Completion Goals

- [ ] Solve all 9 problems
- [ ] Pass all tests without hints
- [ ] Complete each problem within time limit
- [ ] Understand alternative implementations
- [ ] Complete bonus challenges
- [ ] Achieve 42-minute mock OA (1 easy + 1 medium)

## 📧 Notes

- **Standard solutions** are well-tested and include edge case handling
- **Multiple implementations** are provided to show different approaches
- **Extensive tests** (8-11 per problem) ensure correctness
- **Real interview relevance** - all problems based on actual ML engineering OA patterns

---

**Good luck with your preparation! 加油！** 🚀
