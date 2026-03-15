---
name: break-down
description: Analyzes questions or problems to generate a knowledge prerequisite tree showing what you need to learn. Use when users ask "what do I need to know to solve X?" or "how do I implement Y?" or present any problem/question and want to understand the prerequisite knowledge needed. Maps out learning paths from foundational to advanced topics. Helps identify knowledge gaps before tackling complex problems.
---

# Break Down

This skill analyzes questions or problems and generates a structured knowledge prerequisite tree, helping you understand what you need to learn before tackling a challenge.

## How It Works

When you provide a question or problem:

1. **Analyzes the question** to identify all prerequisite knowledge needed
2. **Organizes knowledge by difficulty** (🟢 Foundational → 🟡 Intermediate → 🔴 Advanced)
3. **Asks what you already know** to filter out unnecessary topics (user-in-loop)
4. **Checks existing knowledge tree** to see what you already have vs. gaps
5. **Creates missing nodes** only for knowledge gaps
6. **Presents a learning path** - what to study and in what order

## Workflow

### Step 1: Read the existing tree

Read `TREE.md` from the project root to understand what knowledge already exists in your knowledge base.

### Step 2: Analyze the question/problem

Break down what knowledge is needed:
- What are the core concepts required to understand this problem?
- What prerequisite knowledge is needed for those concepts?
- What algorithms, data structures, or techniques are involved?
- What programming languages or tools are relevant?

Think like a teacher designing a curriculum - work backwards from the problem to identify all the foundational knowledge needed.

### Step 3: Generate knowledge prerequisite tree

Create a hierarchical structure of knowledge needed, organized by **difficulty levels**:

**Organize knowledge into levels**:
- **🟢 Foundational**: Basic concepts most CS students know (data structures, basic algorithms, coordinate systems, etc.)
- **🟡 Intermediate**: Domain-specific knowledge (specific algorithms, frameworks, protocols)
- **🔴 Advanced**: Specialized techniques, optimizations, and applications

**Example question**: "How do I implement a web crawler?"

**Knowledge needed** (organized by level):
- **🟢 Foundational**:
  - Data Structures → Queues, Hash Sets, Graphs
  - Networking → HTTP Protocol basics
- **🟡 Intermediate**:
  - Algorithms → Graph Traversal (BFS/DFS)
  - Python → HTTP Libraries (requests), HTML Parsing (BeautifulSoup)
  - Web Protocols → Robots.txt, DNS
- **🔴 Advanced**:
  - Systems → Concurrency, Rate Limiting, Error Handling
  - Web Scraping → Politeness policies, distributed crawling

### Step 4: User-in-Loop Knowledge Filter ⭐

Choose one of two filtering approaches:

#### **Approach A: Interactive Filtering** (Default)

Ask the user what they already know before creating nodes:

1. **Present the knowledge map** organized by difficulty level (🟢 Foundational → 🟡 Intermediate → 🔴 Advanced)
2. **Ask the user directly**:
   - "Do you already understand [list foundational topics]?"
   - Or give quick filter options:
     - "Skip all foundational topics"
     - "Skip specific topics (tell me which)"
     - "I need everything"
3. **Filter the tree** based on their response
4. **Create only the filtered nodes**

#### **Approach B: Generate-Then-Prune** (User preference)

If the user prefers to manually edit:

1. **Generate the complete tree** with ALL nodes in TREE.md
2. **Tell the user**: "Review TREE.md and delete any nodes for topics you already know"
3. **Wait for user confirmation**: User says "ready" or "done"
4. **Read the pruned TREE.md**
5. **Create directories only for remaining nodes**

**Why this is better**: Gives user full control, easier to see the complete picture, can delete entire branches at once.

This prevents adding basic topics like "Coordinate Systems" when the user is asking about advanced 3D rendering techniques.

### Step 5: Map against existing tree

Compare the needed knowledge with what already exists in TREE.md:
- ✅ Nodes that already exist
- ⚠️ Nodes that need to be created
- 🔗 Nodes where existing content should be cross-linked

### Step 6: Create missing nodes level by level

For each missing knowledge node **that the user needs to learn** (after filtering), add it to the tree:
- Build complete paths (add parent nodes if missing)
- Include short descriptions (max 10 words) for each node
- Maintain alphabetical ordering
- Use proper indentation (2 spaces per level)
- Keep names clear and consistent
- **Skip topics the user already knows** (from Step 4 filter)

**Format**: `- Node Name - Short description (max 10 words)`

### Step 7: Create directory structure and list-based files

**If using Approach A (Interactive)**: Create directories immediately after filtering.

**If using Approach B (Generate-Then-Prune)**:
1. Wait for user to finish editing TREE.md
2. Read the modified TREE.md
3. Create directories only for nodes that remain

**For nodes with inline lists** (e.g., `3D File Formats [FBX, GLTF, OBJ]`):
- Create the directory for the parent node
- Create a markdown file describing each list element

Example for "3D File Formats [FBX, GLTF, OBJ, PLY, STL, USD]":
```bash
mkdir -p "Computer-Science/Computer-Graphics/3D-File-Formats"
```

Then create `3D-File-Formats/overview.md`:
```markdown
# 3D File Formats

## FBX (Filmbox)
- Autodesk proprietary format
- Used for: Animation, rigging, models
[description...]

## GLTF (GL Transmission Format)
- Open standard by Khronos
- Used for: Web 3D, real-time rendering
[description...]

## OBJ (Wavefront)
- Simple, widely supported
- Used for: Static meshes
[description...]
```

Don't create separate directories for list elements (no `FBX/`, `GLTF/` directories).

### Step 8: Present the learning path

Show the user:

**Knowledge Map for: [their question]**

**Existing Knowledge** (what you already have in your tree):
- List of nodes that already exist with file paths

**Knowledge Gaps** (what you need to learn):
- List of new nodes created, organized by priority/prerequisites

**Suggested Learning Order**:
1. Start with foundational concepts (lowest in the tree)
2. Build up to intermediate concepts
3. End with advanced/specific concepts needed for the question

**Next Steps**:
- Suggest which topics to learn first
- Point to any existing content that's relevant
- Note where they can add content as they learn (using `/supplement-node`)

## Examples

**Example 1: Question with user filtering**

Input: "How do I implement LRU cache?"

Process:
1. Read TREE.md
2. Analyze question: Need to understand LRU caching, data structures, and implementation
3. Generate knowledge tree with levels:
   - **🟢 Foundational**: Hash Maps, Doubly Linked Lists
   - **🟡 Intermediate**: Cache Replacement Policies, LRU Algorithm
   - **🔴 Advanced**: Thread-safe LRU, Distributed caching
4. **Ask user**: "I identified these areas. Do you already know: Hash Maps and Doubly Linked Lists?"
5. User: "Yes, I know those basic data structures"
6. **Filter**: Remove foundational topics, keep only Intermediate and Advanced
7. Add to tree: Cache Replacement Policies → LRU (skip Hash Maps/Linked Lists)
8. Show: "✅ Skipped: Hash Maps, Doubly Linked Lists (you know these). ✨ Created: Cache Replacement Policies → LRU → Thread-safe LRU. Start with the LRU algorithm theory, assuming you understand how to combine hash maps with doubly linked lists for O(1) operations."

**Example 2: Complex problem requiring multiple areas**

Input: "I want to build a real-time chat application. What do I need to know?"

Process:
1. Read TREE.md
2. Analyze: This requires networking, databases, frontend, backend, real-time communication
3. Generate comprehensive knowledge tree:
   - **🟢 Foundational**: HTTP, JavaScript basics
   - **🟡 Intermediate**:
     - Networking → WebSockets → Real-time Communication
     - Networking → REST APIs
     - Databases → NoSQL → Message Storage
     - Programming Languages → JavaScript → Node.js → Socket.io
     - Programming Languages → JavaScript → Frontend → React
   - **🔴 Advanced**:
     - Systems → Authentication → JWT
     - Systems → Scalability → Load Balancing
4. Ask user about foundational knowledge
5. Filter based on response
6. Create missing nodes
7. Show organized learning path: "Foundation (HTTP, JavaScript) → Backend (Node.js, Databases) → Real-time (WebSockets, Socket.io) → Frontend (React) → Advanced (Auth, Scalability)"

## Important Principles

**Think like a teacher**: Design a curriculum that builds knowledge progressively. Don't just list topics - organize them by prerequisite relationships.

**Nodes are subjects, not properties or lists**: Every node should represent a subject you can study, not a property or section.

**Leaf nodes as list elements**: Distinguish between **fields/categories** (nodes) and **specific instances** (lists).

**Rule of thumb**: If there are many different algorithms/techniques in this field, it's a NODE. If it's one specific thing, it's a LIST ELEMENT.

**REAL NODE** (research fields):
- NeRF (field with many variants: Instant-NGP, Mip-NeRF, TensoRF, etc.)
- Diffusion Models (field with DDPM, Score-based, Latent Diffusion, etc.)
- GANs (broad category with many architectures)
- Multi-view Synthesis (techniques for consistent view generation)

**PROPERTY LIST** (specific instances):
- Specific models: [DreamFusion, Point-E, Shap-E, Magic3D, Fantasia3D]
- Specific formats: [FBX, GLTF, OBJ, PLY, STL, USD]
- Specific tools: [PyTorch, TensorFlow, JAX]
- Specific algorithms: [Dijkstra, A*, Bellman-Ford]

**Bad** (field treated as list item):
```
- Deep Learning [Diffusion Models, GANs]  ❌
```

**Good** (fields as nodes, specific models as lists):
```
- Deep Learning
  - Diffusion Models  ← field/category = NODE
  - GANs  ← field/category = NODE
- Text to 3D Models [DreamFusion, Point-E, Shap-E]  ← specific models = LIST
```

**Key question**: "Are there many research papers/techniques in this area?" → YES = Node, NO = List element

**After creating the tree**: For parent nodes with inline lists, create a single markdown file (e.g., `3d-file-formats.md`) that describes each list element in sections.

**Filter ruthlessly**: Don't assume the user is a beginner. Always ask what they know and skip topics they've mastered.

**Connect to existing knowledge**: When possible, relate new topics to what already exists in their knowledge tree. Build on what they have.

**Provide context**: Explain *why* each topic is needed for solving the original problem. This helps with motivation and understanding the big picture.

## Success Criteria

After using this skill, the user should:
- Understand what knowledge is needed to solve their problem
- See a clear learning path from foundational to advanced
- Know what they already have vs. what's missing
- Have a structured tree ready to fill with content as they learn
- Feel motivated because they can see the route to their goal
