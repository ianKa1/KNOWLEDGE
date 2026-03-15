# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repository is a personal knowledge organization system for computer science topics. The goal is to create a structured, interconnected learning framework that makes complex CS concepts easy to understand and navigate.

**Core Principles:**
- **Easy to read**: Content should be clear, well-formatted, and accessible
- **Well-structured**: Organize knowledge hierarchically and logically
- **Internally related**: Create meaningful connections between related topics
- **Study-focused**: Optimize for learning and retention, not just reference

## Repository Structure

- **`TREE.md`** — the master knowledge index; the single source of truth for what exists
- **`.claude/skills/`** — skill definitions for common workflows (supplement-node, break-down, generate-code-assessment)
- **Content directories** — created on demand, mirror the TREE.md hierarchy (e.g., `Computer-Science/Algorithms/Sorting/`)

## TREE.md Format

```markdown
- Node Name - Short description (max 10 words)
  - Child Node - Short description
```

Rules:
- 2-space indent per level
- Alphabetically sorted within each level
- Descriptions focus on **what** the topic is, not why it matters
- Bracketed lists `[item1, item2]` at end of a node indicate subtopics listed inline rather than as child nodes

## Content Files

Files live in the directory matching their node's path in the tree. Naming: `kebab-case.md`.

Standard structure:
```markdown
# Topic Name

## Overview
[Brief description]

## Content
[The actual knowledge]

## Related Topics
- [Link to related topic]

## References
[Sources or further reading]
```

## Directory Naming

Match tree node names with spaces replaced by hyphens. Use PascalCase or kebab-case consistently within a subtree.

## Key Principles When Adding Knowledge

**Nodes are subjects, not properties.** Every tree node must be a topic someone can study independently. "Mesh Topology" is a subject. "Quality Metrics" is a property — it belongs as a section inside a content file, not its own node.

**Build complete paths.** Never create orphan nodes. Adding "Quick Sort" requires "Algorithms" → "Sorting" to exist first.

**Prioritize clarity over completeness.** Well-explained foundational topics beat comprehensive-but-unclear coverage.

**Build connections.** Use "Related Topics" sections to cross-link concepts across the tree.

**Think like a learner.** Structure content in the order someone would naturally learn it.

## Available Skills

Use these via the Skill tool when the user's request matches:

- **`supplement-node`** — add content/notes/articles to the knowledge tree; handles placement, directory creation, and TREE.md updates
- **`break-down`** — analyze a problem/question and generate a prerequisite knowledge tree showing what to learn
- **`generate-code-assessment`** — create structured practice problem sets with solutions and automated tests (targets ML/AI/PyTorch)
