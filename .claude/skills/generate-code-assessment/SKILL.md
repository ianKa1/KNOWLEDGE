---
name: generate-code-assessment
description: Generate comprehensive practice problem sets for coding assessments (online assessments, technical interviews, etc.). Creates structured problems with detailed descriptions, standard solutions, automated testing, and documentation. Use this skill when users want to create practice problems, prepare for technical interviews, build coding assessment repositories, or convert study materials into practice exercises. Triggers on phrases like "create practice problems", "generate OA problems", "make coding exercises", "prepare interview questions", or when users provide reference materials and want to turn them into structured practice sets.
---

# Generate Code Assessment

This skill generates comprehensive practice problem sets for coding assessments, particularly for ML/AI engineering interviews and online assessments.

## What This Skill Does

Given a reference document describing an assessment topic (e.g., PyTorch fundamentals, system design, algorithms), this skill:

1. **Analyzes the reference** to identify key topics, concepts, and difficulty levels
2. **Generates practice problems** (5-10 problems) with:
   - Detailed problem descriptions (`problem.md`)
   - Complete reference solutions (`standard_solution.py`)
   - Proper difficulty progression
3. **Creates testing infrastructure** (`test_solutions.py`) to verify user solutions
4. **Builds documentation** (README, Quick Start guide, solution template)
5. **Structures everything** in a ready-to-use practice repository

## When to Use This Skill

Use this skill when the user:
- Provides a study guide or reference document and wants practice problems
- Asks to "create practice problems" or "generate exercises"
- Mentions preparing for technical interviews or online assessments
- Wants to convert learning materials into hands-on practice
- Requests a coding problem repository for a specific topic

## Input Requirements

The user should provide:
1. **Reference document** - A markdown file describing:
   - The assessment topic/domain (e.g., "PyTorch for ML engineering OA")
   - Key concepts and categories (e.g., "tensor operations", "loss functions", "attention")
   - Difficulty levels or progression
   - Expected problem types
   - Time estimates (optional)
   - Why these topics matter (context/motivation)

2. **Target directory** - Where to create the practice problem set

3. **Optional preferences**:
   - Number of problems (default: based on reference content)
   - Programming language (default: Python)
   - Difficulty distribution (default: balanced)
   - Include bonus challenges (default: yes)

## Output Structure

Creates a complete practice problem repository:

```
<topic-name>/
├── README.md                    # Full documentation
├── QUICK_START.md              # Quick reference
├── test_solutions.py           # Automated test harness
├── solution_template.py        # Template for users
│
├── 01-<problem-name>/
│   ├── problem.md              # Problem description
│   └── standard_solution.py    # Reference solution with tests
│
├── 02-<problem-name>/
│   ├── problem.md
│   └── standard_solution.py
│
└── ...
```

## Workflow

### Step 1: Analyze the Reference Document

Read the provided reference document and extract:
- **Main topic/domain** (e.g., "PyTorch OA Common Questions")
- **Key concept categories** (e.g., "Basic Operations", "Loss Functions", "CNN", "Generative Models")
- **Difficulty indicators** (if mentioned: "easy", "medium", "hard")
- **Problem suggestions** (explicit or implied)
- **Context/motivation** ("Why this matters for 3D AI")
- **Time estimates** (if provided)

### Step 2: Plan the Problem Set

Based on the reference analysis, plan 5-10 problems:

**Problem Selection Criteria:**
- Cover all major topics from the reference
- Progress from easier to harder
- Include foundational concepts before advanced ones
- Mix different problem types (implementation, analysis, optimization)
- Ensure practical relevance (connect to real-world applications)

**Difficulty Distribution:**
- 30-40% Easy (build confidence, test fundamentals)
- 40-50% Medium (core competency)
- 20-30% Hard (challenge, depth)

**For each problem, plan:**
1. Problem name (descriptive, kebab-case)
2. Difficulty level
3. Core concept being tested
4. Expected time to solve
5. Key learning objectives
6. Related topics for cross-referencing

### Step 3: Generate Problem Descriptions

For each problem, create `problem.md` with this structure:

```markdown
# Problem N: [Title]

## Difficulty: [Easy|Medium|Hard]

## Problem Description

[1-2 paragraphs explaining what to implement and why it's important.
Connect to real-world applications if relevant.]

## Function Signature

\```python
import torch  # or relevant imports

def function_name(
    arg1: Type,
    arg2: Type,
    arg3: Type = None
) -> ReturnType:
    """
    [Brief description]

    Args:
        arg1: Description
        arg2: Description
        arg3: Description (optional)

    Returns:
        Description of return value
    """
    pass
\```

## Mathematical Formula

[If applicable, include the mathematical foundation]

\```
formula = explanation
\```

## Examples

\```python
# Example 1: [Descriptive name]
input_data = ...
output = function_name(input_data)
# Expected: [description of expected output]

# Example 2: [Another scenario]
...

# Example 3: [Edge case or advanced usage]
...
\```

## Test Cases

\```python
def test_function_name():
    # Test 1: [What this tests]
    ...
    assert ...

    # Test 2: [Another aspect]
    ...
    assert ...

    # Test 3: [Edge case]
    ...
    assert ...
\```

## Hints

1. **[First step]**:
   \```python
   # Code snippet or explanation
   \```

2. **[Second step]**:
   \```python
   # More guidance
   \```

[Continue with 3-5 hints that progressively reveal the solution approach]

## Expected Time

X-Y minutes

## Key Concepts

- Concept 1
- Concept 2
- Concept 3
- Understanding X
- Y technique

## Why This Matters for [Domain]

[2-3 paragraphs explaining real-world applications, especially in the target domain.
Use specific examples and technologies.]

Examples used in:
- **Application 1**: How it's used
- **Application 2**: Why it's important
- **Application 3**: Specific technology/framework

## Bonus Challenge

[Optional advanced extension or related problem]

\```python
def bonus_function(...):
    # Extended functionality
    pass
\```
```

**Writing Guidelines for Problem Descriptions:**

- **Be specific and concrete**: Use actual code examples, not abstract descriptions
- **Include mathematical foundations**: When relevant, show the formulas
- **Progressive hints**: Start with high-level guidance, get more specific
- **Real-world context**: Always explain why this matters
- **Appropriate difficulty**: Match expected time and complexity
- **Complete examples**: Show full input → output transformations

### Step 4: Generate Standard Solutions

For each problem, create `standard_solution.py` with:

```python
"""
Solution: [Problem Title]
Difficulty: [Level]
Expected Time: [Range]
"""

import torch
# Other necessary imports


def main_function(args...):
    """
    [Copy docstring from problem.md]
    """
    # Step 1: [Comment explaining this step]
    ...

    # Step 2: [Next step]
    ...

    return result


# Alternative implementation (if valuable)
def main_function_v2(args...):
    """Alternative approach using [technique]"""
    ...


# Helper functions if needed
def helper_function():
    """Helper for [purpose]"""
    ...


# Bonus implementations
def bonus_function():
    """Bonus challenge implementation"""
    ...


# Test cases
def test_main_function():
    print("Running tests for [function_name]...\\n")

    # Test 1: [Description]
    print("Test 1: [What we're testing]")
    input_data = ...
    output = main_function(input_data)
    assert ...
    print(f"✓ [Success message]")

    # Test 2-10: [More comprehensive tests]
    # Include:
    # - Shape verification
    # - Value correctness
    # - Edge cases
    # - Comparison with standard library (if applicable)
    # - Numerical stability
    # - Performance on large inputs

    print("\\n✅ All tests passed!")


if __name__ == "__main__":
    test_main_function()
```

**Standards for Solutions:**

- **Complete and correct**: Must work flawlessly
- **Well-commented**: Explain the "why", not just the "what"
- **Multiple approaches**: Show alternative implementations when valuable
- **Comprehensive tests**: 8-12 test cases covering edge cases
- **Educational**: Code should teach best practices
- **Comparison with stdlib**: Compare against PyTorch/NumPy built-ins when applicable

### Step 5: Create Test Harness

Generate `test_solutions.py` that:

1. **Discovers problems**: Finds all `XX-problem-name/` directories
2. **Loads modules**: Dynamically imports user's `solution.py` and `standard_solution.py`
3. **Runs test cases**: Executes predefined test cases
4. **Compares outputs**: Checks if user output matches standard output
5. **Reports results**: Shows pass/fail for each test and overall summary

**Test harness configuration:**

```python
PROBLEMS = {
    "01-problem-name": {
        "function": "function_name",
        "test_cases": [
            {
                "name": "Descriptive test name",
                "args": (arg1, arg2),
                "kwargs": {"kwarg1": value},
            },
            # More test cases...
        ],
    },
    # More problems...
}
```

The test harness should:
- Support testing individual problems: `python test_solutions.py 01`
- Support testing multiple: `python test_solutions.py 01 03 05`
- Support testing all: `python test_solutions.py`
- Provide verbose mode: `python test_solutions.py --verbose`
- Handle tuple outputs (e.g., VAE loss returning 3 values)
- Use `torch.allclose()` for tensor comparison
- Show helpful error messages (shape mismatches, value differences)

### Step 6: Generate Documentation

Create three documentation files:

#### **README.md** (comprehensive guide)

Include:
- **Problem table**: Number, name, difficulty, time, topics
- **Structure overview**: What each file/directory contains
- **How to use**: Step-by-step workflow
- **Test output examples**: What success/failure looks like
- **Tips**: Study strategies, timing practice
- **Learning paths**: Beginner → Intermediate → Advanced
- **Troubleshooting**: Common issues and solutions
- **Practice schedule**: Week-by-week plan
- **Completion goals**: Checklist for tracking progress

#### **QUICK_START.md** (quick reference)

Include:
- **3-step workflow**: Choose, write, test
- **Example session**: Concrete walkthrough
- **Test commands**: Common usage patterns
- **Recommended order**: Which problems to start with
- **Common issues**: Quick fixes
- **Pro tips**: Best practices
- **Progress tracker**: Checklist

#### **solution_template.py** (starter code)

Provide a template users can copy to start each problem:

```python
"""
Solution Template for [Assessment Name]

Usage:
    cp solution_template.py 01-problem-name/solution.py
    # Edit solution.py
    python test_solutions.py 01
"""

import torch
# Add other imports as needed


def your_function_name(arg1, arg2):
    """
    [Copy from problem.md]
    """
    # Your implementation here
    pass


if __name__ == "__main__":
    # Optional: your own quick tests
    print("Testing...")
```

### Step 7: Final Structure and Validation

Before completing:

1. **Verify directory names**: Use consistent numbering (01, 02, ..., 09, 10)
2. **Check cross-references**: Ensure problem.md mentions related topics correctly
3. **Validate test harness**: Make sure all problems are configured
4. **Ensure completeness**: Every problem has both files
5. **Test one problem**: Run the test harness on one standard solution to verify it works

**Directory naming conventions:**
- Format: `{number:02d}-{problem-name}`
- Example: `01-implement-softmax`, `05-attention-mechanism`
- Use kebab-case for problem names
- Start from 01 (not 00)

## Problem Quality Guidelines

### Mathematical Accuracy
- Formulas must be correct and properly formatted
- Include dimension annotations for matrix operations
- Explain notation used

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints consistently
- Include comprehensive docstrings
- Comment complex logic
- Show multiple approaches when valuable

### Test Coverage
- Test basic functionality
- Test edge cases (empty inputs, extreme values)
- Test shape preservation
- Compare with standard library implementations
- Test numerical stability
- Verify correctness properties (e.g., attention weights sum to 1)

### Educational Value
- Clear progression from simple to complex
- Connect to real-world applications
- Explain the "why" behind techniques
- Include relevant background (when it matters)
- Cross-reference related problems

## Example Problem Topics

### For ML/PyTorch Assessments:

**Fundamentals:**
- Tensor operations (softmax, normalization)
- Loss functions (cross-entropy, MSE)
- Similarity metrics (cosine similarity, distance)

**Neural Networks:**
- Layer implementations (Linear, Conv2d, Pooling)
- Activation functions
- Batch normalization

**Advanced:**
- Attention mechanisms
- Optimization algorithms (SGD, Adam)
- Custom loss functions

**Generative Models:**
- VAE loss (ELBO, KL divergence)
- Diffusion models (noise scheduling, forward/reverse process)
- GAN discriminator/generator basics

**3D/Computer Vision:**
- Point cloud operations
- 3D convolutions
- Mesh processing basics

## Interaction Pattern

**User provides reference:**
> "I have this ML OA prep guide. Create practice problems for it."
> [Attaches meshy-ml-oa-prep.md]

**You respond:**
1. Read and analyze the reference document
2. Summarize the key topics identified
3. Propose a problem set structure (X problems covering Y topics)
4. Ask for confirmation or adjustments
5. Generate all files
6. Show summary of what was created
7. Explain how to use the practice set

**Example response:**
> "I've analyzed your ML OA prep guide. I'll create 9 practice problems covering:
> - Basic operations (2 problems): Softmax, Cross-entropy
> - Tensor operations (3 problems): Cosine similarity, Pairwise distance, Attention
> - CNN fundamentals (2 problems): Conv2d, Max pooling
> - Generative models (2 problems): VAE loss, Diffusion noise scheduling
>
> Each problem will include detailed descriptions, standard solutions with 8+ tests, and automated testing. Sound good?"

## Tips for Success

1. **Read the reference thoroughly**: Don't just skim—understand the domain, context, and what makes these problems relevant

2. **Calibrate difficulty**: Easy problems should be solvable in 5-10 minutes, hard problems in 20-30 minutes

3. **Test everything**: Run each standard solution to ensure it works before finalizing

4. **Make problems self-contained**: Users should be able to solve problems without external resources (besides basic documentation)

5. **Progressive disclosure**: Hints should guide without giving away the solution

6. **Real-world connections**: Always explain practical applications—this motivates learning

7. **Cross-reference thoughtfully**: Link related problems to build connections

## Common Mistakes to Avoid

❌ **Don't make problems too abstract**: Use concrete examples with actual values
❌ **Don't skip mathematical foundations**: Include formulas when relevant
❌ **Don't write trivial tests**: Test edge cases and correctness properties
❌ **Don't ignore difficulty calibration**: Time estimates should be realistic
❌ **Don't forget context**: Always explain why the problem matters
❌ **Don't duplicate effort**: If problems are similar, cross-reference them
❌ **Don't overcomplicate**: Start simple, add complexity progressively

## Output Checklist

Before completing, verify:

- [ ] All problem directories created with consistent numbering
- [ ] Every problem has `problem.md` and `standard_solution.py`
- [ ] Test harness configured for all problems
- [ ] README.md with complete documentation
- [ ] QUICK_START.md with quick reference
- [ ] solution_template.py provided
- [ ] All standard solutions tested and working
- [ ] Cross-references between problems are correct
- [ ] Difficulty progression makes sense
- [ ] Time estimates are realistic
- [ ] Mathematical formulas are correct
- [ ] Code follows style guidelines
- [ ] Documentation is clear and helpful

## Final Delivery

Show the user:

1. **Summary table** of all problems created
2. **Directory structure** overview
3. **Quick start instructions** for using the practice set
4. **Example workflow** showing how to solve one problem
5. **Location** of all generated files

Example summary:
```
✅ Created 9 practice problems for PyTorch OA preparation:

| # | Problem | Difficulty | Time |
|---|---------|------------|------|
| 01 | Implement Softmax | Easy | 5-10 min |
| 02 | Cross Entropy Loss | Medium | 10-15 min |
...

📁 All files created in: /path/to/PyTorch-OA-Common-Questions/

🚀 Quick start:
1. cd PyTorch-OA-Common-Questions
2. cd 01-implement-softmax && cat problem.md
3. cp ../solution_template.py solution.py
4. # Edit solution.py with your implementation
5. cd .. && python test_solutions.py 01

📖 See README.md for full documentation
⚡ See QUICK_START.md for quick reference
```

---

This skill transforms reference materials into comprehensive, production-ready practice problem sets that help users prepare effectively for technical assessments.
