# Reflection Agent - Self-Improving Content Generator

A LangGraph-powered agent that improves content quality through iterative reflection and refinement.

## 📚 What's Inside

- **`state.py`**: State definition for the workflow
- **`chains.py`**: Generation and reflection prompt chains
- **`graph.py`**: LangGraph workflow with conditional looping
- **`main.py`**: Interactive CLI interface
- **`examples.py`**: Demonstration use cases

## 🎯 What You'll Learn

1. **LangGraph State Management** - Shared state across nodes
2. **Iterative Loops** - Cycles and conditional branching
3. **Generate-Reflect-Refine Pattern** - Self-improvement workflow
4. **Conditional Edges** - Decision-based routing
5. **TypedDict** - Type-safe state definitions

## 🚀 Quick Start

### 1. Run the Interactive CLI

```bash
cd 04-reflection-agent
python main.py
```

**Example Session**:
```
📝 Enter your content request:
> Make this tweet better: LangChain is cool

🔢 Max iterations (default 3): 3

=== ITERATION 1 ===
📝 Generating initial content...
Draft: 🚀 LangChain is revolutionizing LLM development...

🤔 Reflecting on content...
Reflection: Good start, but could be more specific about features...

=== ITERATION 2 ===
✨ Refining based on feedback...
Draft: 🚀 LangChain simplifies building LLM apps with chains, agents...

🤔 Reflecting on content...
Reflection: Much better! Consider adding a call-to-action...

=== ITERATION 3 ===
✨ Refining based on feedback...
Draft: 🚀 LangChain simplifies building LLM apps with chains, agents, 
and memory. Try it today: pip install langchain 🦜🔗

✅ FINAL POLISHED CONTENT
```

### 2. Run Example Use Cases

```bash
python examples.py
```

This runs 4 different examples:
- Tweet improvement
- Professional email writing
- Code documentation
- Blog post introduction

### 3. Test Individual Components

```bash
# Test chains
python chains.py

# Test graph structure
python graph.py
```

## 🏗️ Architecture

### The Reflection Loop

```
Start
  ↓
Generate Initial Content (iteration=1)
  ↓
Reflect on Quality
  ↓
iteration < max? → Yes → Refine Based on Feedback (iteration=2)
                           ↓
                         Reflect on Quality
                           ↓
                         iteration < max? → Yes → Refine (iteration=3)
                                                     ↓
                                                   Reflect
                                                     ↓
                                                   iteration >= max? → No
                                                     ↓
                                                   END (Return Final Draft)
```

### State Flow

```python
{
    "input": "Make this tweet better: LangChain is cool",
    "draft": "",           # Updated by generate_node
    "reflection": "",      # Updated by reflect_node
    "iteration": 0,        # Incremented each loop
    "max_iterations": 3    # Stop condition
}
```

## 🔧 Components Deep Dive

### 1. State (`state.py`)

```python
class ReflectionState(TypedDict):
    input: str              # Original request
    draft: str              # Current version
    reflection: str         # Critique
    iteration: int          # Current iteration
    max_iterations: int     # Max iterations
```

**Why TypedDict?**
- Type safety
- IDE autocomplete
- Clear documentation
- Runtime validation

### 2. Chains (`chains.py`)

**Three Prompt Chains**:

1. **Generation Chain**: Creates initial content
   ```python
   generation_chain = GENERATION_PROMPT | llm
   ```

2. **Refinement Chain**: Improves based on feedback
   ```python
   refinement_chain = REFINEMENT_PROMPT | llm
   ```

3. **Reflection Chain**: Provides critique
   ```python
   reflection_chain = REFLECTION_PROMPT | llm
   ```

**Key Insight**: Separate chains for different tasks = better prompts!

### 3. Graph (`graph.py`)

**Two Nodes**:

1. **generate_node**: Creates or refines content
   - First iteration: Uses generation chain
   - Later iterations: Uses refinement chain

2. **reflect_node**: Critiques current draft
   - Evaluates clarity, impact, tone, structure
   - Provides specific, actionable feedback

**Edges**:

1. **Normal Edge**: `generate → reflect` (always)
2. **Conditional Edge**: `reflect → generate` or `END`
   - Decision based on iteration count

**Decision Function**:
```python
def should_continue(state):
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    else:
        return "continue"  # Loop back!
```

## 📊 Comparison with Previous Modules

| Feature | Module 01 (RAG) | Module 03 (Doc Helper) | Module 04 (Reflection) |
|---------|-----------------|------------------------|------------------------|
| **Pattern** | Retrieval → Generate | Retrieve → Generate | Generate → Reflect → Refine |
| **Loops** | None | None | ✅ Yes |
| **State** | None | Session state | ✅ LangGraph state |
| **Iterations** | 1 | 1 | Multiple (3-10) |
| **Self-improvement** | No | No | ✅ Yes |
| **Framework** | LangChain | LangChain | **LangGraph** |

## 🎓 Key Concepts

### 1. Generate-Reflect-Refine Pattern

**Why it works**:
- LLMs are better at critiquing than creating
- Iteration improves quality
- Specific feedback > vague prompts

**Example**:
```
Iteration 1: "LangChain is cool" → Generic
Iteration 2: "LangChain simplifies LLM development" → Better
Iteration 3: "LangChain simplifies LLM apps with chains, agents, memory" → Specific!
```

### 2. Conditional Looping

**Traditional Chain** (LangChain):
```python
A → B → C → Done
```

**LangGraph Loop**:
```python
A → B → Check → (if not done) → A
         ↓
       (if done)
         ↓
        Done
```

### 3. State Management

**State is shared** across all nodes:
```python
# generate_node modifies draft
state["draft"] = new_content

# reflect_node reads draft, adds reflection
state["reflection"] = critique

# Next iteration: generate_node uses reflection
refined = refine(state["draft"], state["reflection"])
```

## 🛠️ Customization

### Change Max Iterations

```python
# In main.py
final_state = run_reflection_agent(
    user_input,
    max_iterations=5  # More iterations = better quality (but slower)
)
```

### Modify Reflection Criteria

```python
# In chains.py, update REFLECTION_PROMPT
"""Evaluate based on:
1. Clarity
2. Impact
3. Tone
4. Structure
5. Completeness
6. SEO optimization  # ← Add your own!
7. Brand voice
"""
```

### Use Different LLM

```python
# In chains.py
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.7)
```

### Add Quality Threshold

```python
# In graph.py
def should_continue(state):
    # Stop if quality is good enough
    if "excellent" in state["reflection"].lower():
        return "end"
    elif state["iteration"] >= state["max_iterations"]:
        return "end"
    else:
        return "continue"
```

## 🐛 Troubleshooting

### Issue: Too Many Iterations

**Problem**: Agent keeps refining unnecessarily

**Solution**: Lower max_iterations or add quality threshold

### Issue: Poor Quality Output

**Problem**: Final output not much better than initial

**Solutions**:
- Improve reflection prompt (be more specific)
- Increase temperature for more creativity
- Add few-shot examples to prompts

### Issue: Slow Performance

**Problem**: Takes too long to complete

**Solutions**:
- Reduce max_iterations
- Use faster LLM (gemini-flash vs gemini-pro)
- Run chains in parallel (advanced)

## 📚 Next Steps

After mastering this module:

1. **Add Quality Scoring**: Numerical scores for each iteration
2. **Multi-Agent Reflection**: Different agents for different aspects
3. **Human-in-the-Loop**: Pause for human feedback
4. **Checkpointing**: Save and resume long workflows
5. **Parallel Reflection**: Multiple critics at once

## 🔗 Related Documentation

See `/docs` folder for:
- `REFLECTION_PATTERN_EXPLAINED.md` - Deep dive
- `RAG_IMPLEMENTATION_EXPLAINED.md` - Module 01 basics
- `DOCUMENTATION_HELPER_EXPLAINED.md` - Module 03 advanced RAG

---

**🎉 Congratulations!** You've learned LangGraph through a practical self-improving agent!

**Next Module**: Multi-agent systems and advanced workflows
