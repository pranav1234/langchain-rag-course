# Agents and Tools

This module demonstrates AI agents using the ReAct pattern (Reason-Act-Observe) with LangChain.

## 📚 What's Inside

- **`callbacks.py`**: Custom callback handlers for debugging
- **`main_with_agent_executor.py`**: Conceptual comparison of manual vs AgentExecutor
- **`demo_tool_description.py`**: How LLMs see tool descriptions

## 🎯 What You'll Learn

1. Manual agent loop implementation (ReAct pattern)
2. Function calling / Tool calling
3. AgentExecutor abstraction
4. Tool descriptions and docstrings
5. Callback handlers for debugging

## 🔑 Key Concepts

### ReAct Pattern
```
Reason → Act → Observe → Repeat
```

**Example**:
```
User: "What is the length of the word DOG?"

Reason: I need to count characters
Act: Call get_text_length("DOG")
Observe: Result is 3
Reason: I have the answer
Final: The length is 3
```

### Function Calling
- LLM requests tool execution
- Your code runs the tool
- LLM uses result to answer

### Manual Loop vs AgentExecutor

| Manual Loop | AgentExecutor |
|-------------|---------------|
| Full control | Automated |
| Educational | Production-ready |
| ~70 lines | ~30 lines |
| Manual error handling | Built-in safeguards |

## 📝 Files Explained

### callbacks.py
Custom callback handler for debugging:
```python
class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, prompts, **kwargs):
        print(f"***Prompt to LLM:***\n{prompts[0]}")
    
    def on_llm_end(self, response, **kwargs):
        print(f"***LLM Response:***\n{response}")
```

### main_with_agent_executor.py
Compares two approaches:
1. Manual `while True:` loop
2. AgentExecutor abstraction

### demo_tool_description.py
Shows what the LLM sees about your tools:
- Tool name
- Tool description (docstring!)
- Parameters

## 🎓 Learning Path

1. **Start here**: Understand manual agent loop
2. **Then**: Learn AgentExecutor
3. **Finally**: Build production agents

## 🔗 Related Documentation

See `/docs` folder for:
- `FUNCTION_CALLING_EXPLAINED.md`
- `FUNCTION_CALLING_VS_REACT.md`
- `CREATE_TOOL_CALLING_AGENT_EXPLAINED.md`
- `AGENT_EXECUTOR_EXPLAINED.md`
- `COMPARISON.md`

## 📚 Next Steps

After this module:
1. Add more complex tools
2. Implement multi-step reasoning
3. Add error recovery
4. Build conversational agents
