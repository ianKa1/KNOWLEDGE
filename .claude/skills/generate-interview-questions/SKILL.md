---
name: generate-interview-questions
description: Generate targeted technical interview questions with full answers for a specific topic and role. Use this skill when users are preparing for a technical interview, want practice questions, say things like "I have an interview about X", "help me prepare for a Y interview", "generate interview questions on Z", or "what might they ask me about X?". Especially useful when the topic is already in the knowledge base — save the output there. Always trigger this skill when interview prep is mentioned, even casually.
---

# Generate Interview Questions

This skill generates a set of realistic technical interview questions — with full, detailed answers — tailored to a specific topic and role context.

## What This Skill Does

1. **Gathers context** — role, company, and the user's own background
2. **Clarifies the topic** — what technical area is being tested and at what depth
3. **Designs a question set** — 15–20 questions spanning easy to hard, organized by theme
4. **Writes full answers** — complete explanations a candidate could study and internalize
5. **Saves the output** — as a markdown file in the appropriate place in the knowledge tree

## Step 1: Gather Context

Before generating questions, collect enough context to make the questions genuinely useful. Some of this may already be in the conversation — extract it before asking. Only ask for what's actually missing.

**Ask the user to share any of the following that they have:**

- **Job description** — if they have it, read it carefully. The JD often reveals the exact technologies, scale, and problem domains the team cares about. Questions should reflect this.
- **Company background** — startup vs. big tech changes the question balance significantly (see calibration guide below). If the user knows the company's product or tech stack, that shapes what "applied" questions are relevant.
- **Their own skill profile** — what do they already know well vs. where are their gaps? This helps decide where to focus harder questions and where to add more foundational coverage. If the knowledge base is available, check the relevant topic nodes to understand their current level.

If none of this is available, ask directly: "Do you have a job description or know more about the company? And how would you rate your familiarity with [topic] — strong fundamentals, or still building?" Then proceed with whatever the user provides.

**Calibration guide by role type:**

| Role | Question balance |
|---|---|
| Research (academia/lab) | Heavy on theory, intuition, "why does X work", paper-level knowledge |
| ML Engineer (big tech) | Systems thinking, scalability, profiling, integration with frameworks |
| ML Engineer (startup) | Mixed: practical coding + enough theory to debug weird failures |
| Research Engineer (startup) | ~50/50: can you read a paper AND implement it efficiently |
| SWE with ML component | Conceptual understanding, not deep implementation |

## Step 2: Design the Question Set

Organize questions into 4–5 thematic sections, ordered easy → hard within each section. Aim for 15–20 questions total.

Good section structure (adapt per topic):
- **Conceptual Foundations** — definitions, mental models, core mechanisms
- **Memory & Performance** — bottlenecks, profiling, hardware constraints
- **Topic-Specific Applied** — domain-specific scenarios tied to the role's actual work
- **Debugging & Profiling** — how to diagnose slow/broken things
- **Harder / Synthesis** — open-ended, design-level, or multi-concept questions

Scale difficulty to the role: a research role needs harder synthesis questions; a startup engineer role needs more "how would you debug this" questions. If the user flagged specific weak areas, include more questions there — interview prep is most valuable where the gaps are.

## Step 3: Write Full Answers

Each answer should be written so the user can **study it and internalize it**, not just skim it.

Good answers:
- Explain the **mechanism**, not just the outcome ("it's slow because..." not just "it's slow")
- Include **concrete examples** — short code snippets, ASCII diagrams, or tables where they clarify
- Call out **trade-offs** and **common mistakes** where relevant
- For synthesis questions, walk through the reasoning process, not just the conclusion

Avoid:
- Bullet-point summaries that skip the why
- Answers so long they're exhausting to read — be precise, not comprehensive
- Repeating the same explanation across multiple answers

## Step 4: Save the Output

Save the questions and answers as a markdown file in the knowledge base under the most relevant topic node.

**File path**: mirror the TREE.md hierarchy for the topic. For example:
- CUDA questions → `Computer-Science/Hardware/GPU-Computing/CUDA-Basics/cuda-interview-questions.md`
- KV Cache questions → `Computer-Science/Artificial-Intelligence/Machine-Learning-Engineering/LLM-Serving/Inference-Optimization/KV-Cache/kv-cache-interview-questions.md`

If the topic node doesn't exist yet, note it and suggest running `supplement-node` first.

**File structure:**
```markdown
# [Topic] Interview Questions

Brief context line: role, level, focus.

---

## [Section Name]

**Q1. [Question]**

[Full answer — explanation, examples, trade-offs]

---

**Q2. [Question]**

[Full answer]

...

## Related Topics
- [Links to related knowledge base files]
```

## What Good Output Looks Like

- Questions feel like something a real interviewer would ask — not textbook definitions
- Answers are thorough but readable — a motivated candidate could study them in one sitting
- The difficulty ramp is real — early questions are accessible, late questions require synthesis
- Domain-specific questions connect the topic to the actual role and company context
- Weak areas the user flagged get proportionally more coverage
- The file is saved in the right place and cross-linked to related nodes
