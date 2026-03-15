---
name: supplement-node
description: Adds content, notes, articles, concepts, or learning material to a hierarchical knowledge base tree. Use when users provide educational content they want to organize, have notes to add, articles to save, or any learning material about computer science topics. Automatically determines the right place in the tree, creates missing parent nodes, and saves content as markdown files with cross-references.
---

# Supplement Node

This skill organizes knowledge content into a hierarchical tree structure, creating nodes and directories as needed.

## How It Works

When the user provides content (text, file, article, notes, concepts, etc.):

1. **Reads the existing knowledge tree** from `TREE.md` in the project root
2. **Analyzes the content** to understand what topic/subject it covers
3. **Finds the appropriate location** in the tree based on semantic understanding
4. **Creates missing parent nodes** if the content needs intermediate categories that don't exist yet
5. **Creates directory structure** matching the tree hierarchy
6. **Saves content** as markdown files in the appropriate subject directory
7. **Updates TREE.md** with any new nodes added

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

## Workflow

#### Step 1: Read the existing tree

First, read `TREE.md` from the project root to understand the current structure. If it doesn't exist, create it with a basic starting structure:

```markdown
# Knowledge Tree

- Computer Science
```

#### Step 2: Analyze the new content

Understand what the content is about:
- What's the main topic or concept?
- What domain does it belong to (algorithms, systems, languages, etc.)?
- Is it a broad overview or a specific subtopic?
- What related topics already exist in the tree?

#### Step 3: Determine placement

Find where this content fits:

- **Exact match**: Does a node already exist for this exact topic? Use it.
- **Subtopic**: Is this a more specific version of an existing topic? Create a child node.
- **New branch**: Is this a new area not covered yet? Create new nodes.

**Critical: Build the path level by level.** If the content is about "Quick Sort" but you don't have "Algorithms" → "Sorting" yet, create both parent nodes first:
1. Add "Algorithms" under "Computer Science" (if missing)
2. Add "Sorting" under "Algorithms" (if missing)
3. Add "Quick Sort" under "Sorting"

#### Step 4: Update TREE.md

Add the new node(s) to the tree at the appropriate location with short descriptions:

**Format**: `- Node Name - Short description (max 10 words)`

**Writing good descriptions**:
- Focus on **what** the topic is, not why it's useful
- Be specific and clear
- Good: "Shortest path algorithm for weighted graphs"
- Bad: "Important algorithm" (too vague)
- Bad: "An essential technique used in many applications" (too wordy, focuses on why not what)

Maintain proper indentation (2 spaces per level). Keep the tree alphabetically sorted within each level for easy navigation.

#### Step 5: Create directory structure

Create directories for any new nodes in the path. Use the full path from root to leaf:

```bash
mkdir -p "Computer-Science/Algorithms/Sorting"
```

Directory names should match the tree node names with spaces replaced by hyphens.

#### Step 6: Save the content

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

#### Step 7: Confirm with user

Show the user:
- Where the content was placed in the tree
- The file path created
- Any new nodes added
- Suggested related topics to cross-link

## Examples

**Example 1: Adding content about Quick Sort**

Input: "Quick sort is a divide-and-conquer sorting algorithm..."

Process:
1. Read TREE.md
2. Analyze: This is about a specific sorting algorithm
3. Check tree: Need "Computer Science" → "Algorithms" → "Sorting" → "Quick Sort"
4. Found: "Computer Science" exists, but "Algorithms" doesn't
5. Add nodes: "Algorithms" (under CS), "Sorting" (under Algorithms), "Quick Sort" (under Sorting)
6. Create: `Computer-Science/Algorithms/Sorting/`
7. Save: `Computer-Science/Algorithms/Sorting/quicksort.md`
8. Update TREE.md with all new nodes

**Example 2: Adding content to existing category**

Input: "Merge sort is another efficient sorting algorithm..."

Process:
1. Read TREE.md (now has the Sorting node from Example 1)
2. Analyze: Another sorting algorithm
3. Check tree: "Sorting" node exists
4. Add node: "Merge Sort" under existing "Sorting"
5. Directory exists: `Computer-Science/Algorithms/Sorting/`
6. Save: `Computer-Science/Algorithms/Sorting/mergesort.md`
7. Update TREE.md with just "Merge Sort" node
8. Suggest cross-link to quicksort.md in Related Topics

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
