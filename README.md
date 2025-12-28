# LangChain Learning Journey

A structured collection of LangChain implementations and learnings, organized by topic.

## 📁 Project Structure

```
langchain-course/
├── 01-rag-basics/              # RAG implementation
│   ├── main.py                 # Query system
│   ├── ingestion.py            # Document processing
│   ├── mediumblog1.txt         # Sample document
│   └── README.md
│
├── 02-agents-and-tools/        # AI agents with ReAct
│   ├── callbacks.py            # Debug handlers
│   ├── main_with_agent_executor.py
│   ├── demo_tool_description.py
│   └── README.md
│
├── 03-documentation-helper/    # Advanced RAG with web crawling
│   ├── app.py                  # Streamlit web interface
│   ├── crawler.py              # Tavily web scraping
│   ├── ingestion.py            # Enhanced document processing
│   ├── memory.py               # Conversational memory
│   ├── main.py                 # CLI query engine
│   └── README.md
│
├── 04-reflection-agent/        # LangGraph self-improving agent
│   ├── state.py                # State definition
│   ├── chains.py               # Generation & reflection prompts
│   ├── graph.py                # LangGraph workflow
│   ├── main.py                 # Interactive CLI
│   ├── examples.py             # Demo use cases
│   └── README.md
│
├── 05-reflexion-agent/         # Advanced learning agent
│   ├── state.py                # State with episodic memory
│   ├── memory.py               # Memory manager
│   ├── validators.py           # External validation
│   ├── chains.py               # Generation with memory
│   ├── graph.py                # Learning workflow
│   ├── main.py                 # Multi-task CLI
│   ├── examples.py             # Cross-task learning demos
│   └── README.md
│
├── docs/                       # Comprehensive documentation
│   ├── RAG_IMPLEMENTATION_EXPLAINED.md
│   ├── DOCUMENTATION_HELPER_EXPLAINED.md
│   └── REFLECTION_PATTERN_EXPLAINED.md
│   ├── FUNCTION_CALLING_EXPLAINED.md
│   ├── FUNCTION_CALLING_VS_REACT.md
│   ├── CREATE_TOOL_CALLING_AGENT_EXPLAINED.md
│   ├── AGENT_EXECUTOR_EXPLAINED.md
│   ├── COMPARISON.md
│   ├── COHERE_SETUP.md
│   ├── DOCUMENTATION_HELPER_EXPLAINED.md
│   └── GITHUB_UPLOAD_GUIDE.md
│
├── .env                        # API keys (not committed)
├── .gitignore                  # Git ignore rules
├── pyproject.toml              # Dependencies (uv)
├── uv.lock                     # Lock file
└── README.md                   # This file
```

## 🎯 Learning Modules

### [01 - RAG Basics](./01-rag-basics/)
Learn Retrieval-Augmented Generation from scratch:
- ✅ Document loading and chunking
- ✅ Vector embeddings with Cohere
- ✅ Pinecone vector database
- ✅ Semantic search
- ✅ Answer generation with Gemini

**Time**: ~1-2 hours  
**Difficulty**: Beginner

### [02 - Agents and Tools](./02-agents-and-tools/)
Build AI agents using the ReAct pattern:
- ✅ Manual agent loops
- ✅ Function calling
- ✅ Tool descriptions
- ✅ AgentExecutor
- ✅ Debugging with callbacks

**Time**: ~1-2 hours  
**Difficulty**: Intermediate

### [03 - Documentation Helper](./03-documentation-helper/)
Advanced RAG system with web crawling and memory:
- ✅ Web crawling with Tavily
- ✅ Conversational memory
- ✅ Streamlit chat interface
- ✅ Source attribution
- ✅ Recursive text splitting
- ✅ Coreference resolution

**Time**: ~2-3 hours  
**Difficulty**: Intermediate-Advanced

### [04 - Reflection Agent](./04-reflection-agent/)
Learn LangGraph through a self-improving content generator:
- ✅ LangGraph state management
- ✅ Iterative loops and cycles
- ✅ Conditional branching
- ✅ Generate-reflect-refine pattern
- ✅ Quality improvement through feedback

**Time**: ~2-3 hours  
**Difficulty**: Intermediate-Advanced

### [05 - Reflexion Agent](./05-reflexion-agent/)
Advanced LangGraph agent with episodic memory and learning:
- ✅ Episodic memory management
- ✅ External validation with tests
- ✅ Cross-task learning
- ✅ Memory persistence
- ✅ Success pattern recognition
- ✅ Learning from failures

**Time**: ~3-4 hours  
**Difficulty**: Advanced

### Coming Soon...
- 06 - Multi-Agent Systems
- 07 - Advanced RAG (Re-ranking, Hybrid Search)
- 08 - Production Deployment

## � Quick Start

### 1. Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_key
COHERE_API_KEY=your_cohere_key
PINECONE_API_KEY=your_pinecone_key
INDEX_NAME=your_index_name
TAVILY_API_KEY=your_tavily_key  # For Module 03
```

### 3. Get Free API Keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **Cohere**: https://dashboard.cohere.com/
- **Pinecone**: https://www.pinecone.io/
- **Tavily**: https://tavily.com/ (for Module 03)

### 4. Start Learning!
```bash
# Module 1: RAG
cd 01-rag-basics
python ingestion.py  # One-time setup
python main.py       # Query the system

# Module 2: Agents
cd ../02-agents-and-tools
python demo_tool_description.py

# Module 3: Documentation Helper
cd ../03-documentation-helper
python ingestion.py      # Crawl and ingest docs
streamlit run app.py     # Launch web interface

# Module 4: Reflection Agent
cd ../04-reflection-agent
python main.py           # Interactive CLI
python examples.py       # Run demo use cases

# Module 5: Reflexion Agent
cd ../05-reflexion-agent
python main.py           # Multi-task learning CLI
python examples.py       # Cross-task learning demo
```

## 🏗️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **Framework** | LangChain | Industry standard for LLM apps |
| **LLM** | Gemini 2.5 Flash Lite | Free tier, fast, capable |
| **Embeddings** | Cohere v3.0 | Free tier, 1024-d vectors |
| **Vector DB** | Pinecone | Managed, scalable, easy |
| **Package Manager** | uv | 10-100x faster than pip |

## 📚 Documentation

All detailed explanations are in the `/docs` folder:

### RAG Deep Dives
- **RAG_IMPLEMENTATION_EXPLAINED.md**: Complete RAG walkthrough
- **DOCUMENTATION_HELPER_EXPLAINED.md**: Advanced RAG with web crawling
- **COHERE_SETUP.md**: Getting Cohere API key

### Agent Deep Dives
- **FUNCTION_CALLING_EXPLAINED.md**: What is function calling?
- **FUNCTION_CALLING_VS_REACT.md**: Function calling vs ReAct
- **CREATE_TOOL_CALLING_AGENT_EXPLAINED.md**: Agent creation
- **AGENT_EXECUTOR_EXPLAINED.md**: AgentExecutor features
- **COMPARISON.md**: Manual vs automated agents

### Guides
- **GITHUB_UPLOAD_GUIDE.md**: How to push to GitHub

## 🎓 Learning Path

**Recommended order**:

1. **Start with RAG** (`01-rag-basics/`)
   - Understand embeddings and vector search
   - See how retrieval works
   - Build your first RAG system

2. **Then Agents** (`02-agents-and-tools/`)
   - Learn the ReAct pattern
   - Understand function calling
   - Compare manual vs automated approaches

3. **Read Documentation** (`docs/`)
   - Deep dive into concepts
   - Understand trade-offs
   - Learn best practices

4. **Experiment**
   - Modify chunk sizes
   - Add new tools
   - Try different models
   - Build your own projects

## 🔧 Customization

### Use Different Models

**LLM**:
```python
# Gemini Pro (more capable)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Claude
llm = ChatAnthropic(model="claude-3-sonnet")
```

**Embeddings**:
```python
# OpenAI
embeddings = OpenAIEmbeddings()

# Multilingual Cohere
embeddings = CohereEmbeddings(model="embed-multilingual-v3.0")
```

### Add Your Own Documents

Replace `mediumblog1.txt` with your own:
```python
loader = TextLoader("your_document.txt")
# Or use other loaders:
# PDFLoader, CSVLoader, WebBaseLoader, etc.
```

## 📊 What You'll Build

By completing all modules, you'll have:
- ✅ Working RAG system
- ✅ Custom AI agents
- ✅ Understanding of LangChain patterns
- ✅ Production-ready code examples
- ✅ Comprehensive documentation

## 🐛 Troubleshooting

### API Quota Issues
- Gemini: Free tier resets daily
- Cohere: 100 calls/min free
- Pinecone: 1 index free

### Dimension Mismatch
Ensure embeddings match Pinecone index:
- Cohere `embed-english-v3.0`: 1024 dimensions
- Set Pinecone index to 1024 dimensions

### Import Errors
```bash
# Reinstall dependencies
uv sync

# Or
pip install -r requirements.txt
```

## 🤝 Contributing

Feel free to:
- Add new modules
- Improve documentation
- Fix bugs
- Share your learnings

## 📄 License

MIT

## 🙏 Acknowledgments

- LangChain team for the amazing framework
- Google for Gemini
- Cohere for embeddings
- Pinecone for vector database

---

**Happy Learning! 🚀**

*This is a living repository - new modules and improvements added regularly*
