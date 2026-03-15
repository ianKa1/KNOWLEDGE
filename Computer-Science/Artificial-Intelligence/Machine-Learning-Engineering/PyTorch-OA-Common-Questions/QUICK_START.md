# Quick Start Guide

## 🎯 Complete Setup

All files are ready! Here's what you have:

```
PyTorch-OA-Common-Questions/
├── README.md                    # Full documentation
├── QUICK_START.md              # This file
├── test_solutions.py           # Automated test script
├── solution_template.py        # Template for your solutions
│
├── 01-implement-softmax/
│   ├── problem.md              # Problem description
│   └── standard_solution.py    # Reference solution
│
├── 02-cross-entropy-loss/
│   ├── problem.md
│   └── standard_solution.py
│
├── 03-cosine-similarity/
│   ├── problem.md
│   └── standard_solution.py
│
├── 04-pairwise-distance/
│   ├── problem.md
│   └── standard_solution.py
│
├── 05-attention-mechanism/
│   ├── problem.md
│   └── standard_solution.py
│
├── 06-conv2d-layer/
│   ├── problem.md
│   └── standard_solution.py
│
├── 07-vae-loss/
│   ├── problem.md
│   └── standard_solution.py
│
├── 08-diffusion-noise-schedule/
│   ├── problem.md
│   └── standard_solution.py
│
└── 09-max-pooling/
    ├── problem.md
    └── standard_solution.py
```

## ⚡ 3-Step Workflow

### Step 1: Choose a Problem
```bash
cd 01-implement-softmax
cat problem.md
```

### Step 2: Write Your Solution
```bash
# Copy template
cp ../solution_template.py solution.py

# Edit solution.py with your implementation
# Use the function signature from problem.md
```

### Step 3: Test Your Solution
```bash
cd ..
python test_solutions.py 01
```

## 🔥 Example Session

```bash
# Navigate to problems directory
cd PyTorch-OA-Common-Questions

# Start with Problem 01
cd 01-implement-softmax
cat problem.md

# Create your solution
cp ../solution_template.py solution.py
# Edit solution.py...

# Test it
cd ..
python test_solutions.py 01

# See results:
# ✅ All 3 tests passed!  (Success!)
# or
# ❌ 1/3 tests failed    (Keep trying!)
```

## 📝 Your Solution Format

```python
# 01-implement-softmax/solution.py

import torch

def softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    # Your implementation here
    pass
```

The function name **must match** the one in `problem.md`!

## ✅ Test Commands

```bash
# Test one problem
python test_solutions.py 01

# Test multiple problems
python test_solutions.py 01 03 05

# Test all problems you've completed
python test_solutions.py

# Show detailed output
python test_solutions.py 01 --verbose
```

## 🎓 Recommended Order

**Start here (Easy):**
1. Problem 01 - Softmax
2. Problem 09 - Max Pooling
3. Problem 03 - Cosine Similarity

**Then (Medium):**
4. Problem 02 - Cross Entropy Loss
5. Problem 04 - Pairwise Distance
6. Problem 06 - Conv2D Layer
7. Problem 08 - Diffusion Noise Schedule

**Finally (Hard):**
8. Problem 05 - Attention Mechanism
9. Problem 07 - VAE Loss

## 🐛 Common Issues

### "No module named 'torch'"
```bash
pip install torch
```

### "solution.py not found"
You need to create `solution.py` in the problem directory:
```bash
cd 01-implement-softmax
cp ../solution_template.py solution.py
# Then edit solution.py
```

### "Function 'xxx' not found"
Make sure your function name exactly matches the one in `problem.md`.

### Tests fail with shape mismatches
Check the expected input/output shapes in `problem.md`.

## 💡 Pro Tips

1. **Don't peek at standard_solution.py** until after you've tried!
2. **Use hints progressively** - only look when stuck
3. **Time yourself** to simulate real conditions
4. **Run tests often** as you code
5. **Read error messages carefully** - they tell you exactly what's wrong

## 🎯 Before Your Real OA

Practice with a mock assessment:
```bash
# Pick 1 easy + 1 medium problem
# Set 42-minute timer
# Solve both problems
# Run tests

python test_solutions.py 01 04
```

## 📊 Progress Tracking

Keep track of your progress:

```
Problems Completed: __ / 9

✅ = Completed and passing all tests
⏳ = In progress
❌ = Attempted but failing tests
☐ = Not started

[☐] 01 - Softmax
[☐] 02 - Cross Entropy Loss
[☐] 03 - Cosine Similarity
[☐] 04 - Pairwise Distance
[☐] 05 - Attention Mechanism
[☐] 06 - Conv2D Layer
[☐] 07 - VAE Loss
[☐] 08 - Diffusion Noise Schedule
[☐] 09 - Max Pooling
```

---

**Ready to start? Pick Problem 01 and let's go! 加油！** 💪
