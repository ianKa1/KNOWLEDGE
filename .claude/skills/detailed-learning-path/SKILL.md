---
name: detailed-learning-path
description: Generate comprehensive, structured learning guides for technologies and concepts. Creates detailed study plans with theory, practice, curated resources, and progression from beginner to advanced. Use this skill when users want to learn a new technology deeply, need a study roadmap, ask "how do I learn X?", want to create learning materials, or after running break-down/supplement-node skills to create actionable study plans. Triggers on phrases like "create a learning path", "how do I study this?", "make a study guide", "I want to learn X thoroughly", or when users need structured guidance for mastering a topic.
---

# Detailed Learning Path

This skill generates comprehensive, actionable learning guides that take users from beginner to proficient in a technology or concept. It combines theoretical understanding, practical exercises, curated resources, and structured progression.

## What This Skill Does

Creates a `LEARNING_PATH.md` file (or similar) for a technology/concept that includes:

1. **Technology Overview** - What it is, why it matters, when to use it
2. **Prerequisites** - What you should know first
3. **Study Plan** - Step-by-step progression from fundamentals to advanced
4. **Curated Resources** - High-quality tutorials, docs, videos, courses
5. **Practical Exercises** - Hands-on projects and demos
6. **Learning Milestones** - Checkpoints to verify understanding
7. **Common Pitfalls** - What beginners struggle with
8. **Next Steps** - Where to go after mastering the basics

## When to Use This Skill

Use this skill when:
- User wants to learn a new technology or concept thoroughly
- After running `break-down` to understand prerequisites
- After running `supplement-node` to add a new topic to the knowledge tree
- User asks "how do I learn X?" or "create a study plan for Y"
- Building educational materials or onboarding docs
- User needs structured guidance with curated resources

## Input Requirements

The user should provide:
1. **Topic/Technology name** (e.g., "Kubernetes", "Diffusion Models", "React Hooks")
2. **Target knowledge level** (optional: beginner/intermediate/advanced, default: beginner)
3. **Learning context** (optional: e.g., "for building 3D AI apps", "for web development")
4. **Time commitment** (optional: e.g., "2 weeks intensive", "3 months part-time")
5. **Existing knowledge** (optional: what they already know that relates)

## Output Structure

Create a comprehensive `LEARNING_PATH.md` file:

```markdown
# Learning Path: [Technology Name]

## Overview

### What is [Technology]?
[2-3 paragraph explanation of what this technology is and its core concepts]

### Why Learn This?
[Real-world applications and benefits]
- **Use Case 1**: Description
- **Use Case 2**: Description
- **Use Case 3**: Description

### When to Use [Technology]
[Scenarios where this technology is the right choice]

### When NOT to Use It
[Limitations and alternative scenarios]

### Advantages
- ✅ Advantage 1
- ✅ Advantage 2
- ✅ Advantage 3

### Disadvantages
- ⚠️ Disadvantage 1
- ⚠️ Disadvantage 2

### Alternatives
- **Alternative 1**: When to use instead, comparison
- **Alternative 2**: When to use instead, comparison

## Prerequisites

### Required Knowledge
- [ ] Prerequisite 1 - [Link to learning resource if it exists in knowledge base]
- [ ] Prerequisite 2
- [ ] Prerequisite 3

### Recommended Background
- Topic 1 (helpful but not essential)
- Topic 2

### Setup Requirements
- Tool/software installations needed
- Development environment setup
- Account registrations (if any)

## Learning Path

### Phase 1: Foundations (Week 1-2)
**Goal**: Understand core concepts and terminology

#### Topics to Master
1. **Core Concept 1**
   - What it is and why it matters
   - Key terminology
   - Simple examples

2. **Core Concept 2**
   - Explanation
   - How it relates to Concept 1

**Learning Activities**:
- [ ] Read [Resource Name] (link)
- [ ] Watch [Video Tutorial] (link, duration)
- [ ] Complete [Interactive Tutorial] (link)

**Practical Exercise**:
```
[Step-by-step exercise description]
Goal: Build [simple thing]
Time: ~X hours
```

**Checkpoint**: You should be able to:
- [ ] Explain [concept] in your own words
- [ ] Build a simple [thing]
- [ ] Understand when to use [technology]

---

### Phase 2: Intermediate Concepts (Week 3-4)
**Goal**: [Next level goal]

#### Topics to Master
1. **Advanced Topic 1**
2. **Advanced Topic 2**

**Learning Activities**:
[Curated resources]

**Practical Exercise**:
[More complex project]

**Checkpoint**: You should be able to:
[Validation criteria]

---

### Phase 3: Advanced Topics (Week 5-6)
**Goal**: [Advanced mastery goal]

[Continue pattern...]

---

### Phase 4: Real-World Application (Week 7-8)
**Goal**: Build production-ready solutions

[Project-based learning]

## Curated Resources

### Official Documentation
- 📚 [Official Docs](link) - Complete reference
- 📖 [Getting Started Guide](link) - Official tutorial

### Best Tutorials
⭐ = Highly recommended

- ⭐ **[Tutorial Name](link)** - [Brief description, why it's good, difficulty level]
  - Format: Video/Text/Interactive
  - Duration: X hours
  - Level: Beginner/Intermediate/Advanced

- **[Another Tutorial](link)** - [Description]

### Video Courses
- ⭐ **[Course Name](link)** by [Instructor]
  - Platform: YouTube/Udemy/Coursera
  - Duration: X hours
  - Free/Paid: [Price if paid]
  - Rating: ⭐⭐⭐⭐⭐ (if available)

### Books
- **[Book Title](link)** by Author - [Why it's recommended]

### Blog Posts & Articles
- ⭐ **[Article Title](link)** - [What makes it valuable]
- **[Deep Dive Series](link)** - [Description]

### Interactive Resources
- **[Interactive Platform](link)** - Hands-on exercises
- **[Code Playground](link)** - Experiment in browser

### Community Resources
- 📖 [Official Forum/Discord](link)
- 💬 [Reddit Community](link)
- 🐦 [Key People to Follow on Twitter](links)
- 📺 [YouTube Channels](links)

## Practical Projects

### Project 1: [Simple Project Name]
**Level**: Beginner
**Time**: 2-4 hours
**Goal**: [What you'll learn]

**Description**: [What you'll build]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Skills Practiced**:
- Skill 1
- Skill 2

**Resources**:
- [Starter template if available]
- [Reference implementation]

---

### Project 2: [Intermediate Project]
**Level**: Intermediate
**Time**: 8-12 hours

[Continue pattern...]

---

### Project 3: [Advanced Project]
**Level**: Advanced
**Time**: 20+ hours

[Comprehensive project]

## Common Pitfalls & How to Avoid Them

### Pitfall 1: [Common mistake]
**Why it happens**: [Explanation]
**How to avoid**: [Solution]
**Resources**: [Link to deeper explanation]

### Pitfall 2: [Another mistake]
[Continue pattern...]

## Learning Tips

### Effective Study Strategies
1. **[Strategy 1]**: [Why it works for this technology]
2. **[Strategy 2]**: [Specific advice]
3. **Build, don't just read**: [Importance of hands-on practice]

### How to Practice Effectively
- [Specific practice techniques]
- [Spaced repetition for concepts]
- [Building progressive projects]

### Debugging & Problem-Solving
- [Where to get help]
- [How to debug effectively]
- [Common error messages and solutions]

## Assessment Checkpoints

### After Phase 1
Can you:
- [ ] Explain [core concept] to a beginner?
- [ ] Build [simple thing] from scratch?
- [ ] Debug [common error]?
- [ ] Choose between [option A] and [option B]?

### After Phase 2
[Intermediate checkpoints]

### Final Mastery Check
[Comprehensive assessment]

## What's Next?

### Related Technologies to Learn
1. **[Related Tech 1]**: Why it pairs well, when to learn it
2. **[Related Tech 2]**: How it complements this knowledge

### Advanced Topics (Beyond This Guide)
- [Advanced topic 1]
- [Advanced topic 2]

### Staying Current
- [How to keep up with updates]
- [Key sources for news/releases]
- [Community events/conferences]

### Contribution Opportunities
- [How to contribute to open source projects]
- [How to help the community]

## Quick Reference

### Essential Commands/Patterns
```
[Most commonly used code patterns]
```

### Cheat Sheet
[Link to cheat sheet or inline quick reference]

### Troubleshooting Guide
Common issues and solutions

---

**Last Updated**: [Date]
**Estimated Time to Complete**: [Total time estimate]
**Difficulty**: [Overall difficulty rating]

## Feedback & Updates
This is a living document. If you find broken links, outdated information, or have suggestions for improvement, please [how to provide feedback].
```

## Workflow

### Step 1: Understand the Topic

Ask clarifying questions if needed:
- "What's your current knowledge level with this technology?"
- "What's your learning goal? (e.g., build a project, pass certification, job requirement)"
- "How much time can you dedicate? (hours per week)"
- "Any specific areas you want to focus on?"

If the user just completed `break-down`, reference the prerequisite tree to inform the learning path.

### Step 2: Research the Technology

Use WebSearch to gather information about:

**Overview & Context**:
- Official documentation and getting started guides
- Wikipedia or authoritative explanations
- Recent blog posts about the technology
- Use cases and real-world applications

**Learning Resources** (search for):
- "best [technology] tutorials 2026"
- "[technology] getting started guide"
- "[technology] crash course"
- "learn [technology] step by step"
- "[technology] project ideas"
- "[technology] vs alternatives"

**Quality Indicators**:
- GitHub stars (for code examples/repos)
- Upvotes on sites like Medium, Dev.to, Reddit
- Course ratings on platforms like Udemy, Coursera
- Official endorsements or recommendations
- Recency (prefer 2024-2026 content for modern tech)

**Community Resources**:
- Official Discord/Slack communities
- Subreddits
- Stack Overflow tags
- YouTube channels dedicated to the topic

### Step 3: Structure the Learning Path

**Progression Principle**: Each phase should build on the previous one.

**Phase Design**:
1. **Foundations** (20-30% of time)
   - Core concepts and terminology
   - Mental models
   - "Hello World" equivalent
   - Basic operations

2. **Intermediate** (30-40% of time)
   - Common patterns and best practices
   - Integration with other tools
   - Real-world scenarios
   - Debugging basics

3. **Advanced** (20-30% of time)
   - Performance optimization
   - Advanced patterns
   - Edge cases
   - Architecture decisions

4. **Mastery** (10-20% of time)
   - Production considerations
   - Building complete projects
   - Contributing to ecosystem

**Time Allocation**:
- If user specified time commitment: divide phases appropriately
- Default: assume 6-8 weeks of part-time study (5-10 hours/week)
- Be realistic about time estimates

### Step 4: Curate Resources

**Quality Over Quantity**: Better to have 5 excellent resources than 20 mediocre ones.

**Resource Selection Criteria**:
- ✅ Clear explanations for the target level
- ✅ Hands-on/interactive when possible
- ✅ Recent (last 1-2 years for fast-moving tech)
- ✅ Free or reasonably priced
- ✅ Positive community feedback
- ✅ Progressive difficulty
- ⚠️ Avoid resources that assume too much prior knowledge
- ⚠️ Skip outdated content (check dates)

**Diversity of Formats**:
- Mix video, text, and interactive resources
- Some people learn better from videos, others from reading
- Interactive platforms (like CodeSandbox, Repl.it) for practice

**Mark the Best**: Use ⭐ to highlight the absolutely must-see resources

### Step 5: Design Practical Exercises

**Project Progression**:

1. **Starter Project** (Phase 1)
   - Very simple, ~2-4 hours
   - Uses only fundamental concepts
   - Clear success criteria
   - Example: "Build a simple counter app" (for React)

2. **Intermediate Project** (Phase 2)
   - Combines multiple concepts
   - 8-12 hours
   - More realistic use case
   - Example: "Build a todo app with persistence" (for React)

3. **Advanced Project** (Phase 3-4)
   - Production-ready complexity
   - 20+ hours
   - Demonstrates mastery
   - Example: "Build a real-time chat application" (for React + WebSockets)

**Project Guidelines**:
- Provide clear objectives
- List what concepts each project reinforces
- Link to starter templates or reference implementations
- Suggest extensions for further learning

### Step 6: Add Learning Enhancements

**Prerequisites Section**:
- Link to knowledge base nodes if they exist
- Provide external resources for prerequisites
- Be realistic about what's truly required vs. nice-to-have

**Common Pitfalls**:
- Research what beginners typically struggle with
- Search for "[technology] common mistakes" or "[technology] gotchas"
- Include solutions and workarounds

**Assessment Checkpoints**:
- Self-check questions for each phase
- Skills checklist
- "You should be able to..." statements

**Related Topics**:
- What to learn next
- Complementary technologies
- How this fits into broader ecosystem

### Step 7: Search for Quality Resources

Use WebSearch strategically:

```
# For official docs
"[technology] official documentation"
"[technology] getting started"

# For tutorials
"best [technology] tutorial 2026"
"[technology] crash course"
"learn [technology] from scratch"

# For videos
"[technology] youtube tutorial"
"[technology] course udemy/coursera"

# For community
"[technology] reddit"
"[technology] discord community"

# For projects
"[technology] project ideas"
"[technology] example projects github"

# For comparisons
"[technology] vs [alternative]"
"when to use [technology]"
```

**Verify Quality**:
- Check publication dates
- Look for engagement metrics (views, stars, upvotes)
- Prefer official sources or well-known authors
- Test a few links to ensure they're still active

### Step 8: Format and Save

**File Naming**:
- Primary: `LEARNING_PATH.md`
- Alternative: `[Technology]-Study-Guide.md`
- Save to the topic's directory in the knowledge base

**Final Touches**:
- Add table of contents if the guide is long (>500 lines)
- Include estimated completion time
- Add "Last Updated" date
- Provide feedback mechanism

**Cross-Reference**:
- If this follows a `break-down` or `supplement-node` operation, mention the knowledge tree structure
- Link back to related nodes in the knowledge base

## Writing Style Guidelines

### Tone
- **Encouraging**: Learning new tech is challenging; be supportive
- **Practical**: Focus on actionable advice, not abstract theory
- **Realistic**: Don't sugarcoat difficulty; be honest about time investment
- **Specific**: Use concrete examples, not vague descriptions

### Structure
- Use progressive disclosure: simple → complex
- Each section should flow naturally to the next
- Include visual breaks (emojis, headers) for scannability
- Keep paragraphs short (3-5 sentences max)

### Examples
- Always include concrete examples
- Code snippets should be runnable
- Explain "why" not just "what"

## Special Considerations

### For Rapidly Changing Technologies
- Focus more on fundamentals that won't change
- Mention version-specific content explicitly
- Provide strategies for staying current

### For Complex Technologies
- Break down into smaller sub-paths if needed
- May require 12+ weeks instead of 6-8
- Include more checkpoints

### For Niche Technologies
- May have fewer resources; quality over quantity even more important
- Include how to get help (community is critical)
- Explain the niche and why it exists

### Integration with Knowledge Base
- If the topic exists in TREE.md, reference its position
- Link to parent concepts
- Suggest related sibling topics to explore

## Example Interaction

**User**: "I just added Kubernetes to my knowledge tree. Create a learning path for it. I know Docker and basic Linux."

**You respond**:
1. Acknowledge existing knowledge: "Great! Your Docker knowledge will help a lot—Kubernetes builds on containerization concepts."
2. Research Kubernetes resources (WebSearch)
3. Create `LEARNING_PATH.md` in the Kubernetes node directory
4. Structure 8-week plan:
   - Phase 1: K8s fundamentals (Pods, Services, Deployments)
   - Phase 2: Configuration (ConfigMaps, Secrets, Volumes)
   - Phase 3: Advanced (StatefulSets, DaemonSets, Operators)
   - Phase 4: Production (Monitoring, Security, Best Practices)
5. Include curated resources from official K8s docs, CNCF, popular tutorials
6. Design projects: Deploy simple app → Multi-tier app → Full microservices architecture
7. Add common pitfalls: Networking confusion, YAML syntax, resource limits

## Quality Checklist

Before finalizing, ensure:

- [ ] Overview clearly explains what the technology is
- [ ] Use cases are concrete and relatable
- [ ] Prerequisites are realistic
- [ ] Learning phases progress logically
- [ ] At least 3-5 quality resources per phase
- [ ] Resources are recent (last 1-2 years)
- [ ] Mix of free and paid resources noted
- [ ] At least 3 practical projects included
- [ ] Projects increase in complexity
- [ ] Common pitfalls section is helpful
- [ ] Assessment checkpoints are clear
- [ ] Next steps point to related topics
- [ ] All links are working (spot-check a few)
- [ ] Time estimates are realistic
- [ ] Markdown formatting is clean

## Tips for Success

1. **Start with "Why"**: People learn better when motivated. Explain real-world value upfront.

2. **Connect to Existing Knowledge**: Reference what the user already knows. Learning is about building on foundations.

3. **Balance Theory and Practice**: Don't just list resources—explain the learning strategy.

4. **Be Honest About Difficulty**: Some technologies are genuinely hard. Acknowledge this and provide extra support.

5. **Curate Ruthlessly**: 5 excellent resources beat 20 mediocre ones. Quality matters.

6. **Test the Path**: If possible, spot-check a few resources to ensure they're actually good.

7. **Update Over Time**: Technologies evolve. Mention this is a living document.

8. **Provide Escape Hatches**: Include "if you're stuck" sections with where to get help.

---

This skill creates comprehensive, actionable learning guides that take users from novice to proficient in a structured, supportive way.
