# LangChain RAG Course

A complete implementation of RAG (Retrieval-Augmented Generation) and AI agents using LangChain, Gemini, Cohere, and Pinecone.

## 🎯 What's Inside

### 1. **Agent with Tools** (`main.py` - original)
- Manual ReAct loop implementation
- Custom tool: `get_text_length`
- Gemini LLM with function calling
- Educational comments explaining each step

### 2. **RAG System** 
- **`ingestion.py`**: Document processing pipeline
- **`main.py`**: Query system with retrieval
- Semantic search using Cohere embeddings
- Pinecone vector database
- Gemini for answer generation

## 🚀 Features

- ✅ Manual agent loop (ReAct pattern)
- ✅ RAG implementation from scratch
- ✅ Free-tier compatible (Cohere + Gemini)
- ✅ Production-ready architecture
- ✅ Comprehensive documentation

## 📦 Setup

### 1. Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
PINECONE_API_KEY=your_pinecone_api_key
INDEX_NAME=your_pinecone_index_name
```

### 3. Get API Keys (All Free!)

**Gemini**: https://makersuite.google.com/app/apikey  
**Cohere**: https://dashboard.cohere.com/  
**Pinecone**: https://www.pinecone.io/

## 🏃 Usage

### RAG System

#### Step 1: Ingest Documents (One-time)
```bash
python ingestion.py
```
This will:
- Load `mediumblog1.txt`
- Split into 20 chunks
- Create embeddings with Cohere
- Store in Pinecone

#### Step 2: Query the System
```bash
python main.py
```
Ask questions about your documents!

### Agent with Tools
```bash
python main.py  # (the original agent implementation)
```

## 🏗️ Architecture

### RAG Pipeline
```
Document → Split → Embed (Cohere) → Store (Pinecone)
                                          ↓
Query → Embed → Search → Retrieve → Generate (Gemini)
```

### Components
- **Embeddings**: Cohere `embed-english-v3.0` (1024 dimensions)
- **Vector DB**: Pinecone (cloud-hosted)
- **LLM**: Gemini `gemini-2.5-flash-lite`
- **Framework**: LangChain

## 📚 Documentation

- **`RAG_IMPLEMENTATION_EXPLAINED.md`**: Deep dive into RAG system
- **`FUNCTION_CALLING_EXPLAINED.md`**: What is function calling?
- **`FUNCTION_CALLING_VS_REACT.md`**: Function calling vs ReAct pattern
- **`CREATE_TOOL_CALLING_AGENT_EXPLAINED.md`**: AgentExecutor explained
- **`AGENT_EXECUTOR_EXPLAINED.md`**: What makes AgentExecutor special?
- **`COMPARISON.md`**: Manual loop vs AgentExecutor

## 📁 Project Structure

```
langchain-course/
├── main.py                          # RAG query system
├── ingestion.py                     # Document processing
├── callbacks.py                     # LLM callback handlers
├── mediumblog1.txt                  # Sample document
├── pyproject.toml                   # Dependencies (uv)
├── .env                             # API keys (not committed)
└── docs/
    ├── RAG_IMPLEMENTATION_EXPLAINED.md
    ├── FUNCTION_CALLING_EXPLAINED.md
    └── ...
```

## 🎓 What You'll Learn

1. **RAG Fundamentals**
   - Document chunking strategies
   - Vector embeddings
   - Semantic search
   - Retrieval-augmented generation

2. **AI Agents**
   - ReAct pattern (Reason-Act-Observe)
   - Function calling
   - Tool binding
   - Manual vs automated loops

3. **Production Patterns**
   - LangChain chains
   - AgentExecutor
   - Error handling
   - Prompt engineering

## 🔧 Customization

### Change the Query
Edit `main.py`:
```python
query = "Your question here"
```

### Adjust Retrieval
```python
# Get more chunks
vectorstore.as_retriever(search_kwargs={"k": 10})

# Filter by metadata
vectorstore.as_retriever(
    search_kwargs={"filter": {"source": "specific_file.txt"}}
)
```

### Use Different Models
```python
# Different Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Different embedding model
embeddings = CohereEmbeddings(model="embed-multilingual-v3.0")
```

## 🐛 Troubleshooting

### API Quota Exceeded
- **Gemini**: Wait for daily quota reset
- **Cohere**: Free tier: 100 calls/min
- **Pinecone**: Free tier: 1 index, 100K vectors

### Dimension Mismatch
Ensure embedding model dimensions match Pinecone index:
- Cohere `embed-english-v3.0`: 1024 dimensions
- Pinecone index must also be 1024 dimensions

### NumPy Errors
```bash
pip install numpy --upgrade
```

## 📊 Performance

- **Ingestion**: ~10-15 seconds for 20 chunks
- **Query**: ~2-3 seconds (embedding + search + generation)
- **Accuracy**: Depends on document quality and chunk size

## 🤝 Contributing

Feel free to:
- Add more tools to the agent
- Improve chunking strategies
- Add conversation memory
- Implement re-ranking

## 📄 License

MIT

## 🙏 Acknowledgments

- LangChain for the framework
- Google for Gemini
- Cohere for embeddings
- Pinecone for vector database

---

**Built with ❤️ as part of a LangChain learning journey**
