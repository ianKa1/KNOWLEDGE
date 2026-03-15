---
name: supplement-node
description: Adds content, notes, articles, concepts, or learning material to a hierarchical knowledge base tree. Use when users provide educational content they want to organize, have notes to add, articles to save, or any learning material about computer science topics. Automatically determines the right place in the tree, creates missing parent nodes, and saves content as markdown files with cross-references.
---

# Supplement Node

This skill organizes knowledge content into a hierarchical tree structure, creating nodes and directories as needed.

## Two Modes of Input

The user may provide either:

- **Rich content** — an article, notes, a detailed explanation, or a file. Analyze what it's about and place it.
- **Topic directions** — keywords, topic names, or hints like "kubernetes, vLLM, inference acceleration". These are not node names to copy verbatim; they are directions pointing at a knowledge area.

**When the input is topic directions**, your job is to think about the logical structure of that knowledge area yourself. The user is telling you what they're interested in, not dictating the tree shape. Derive the right hierarchy from first principles: what are the natural parent categories? What sub-topics are mandatory to understand the area? How do the user's keywords relate to each other — are some subtopics of others? Only then propose a tree.

## How It Works

1. **Read the existing tree** from `TREE.md`
2. **Analyze the input** to determine whether it's rich content or topic directions
3. **Design the subtree** — for topic directions, reason about the logical structure independently before writing anything. Ask: what's the natural hierarchy here? Which of the user's terms are categories vs. specific tools vs. techniques? How do they nest?
4. **Propose the subtree to the user** (see User-in-the-Loop section below) and wait for approval
5. **Create directory structure** for approved nodes
6. **Save content files** in the appropriate directories
7. **Update TREE.md** with approved nodes

## Tree Structure

The knowledge tree is maintained in `TREE.md` at the project root using markdown nested lists with **short descriptions** (max 10 words) after each node:

```markdown
# Knowledge Tree

- Computer Science - Foundational computing concepts and theory
  - Algorithms - Problem-solving techniques and complexity analysis
    - Sorting - Arranging data in specific order
    - Graph Algorithms - Algorithms for graph traversal and analysis
  - Data Structures - Ways to organize and store data
    - Trees - Hierarchical data structure with nodes
    - Hash Tables - Key-value data structure for fast lookup
  - Programming Languages - Languages for software development
    - Python - High-level interpreted general-purpose language
    - JavaScript - Web programming and scripting language
```

**Format**: `- Node Name - Short description (max 10 words)`

Each indent level represents one level in the hierarchy. Descriptions help users quickly understand what each topic covers without opening files.

## Directory Structure

Directories mirror the tree structure. For example:

```
/
├── TREE.md
├── Computer-Science/
│   ├── Algorithms/
│   │   ├── Sorting/
│   │   │   └── quicksort.md
│   │   └── Graph-Algorithms/
│   └── Data-Structures/
│       ├── Trees/
│       └── Hash-Tables/
```

Directory names use PascalCase or kebab-case and match the tree node names (spaces converted to hyphens).

## User-in-the-Loop: Propose Before Acting

Before creating any files or modifying `TREE.md`, always present your proposed subtree to the user and wait for their approval. This is mandatory — never skip ahead.

Format the proposal in two parts: the requested nodes first, then any missing prerequisites separately so the user can easily prune what they already know.

```
Here's what I'd add for the requested topics:

  [under Machine Learning Engineering]
  - LLM Serving - Infrastructure for deploying large language models
    - Distributed LLM Systems - Multi-node parallelism and deployment
    - Inference Optimization - Techniques to reduce latency and increase throughput
      - vLLM - High-throughput inference engine using PagedAttention

  [new branch under Computer Science]
  - Systems
    - Container Orchestration
      - Kubernetes - Open-source container orchestration platform

These prerequisites are currently missing from the tree — I'd add them too
for a smooth learning path:

  [under Deep Learning]
  - Transformer Architecture - Self-attention based sequence model
    - Attention Mechanism - Scaled dot-product attention
    - KV Cache - Key-value cache for autoregressive inference

  [under Systems]
  - Containers - OS-level process isolation and packaging
    - Docker - Build, ship, and run containerized applications

  [new branch under Computer Science]
  - Hardware
    - GPU Computing - Parallel processing for ML workloads
      - GPU Memory Hierarchy - HBM, SRAM, bandwidth vs compute tradeoffs

Prune anything you already know or don't want. I'll only create what you approve.
```

Then wait. The user may:
- Approve as-is → proceed to file creation
- Remove nodes → respect exactly what they prune
- Ask to restructure → revise the proposal and show it again

Do not proceed to Step 5 (creating directories) until the user explicitly approves.

## Workflow

#### Step 1: Read the existing tree

First, read `TREE.md` from the project root to understand the current structure. If it doesn't exist, create it with a basic starting structure:

```markdown
# Knowledge Tree

- Computer Science
```

#### Step 2: Analyze the input

If the input is **rich content**: understand what it's about — domain, specificity, related topics already in the tree.

If the input is **topic directions**: reason about the logical structure of the knowledge area. Think about:
- Which terms are broad categories vs. specific tools vs. techniques?
- How do the terms relate — are some subtopics of others?
- What intermediate nodes are logically mandatory even if the user didn't mention them?
- Where in the existing tree does this area belong?

**Example reasoning for "kubernetes, LLM distributed system, vLLM-omni, inference accelerator":**
- "LLM distributed system" → broad deployment category → should be a parent node
- "inference accelerator" → a category of techniques (quantization, speculative decoding, etc.) → child of a serving parent
- "vLLM" → a specific tool that *implements* inference optimization → child of "inference acceleration", not a sibling
- "kubernetes" → general infrastructure tool, not ML-specific → belongs in a separate "Systems" branch

So the hierarchy would be: `LLM Serving → Inference Optimization → vLLM`, not three siblings.

#### Step 3: Design the subtree

Sketch the complete subtree before writing anything. Include nodes the user didn't explicitly mention but that are logically necessary as parents or groupings. Verify:
- No orphan nodes (every new node has a logical parent)
- Correct depth — tools/implementations are deeper than categories
- Siblings are genuinely at the same level of abstraction

**Also identify missing prerequisites.** For each new node being added, ask: "What does a learner need to understand *before* this?" Then check whether those prerequisite topics exist in the current tree. If they don't, add them to the proposal too.

The goal is a smooth learning curve — someone should be able to navigate the tree from foundational concepts down to the new nodes without hitting unexplained jumps. If a prerequisite is already in the tree, just note the dependency (via Related Topics in the content file). If it's absent, propose it as an additional node.

**Example:** Adding `vLLM` and `Kubernetes` without first having `Transformer Architecture` (needed to understand KV cache → PagedAttention) and `Containers / Docker` (needed to understand what Kubernetes orchestrates) creates a cliff. Propose those prerequisite nodes alongside the requested ones, clearly labeled so the user can prune what they already know.

#### Step 4: Propose and get approval

Present the proposed subtree to the user as shown in the User-in-the-Loop section. Wait for their response before continuing.

#### Step 5: Create directory structure

Once approved, create directories for all new nodes. Use the full path from root to leaf:

```bash
mkdir -p "Computer-Science/Algorithms/Sorting"
```

Directory names should match the tree node names with spaces replaced by hyphens.

#### Step 6: Update TREE.md

Add the approved nodes to the tree at the appropriate location:

**Format**: `- Node Name - Short description (max 10 words)`

**Writing good descriptions**:
- Focus on **what** the topic is, not why it's useful
- Be specific and clear
- Good: "Shortest path algorithm for weighted graphs"
- Bad: "Important algorithm" (too vague)

Maintain proper indentation (2 spaces per level). Keep the tree alphabetically sorted within each level.

#### Step 7: Save the content

Create a markdown file in the deepest (most specific) directory:

**Filename**: Use a descriptive kebab-case name based on the specific topic (e.g., `quicksort.md`, `binary-search-trees.md`, `python-decorators.md`)

**Content structure**:
```markdown
# [Topic Name]

## Overview
[Brief description of what this is]

## Content
[The actual knowledge content]

## Related Topics
- [Link to related topic 1]
- [Link to related topic 2]

## References
[Any sources or further reading]
```

The "Related Topics" section helps create internal connections across the knowledge base.

#### Step 8: Confirm with user

Show the user:
- Where the content was placed in the tree
- The file paths created
- Suggested related topics to cross-link

## Examples

**Example 1: Rich content — an article about Quick Sort**

Input: "Quick sort is a divide-and-conquer sorting algorithm..."

Process:
1. Read TREE.md — identify as rich content
2. Analyze: specific sorting algorithm
3. Design subtree: "Algorithms" → "Sorting" → "Quick Sort" (create missing parents)
4. Propose to user: show the subtree, wait for approval
5. Create: `Computer-Science/Algorithms/Sorting/`
6. Update TREE.md
7. Save: `Computer-Science/Algorithms/Sorting/quicksort.md`

**Example 2: Topic directions — "kubernetes, LLM distributed system, vLLM, inference accelerator"**

Input: keywords, no detailed content

Process:
1. Read TREE.md — identify as topic directions
2. Reason about structure:
   - "LLM distributed system" = broad deployment parent
   - "inference accelerator" = category of optimization techniques (quantization, speculative decoding…) → child of serving
   - "vLLM" = specific tool implementing inference optimization → child of "Inference Optimization", not a sibling to it
   - "kubernetes" = general infra tool, not ML-specific → separate "Systems" branch
3. Design subtree:
   ```
   Machine Learning Engineering
     └── LLM Serving
           ├── Distributed LLM Systems
           └── Inference Optimization
                 └── vLLM
   Systems (new branch)
     └── Container Orchestration
           └── Kubernetes
   ```
4. Propose subtree to user, wait for approval/pruning
5. After approval: create directories, update TREE.md, write content files

## Important Principles

**Nodes are subjects, not properties**: This is critical. Every node in the tree should represent a **subject or topic you can study**, not a property, attribute, or document section.

**Good nodes** (subjects to learn):
- "Mesh Topology" - a concept you can study
- "Graph Algorithms" - a category of algorithms
- "Python" - a programming language
- "WebSockets" - a protocol/technology

**Bad nodes** (properties/sections/lists):
- ❌ "3D Geometry Quality" - this is a property of meshes, not a subject. Quality metrics should be covered in "Mesh Topology" or "Mesh Representations"
- ❌ "Common Problems" - this is a section within a document, not a standalone subject
- ❌ "Best Practices" - belongs as a section in relevant topics
- ❌ "Advantages and Disadvantages" - belongs in the document for the actual topic

**How to decide**: Ask "Can I study this as a topic?" vs. "Is this an aspect/property of something else?"
- "Can I study Mesh Topology?" → YES, it's a subject (vertices, edges, faces, manifolds)
- "Can I study 3D Geometry Quality?" → NO, quality is a property. Study "Mesh Topology" and quality will be covered as part of it

**Where do properties/aspects go?** They belong as **sections within the document** for the actual subject:
```markdown
# Mesh Topology

## Overview
[What mesh topology is]

## Core Concepts
[Vertices, edges, faces]

## Quality Metrics ← property/aspect as a section
- Manifold vs non-manifold
- Watertight
- Orientation

## Common Problems ← issues as a section
- Holes
- Flipped normals
- Degenerate triangles
```

**Semantic understanding over keyword matching**: Don't just look for exact word matches. Understand what the content is actually about. "Hash maps" and "Hash tables" are the same thing. "Big O notation" belongs under "Algorithm Analysis", not as a sibling to "Algorithms".

**Build complete paths**: Never create orphan nodes. If you're adding "Red-Black Trees", make sure "Trees" → "Balanced Trees" exists too if that's the logical hierarchy.

**Maintain readability**: The tree should read naturally. Someone should be able to scan TREE.md and understand the knowledge organization at a glance.

**Create connections**: Use the "Related Topics" section in each markdown file to link to conceptually related content elsewhere in the tree. This makes the knowledge base interconnected, not just hierarchical.

**Depth vs breadth**: Prefer deeper, more specific organization over broad, flat categories. "Python → Object-Oriented Programming → Decorators" is better than "Programming Languages → Decorators".

## Edge Cases

**Content spans multiple topics**: If the content naturally fits in multiple places (e.g., "Dynamic Programming in Python" fits under both "Algorithms" and "Python"), create a primary location based on the main focus, and add cross-references in the Related Topics sections.

**Refactoring the tree**: If you notice the tree structure could be improved (e.g., a node has too many direct children and should be split into subcategories), suggest it to the user but don't reorganize without asking.

**Different content types**: Some content might be a broad overview, others are specific examples. Use your judgment:
- Broad overviews: Higher in the tree
- Specific implementations/examples: Deeper in the tree
- Tutorials/guides: Could have their own subtree if there are many

## File Naming

- Use kebab-case: `binary-search-trees.md`, not `Binary Search Trees.md`
- Be specific: `quicksort.md` not `algorithm.md`
- Avoid redundancy: In `Sorting/quicksort.md`, don't name it `quicksort-sorting.md`

## Success Criteria

After adding content, the user should be able to:
- Find the content by navigating the tree structure
- Discover related content through cross-links
- Understand where this topic fits in the bigger picture
- See a clear, logical organization of their knowledge base
