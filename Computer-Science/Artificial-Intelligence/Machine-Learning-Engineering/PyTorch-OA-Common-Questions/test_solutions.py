#!/usr/bin/env python3
"""
Test script to verify your solutions against standard solutions.

Usage:
    python test_solutions.py                    # Test all problems
    python test_solutions.py 01 03 05          # Test specific problems
    python test_solutions.py --verbose         # Show detailed output
"""

import sys
import os
import importlib.util
import torch
from pathlib import Path
from typing import Callable, Any
import traceback


# Problem configurations
PROBLEMS = {
    "01-implement-softmax": {
        "function": "softmax",
        "test_cases": [
            {
                "name": "1D tensor",
                "args": (torch.tensor([1.0, 2.0, 3.0]),),
                "kwargs": {},
            },
            {
                "name": "2D tensor, dim=1",
                "args": (torch.randn(4, 10),),
                "kwargs": {"dim": 1},
            },
            {
                "name": "Large values (numerical stability)",
                "args": (torch.tensor([[1000.0, 2000.0, 3000.0]]),),
                "kwargs": {},
            },
        ],
    },
    "02-cross-entropy-loss": {
        "function": "cross_entropy_loss",
        "test_cases": [
            {
                "name": "Random logits and targets",
                "args": (torch.randn(32, 10), torch.randint(0, 10, (32,))),
                "kwargs": {},
            },
            {
                "name": "Perfect prediction",
                "args": (torch.eye(5) * 100, torch.arange(5)),
                "kwargs": {},
            },
        ],
    },
    "03-cosine-similarity": {
        "function": "cosine_similarity",
        "test_cases": [
            {
                "name": "Random vectors",
                "args": (torch.randn(20, 64), torch.randn(30, 64)),
                "kwargs": {},
            },
            {
                "name": "Orthogonal vectors",
                "args": (torch.tensor([[1.0, 0.0, 0.0]]), torch.tensor([[0.0, 1.0, 0.0]])),
                "kwargs": {},
            },
            {
                "name": "Identical vectors",
                "args": (torch.randn(10, 32), torch.randn(10, 32)),
                "kwargs": {},
                "check": "diagonal_ones",  # Special check for identical input
            },
        ],
    },
    "04-pairwise-distance": {
        "function": "pairwise_distance",
        "test_cases": [
            {
                "name": "Random 3D points",
                "args": (torch.randn(20, 3), torch.randn(30, 3)),
                "kwargs": {},
            },
            {
                "name": "Known 2D distances",
                "args": (
                    torch.tensor([[0.0, 0.0], [1.0, 1.0]]),
                    torch.tensor([[0.0, 0.0], [3.0, 4.0]]),
                ),
                "kwargs": {},
            },
        ],
    },
    "05-attention-mechanism": {
        "function": "scaled_dot_product_attention",
        "test_cases": [
            {
                "name": "Random Q, K, V",
                "args": (torch.randn(2, 10, 32), torch.randn(2, 20, 32), torch.randn(2, 20, 64)),
                "kwargs": {},
            },
            {
                "name": "Self-attention",
                "args": (torch.randn(2, 10, 64),) * 3,  # Q = K = V
                "kwargs": {},
            },
            {
                "name": "With causal mask",
                "args": (torch.randn(2, 5, 64),) * 3,
                "kwargs": {
                    "mask": torch.triu(torch.ones(5, 5), diagonal=1).bool().unsqueeze(0).expand(2, -1, -1)
                },
            },
        ],
    },
    "06-conv2d-layer": {
        "function": "conv2d",
        "test_cases": [
            {
                "name": "Basic 3x3 conv, stride=1, padding=1",
                "args": (torch.randn(2, 3, 28, 28), torch.randn(16, 3, 3, 3)),
                "kwargs": {"stride": 1, "padding": 1},
            },
            {
                "name": "Strided conv with bias",
                "args": (torch.randn(2, 3, 28, 28), torch.randn(8, 3, 5, 5), torch.randn(8)),
                "kwargs": {"stride": 2, "padding": 2},
            },
        ],
    },
    "07-vae-loss": {
        "function": "vae_loss",
        "test_cases": [
            {
                "name": "Image VAE",
                "args": (torch.randn(16, 1, 28, 28), torch.randn(16, 1, 28, 28), torch.randn(16, 32), torch.randn(16, 32)),
                "kwargs": {"beta": 1.0},
            },
            {
                "name": "Beta-VAE",
                "args": (torch.randn(8, 784), torch.randn(8, 784), torch.randn(8, 64), torch.randn(8, 64)),
                "kwargs": {"beta": 2.0},
            },
        ],
    },
    "08-diffusion-noise-schedule": {
        "function": "forward_diffusion",
        "test_cases": [
            {
                "name": "Forward diffusion at different timesteps",
                "args": (torch.randn(4, 3, 32, 32), torch.tensor([0, 250, 500, 999])),
                "kwargs": {},
                "setup": lambda: ("alphas_cumprod", torch.cumprod(1.0 - torch.linspace(0.0001, 0.02, 1000), dim=0)),
            },
        ],
    },
    "09-max-pooling": {
        "function": "max_pool2d",
        "test_cases": [
            {
                "name": "2x2 pooling",
                "args": (torch.randn(4, 16, 32, 32),),
                "kwargs": {"kernel_size": 2, "stride": 2},
            },
            {
                "name": "3x3 pooling with stride=1",
                "args": (torch.randn(2, 3, 28, 28),),
                "kwargs": {"kernel_size": 3, "stride": 1},
            },
        ],
    },
}


def load_module(module_path: Path, module_name: str):
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def compare_outputs(your_output: Any, standard_output: Any, atol: float = 1e-5) -> tuple[bool, str]:
    """Compare two outputs and return (match, message)."""
    # Handle tuple outputs (e.g., VAE loss returns 3 values)
    if isinstance(standard_output, tuple):
        if not isinstance(your_output, tuple):
            return False, f"Expected tuple output, got {type(your_output)}"
        if len(your_output) != len(standard_output):
            return False, f"Expected {len(standard_output)} outputs, got {len(your_output)}"

        for i, (yours, standard) in enumerate(zip(your_output, standard_output)):
            match, msg = compare_outputs(yours, standard, atol)
            if not match:
                return False, f"Output {i}: {msg}"
        return True, "All outputs match"

    # Handle tensor outputs
    if isinstance(standard_output, torch.Tensor):
        if not isinstance(your_output, torch.Tensor):
            return False, f"Expected tensor, got {type(your_output)}"

        if your_output.shape != standard_output.shape:
            return False, f"Shape mismatch: {your_output.shape} vs {standard_output.shape}"

        if not torch.allclose(your_output, standard_output, atol=atol, rtol=1e-5):
            max_diff = (your_output - standard_output).abs().max().item()
            return False, f"Values differ (max diff: {max_diff:.2e})"

        return True, "Tensors match"

    # Handle other types
    if your_output != standard_output:
        return False, f"Value mismatch: {your_output} vs {standard_output}"

    return True, "Values match"


def test_problem(problem_dir: str, verbose: bool = False) -> dict:
    """Test a single problem."""
    base_path = Path(__file__).parent / problem_dir

    result = {
        "problem": problem_dir,
        "exists": False,
        "imported": False,
        "tests_passed": 0,
        "tests_failed": 0,
        "errors": [],
    }

    # Check if user solution exists
    user_solution_path = base_path / "solution.py"
    standard_solution_path = base_path / "standard_solution.py"

    if not user_solution_path.exists():
        result["errors"].append("solution.py not found")
        return result

    result["exists"] = True

    if not standard_solution_path.exists():
        result["errors"].append("standard_solution.py not found")
        return result

    # Load modules
    try:
        user_module = load_module(user_solution_path, f"user_{problem_dir.replace('-', '_')}")
        standard_module = load_module(standard_solution_path, f"standard_{problem_dir.replace('-', '_')}")
    except Exception as e:
        result["errors"].append(f"Import error: {str(e)}")
        return result

    result["imported"] = True

    # Get function name
    config = PROBLEMS.get(problem_dir, {})
    func_name = config.get("function")

    if not func_name:
        result["errors"].append(f"No test configuration found")
        return result

    # Get functions
    if not hasattr(user_module, func_name):
        result["errors"].append(f"Function '{func_name}' not found in your solution")
        return result

    if not hasattr(standard_module, func_name):
        result["errors"].append(f"Function '{func_name}' not found in standard solution")
        return result

    user_func = getattr(user_module, func_name)
    standard_func = getattr(standard_module, func_name)

    # Run test cases
    test_cases = config.get("test_cases", [])

    for i, test_case in enumerate(test_cases):
        test_name = test_case.get("name", f"Test {i+1}")
        args = test_case.get("args", ())
        kwargs = test_case.get("kwargs", {})

        # Setup additional kwargs if needed (e.g., alphas_cumprod for diffusion)
        if "setup" in test_case:
            setup_func = test_case["setup"]
            key, value = setup_func()
            kwargs[key] = value

        try:
            # Run both functions
            your_output = user_func(*args, **kwargs)
            standard_output = standard_func(*args, **kwargs)

            # Compare outputs
            match, message = compare_outputs(your_output, standard_output)

            if match:
                result["tests_passed"] += 1
                if verbose:
                    print(f"  ✓ {test_name}: {message}")
            else:
                result["tests_failed"] += 1
                result["errors"].append(f"{test_name}: {message}")
                if verbose:
                    print(f"  ✗ {test_name}: {message}")

        except Exception as e:
            result["tests_failed"] += 1
            error_msg = f"{test_name}: {type(e).__name__}: {str(e)}"
            result["errors"].append(error_msg)
            if verbose:
                print(f"  ✗ {error_msg}")
                traceback.print_exc()

    return result


def main():
    """Main test runner."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Get problem numbers from command line
    problem_nums = [arg for arg in sys.argv[1:] if arg.isdigit() or (arg.startswith("0") and arg[1:].isdigit())]

    if problem_nums:
        # Test specific problems
        problems_to_test = [f"{num.zfill(2)}-{name}" for num in problem_nums
                           for name in PROBLEMS.keys() if name.startswith(num.zfill(2))]
    else:
        # Test all problems
        problems_to_test = sorted(PROBLEMS.keys())

    print("=" * 70)
    print("PyTorch OA Practice - Solution Checker")
    print("=" * 70)
    print()

    results = []

    for problem_dir in problems_to_test:
        print(f"Testing: {problem_dir}")
        result = test_problem(problem_dir, verbose)
        results.append(result)

        if not result["exists"]:
            print("  ⊘ No solution file found (skipped)")
        elif not result["imported"]:
            print("  ✗ Import failed:")
            for error in result["errors"]:
                print(f"    - {error}")
        else:
            total_tests = result["tests_passed"] + result["tests_failed"]
            if result["tests_failed"] == 0:
                print(f"  ✅ All {total_tests} tests passed!")
            else:
                print(f"  ❌ {result['tests_failed']}/{total_tests} tests failed")
                if not verbose:
                    print("  Errors:")
                    for error in result["errors"]:
                        print(f"    - {error}")
        print()

    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)

    total_problems = len([r for r in results if r["exists"]])
    passed_problems = len([r for r in results if r["exists"] and r["tests_failed"] == 0 and r["imported"]])

    total_tests = sum(r["tests_passed"] + r["tests_failed"] for r in results)
    passed_tests = sum(r["tests_passed"] for r in results)

    print(f"Problems: {passed_problems}/{total_problems} passed")
    print(f"Tests: {passed_tests}/{total_tests} passed")
    print()

    if passed_problems == total_problems and total_problems > 0:
        print("🎉 Congratulations! All solutions are correct!")
    elif passed_problems > 0:
        print("💪 Keep going! You're making progress!")
    else:
        print("📚 Start with the easier problems and work your way up!")

    print()

    # Exit with error code if any tests failed
    sys.exit(0 if passed_problems == total_problems else 1)


if __name__ == "__main__":
    main()
