# Documentation Helper - Advanced RAG with Web Crawling & Memory

A sophisticated AI-powered documentation assistant that serves as a slim version of chat.langchain.com. This module builds upon the foundational RAG concepts from Module 01, adding web crawling, conversational memory, and an interactive Streamlit interface.

## 📚 What's Inside

- **`app.py`**: Streamlit web interface with chat UI
- **`crawler.py`**: Tavily-powered web scraping for LangChain docs
- **`ingestion.py`**: Enhanced document processing pipeline
- **`memory.py`**: Conversational memory system
- **`main.py`**: CLI query engine (for testing)

## 🎯 What You'll Learn

1. **Web Crawling** with Tavily for intelligent content extraction
2. **Conversational Memory** for multi-turn conversations
3. **Streamlit Development** for chat interfaces
4. **Source Attribution** to show where answers come from
5. **Advanced RAG** techniques (recursive splitting, metadata)

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|-----------|-------------|
| 🖥️ **Frontend** | Streamlit | Interactive web interface |
| 🧠 **AI Framework** | LangChain 🦜🔗 | Orchestrates the AI pipeline |
| 🔍 **Vector Database** | Pinecone 🌲 | Stores and retrieves embeddings |
| 🌐 **Web Crawling** | Tavily | Intelligent web scraping |
| 🧩 **Memory** | ConversationBufferMemory | Context continuity |
| 🤖 **LLM** | Gemini 2.5 Flash Lite | Powers the AI |
| 🔢 **Embeddings** | Cohere v3.0 | 1024-d vectors |

## 🚀 Quick Start

### 1. Install Dependencies

First, update your dependencies:

```bash
# Add new packages to pyproject.toml
uv add streamlit tavily-python

# Or using pip
pip install streamlit tavily-python
```

### 2. Get Tavily API Key

1. Visit https://tavily.com/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env`:

```bash
TAVILY_API_KEY=your_tavily_key_here
```

### 3. Run Ingestion (One-time)

This crawls LangChain documentation and stores it in Pinecone:

```bash
cd 03-documentation-helper
python ingestion.py
```

**Expected Output**:
- Crawls ~15 web pages from LangChain docs
- Loads local file from Module 01
- Creates ~100-150 chunks with metadata
- Stores in Pinecone

**Time**: ~30-60 seconds

### 4. Launch the Web App

```bash
streamlit run app.py
```

This opens http://localhost:8501 in your browser.

### 5. Start Chatting!

Try these example questions:
- "What is LangChain?"
- "How do I create a retrieval chain?"
- "What are the different types of agents?"
- "Show me an example of LCEL"

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INGESTION PHASE                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Web Docs (Tavily) ──┐                                 │
│                      ├──→ Crawler ──→ Documents        │
│  Local Files ────────┘                                  │
│                                                         │
│  Documents ──→ RecursiveTextSplitter ──→ Chunks        │
│                                                         │
│  Chunks ──→ Cohere Embeddings ──→ Pinecone             │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     QUERY PHASE                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User Question ──→ Streamlit UI                        │
│                                                         │
│  Question + Chat History ──→ Embed ──→ Pinecone        │
│                                                         │
│  Pinecone ──→ Top 4 Chunks (with metadata)             │
│                                                         │
│  Chunks + Question + History ──→ Gemini LLM            │
│                                                         │
│  Answer + Sources ──→ Display in UI                    │
│                                                         │
│  Update Conversation Memory                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Components Deep Dive

### 1. Web Crawler (`crawler.py`)

**Purpose**: Intelligently fetch LangChain documentation from the web

**Key Features**:
- Uses Tavily API for smart web scraping
- Filters to official LangChain domains
- Extracts clean content (no HTML noise)
- Preserves metadata (URLs, titles, scores)

**Example Usage**:
```python
from crawler import LangChainDocCrawler

crawler = LangChainDocCrawler()
docs = crawler.search_langchain_docs("LangChain RAG tutorial", max_results=5)
```

### 2. Enhanced Ingestion (`ingestion.py`)

**Improvements over Module 01**:
- ✅ **Multiple Sources**: Local files + web content
- ✅ **Recursive Splitting**: Smarter chunking (preserves paragraphs)
- ✅ **Chunk Overlap**: 200 chars overlap for context continuity
- ✅ **Metadata Tracking**: Source URLs, titles, document type

**Chunking Strategy**:
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,  # NEW: Overlap for better context
    separators=["\n\n", "\n", " ", ""]  # Try in order
)
```

### 3. Conversational Memory (`memory.py`)

**Purpose**: Maintain conversation context across multiple turns

**Features**:
- Stores last 10 conversation turns
- Formats history for prompt injection
- Enables coreference resolution ("it", "that", "the previous example")

**Example**:
```
User: "What is LangChain?"
AI: "LangChain is a framework for developing LLM applications..."

User: "How do I install it?"  ← "it" refers to LangChain
AI: "You can install LangChain using pip install langchain"
```

### 4. Streamlit Interface (`app.py`)

**Features**:
- 💬 Chat-like interface with message history
- 📚 Expandable source citations
- 🎨 Modern, clean design
- 🔄 Real-time streaming responses
- 🧹 Clear conversation button
- 💡 Example questions in sidebar

**Session Management**:
- Conversation history stored in `st.session_state`
- Persists across interactions within a session
- Cleared when browser refreshed or "Clear" clicked

### 5. CLI Version (`main.py`)

**Purpose**: Test the system without Streamlit

**Usage**:
```bash
python main.py
```

**Features**:
- Interactive query loop
- Displays answers and sources
- Commands: `quit`, `clear`

## 📊 Comparison with Module 01

| Feature | Module 01 (Basic RAG) | Module 03 (Advanced RAG) |
|---------|----------------------|--------------------------|
| **Data Sources** | Single local file | Local + Web crawling |
| **Text Splitting** | CharacterTextSplitter | RecursiveCharacterTextSplitter |
| **Chunk Overlap** | None | 200 characters |
| **Metadata** | Basic | Rich (URLs, titles, type) |
| **Interface** | CLI only | Streamlit + CLI |
| **Memory** | None | Conversational memory |
| **Source Attribution** | No | Yes, with URLs |
| **Coreference** | No | Yes |

## 🎓 Key Concepts

### 1. Web Crawling with Tavily

**Why Tavily?**
- Designed for AI applications
- Returns clean, structured content
- Handles JavaScript-heavy sites
- Respects robots.txt
- Free tier available

**vs. Traditional Scraping**:
- No need for BeautifulSoup parsing
- No HTML cleanup required
- Built-in rate limiting
- Better content extraction

### 2. Conversational Memory

**Types of Memory**:
- **ConversationBufferMemory**: Stores all messages (used here)
- **ConversationSummaryMemory**: Summarizes old messages
- **ConversationBufferWindowMemory**: Keeps last N messages

**Coreference Resolution**:
The LLM uses conversation history to understand pronouns:
```
History: "LangChain is a framework..."
Current: "How do I use it?"
LLM understands: "it" = "LangChain"
```

### 3. Recursive Text Splitting

**How it works**:
1. Try to split on `\n\n` (paragraphs)
2. If chunks too large, split on `\n` (lines)
3. If still too large, split on spaces
4. Last resort: split on characters

**Benefits**:
- Preserves semantic coherence
- Keeps paragraphs together
- Better than arbitrary character splits

### 4. Source Attribution

**Metadata Flow**:
```
Web Doc → {url, title, type} → Chunk → Pinecone → Retrieved → Display
```

**Why Important?**:
- Verify answer accuracy
- Explore original documentation
- Build trust with users
- Debug retrieval issues

## 🔍 How It Works

### Example Conversation

**Turn 1**:
```
User: "What is LangChain?"
→ Embed query
→ Search Pinecone (no history)
→ Retrieve 4 chunks
→ Generate answer
→ Store in memory: User: "What is LangChain?" / AI: "LangChain is..."
```

**Turn 2**:
```
User: "How do I install it?"
→ Embed query
→ Search Pinecone WITH history
→ LLM sees: "Previous: What is LangChain? Current: How do I install it?"
→ LLM understands "it" = "LangChain"
→ Retrieve relevant chunks about installation
→ Generate contextual answer
→ Update memory
```

## 🛠️ Customization

### Change Crawling Scope

```python
# In crawler.py
response = self.client.search(
    query=query,
    max_results=10,  # Get more results
    include_domains=["python.langchain.com", "docs.langchain.com", "blog.langchain.dev"],
)
```

### Adjust Memory Length

```python
# In app.py or main.py
memory = ConversationMemoryManager(max_history=20)  # Keep 20 turns
```

### Modify Retrieval

```python
# In app.py
retriever=vectorstore.as_retriever(
    search_kwargs={
        "k": 6,  # Retrieve 6 chunks instead of 4
        "filter": {"type": "web"}  # Only web sources
    }
)
```

### Change UI Theme

```python
# In app.py, modify the CSS in st.markdown()
st.markdown("""
<style>
    .main-header {
        color: #ff6b6b;  # Change color
        font-size: 3rem;  # Bigger header
    }
</style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### Tavily API Errors

**Error**: `TAVILY_API_KEY not found`
- **Fix**: Add `TAVILY_API_KEY=your_key` to `.env`

**Error**: `Rate limit exceeded`
- **Fix**: Wait a minute or upgrade Tavily plan
- **Workaround**: Reduce `max_results` in crawler

### Streamlit Issues

**Error**: `streamlit: command not found`
- **Fix**: `uv add streamlit` or `pip install streamlit`

**Error**: App doesn't update
- **Fix**: Click "Always rerun" in Streamlit or press `R`

### Memory Issues

**Problem**: Responses don't use conversation context
- **Check**: Verify `chat_history` is being passed to chain
- **Debug**: Print `chat_history` before invoking chain

### Empty Results

**Problem**: No sources found
- **Fix**: Run `python ingestion.py` first
- **Check**: Verify Pinecone index has documents
- **Debug**: Test with Module 01 query to verify Pinecone works

## 📚 Next Steps

After mastering this module:

1. **Add Re-ranking**: Use Cohere re-ranker for better results
2. **Implement Streaming**: Stream LLM responses token-by-token
3. **Add Citations**: Inline citations in answers [1], [2]
4. **Multi-modal**: Add image/diagram search
5. **Feedback Loop**: Let users rate answers
6. **Deploy**: Host on Streamlit Cloud or Hugging Face Spaces

## 🔗 Related Documentation

See `/docs` folder for:
- `DOCUMENTATION_HELPER_EXPLAINED.md` - Deep dive into concepts
- `RAG_IMPLEMENTATION_EXPLAINED.md` - Module 01 basics
- `COHERE_SETUP.md` - API key setup

---

**🎉 Congratulations!** You've built an advanced RAG system with web crawling and conversational memory!

**Next Module**: Check out Module 04 for production deployment strategies.
