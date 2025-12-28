# Reflexion Agent - Learning from Failures

A LangGraph-powered agent that learns from past failures using episodic memory and external validation.

## 🎯 What's Inside

- **`state.py`**: State definition with episodic memory
- **`memory.py`**: Persistent memory manager
- **`validators.py`**: External validation (code tests)
- **`chains.py`**: Generation & reflection with memory
- **`graph.py`**: LangGraph workflow with learning
- **`main.py`**: Interactive CLI
- **`examples.py`**: Cross-task learning demos

## 🚀 Quick Start

```bash
cd 05-reflexion-agent
python main.py
```

**Example Session**:
```
Task 1: "Write a function to reverse a string"
Attempt 1: FAIL (no empty check)
Lesson: "Always check for empty input"

Attempt 2: SUCCESS!

---

Task 2: "Write a function to check palindrome"
Attempt 1: SUCCESS! (Applied lesson from Task 1!)
```

## 🔑 Key Difference from Module 04

| Feature | Module 04 (Reflection) | Module 05 (Reflexion) |
|---------|------------------------|----------------------|
| **Memory** | ❌ None | ✅ Episodic |
| **Learning** | ❌ No | ✅ Yes |
| **Validation** | Self-critique | External tests |
| **Use Case** | Content creation | Problem-solving |

## 🏗️ Architecture

```
Generate (using past lessons)
  ↓
Validate (run tests)
  ↓
Success? → Yes → Store success pattern → END
  ↓ No
Reflect → Store lesson in memory
  ↓
Attempts left? → Yes → Generate (with new lesson)
  ↓ No
END
```

## 💡 Key Features

### 1. Episodic Memory
- Stores lessons from failures
- Persists across sessions
- Retrieves relevant lessons

### 2. External Validation
- Runs actual code tests
- Objective success criteria
- Error analysis

### 3. Cross-Task Learning
- Applies lessons to new tasks
- Improves over time
- Pattern recognition

## 📊 Commands

```bash
# Run interactive CLI
python main.py

# Run learning demo
python examples.py

# Test components
python memory.py      # Test memory
python validators.py  # Test validators
python chains.py      # Test chains
python graph.py       # Show graph structure
```

## 🎓 Learning Outcomes

- ✅ Episodic memory management
- ✅ External validation strategies
- ✅ Cross-task learning
- ✅ Memory persistence
- ✅ Advanced LangGraph patterns
- ✅ Success pattern recognition

## 🔧 Customization

### Add Custom Validators

```python
# In validators.py
def validate_custom(solution, criteria):
    # Your validation logic
    return {"success": bool, "error": str}
```

### Modify Memory Retrieval

```python
# In memory.py
def get_relevant_lessons(self, task):
    # Use embeddings for semantic search
    # Current: returns recent lessons
```

## 📚 Next Steps

After mastering this module:
1. Add semantic similarity for lesson retrieval
2. Implement multi-agent reflexion
3. Add human-in-the-loop validation
4. Create domain-specific validators

---

**🎉 You've learned advanced LangGraph with episodic memory!**
