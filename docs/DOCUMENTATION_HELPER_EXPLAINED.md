# LangChain Documentation Helper - Deep Dive

This document provides an in-depth explanation of the advanced RAG concepts used in Module 03.

## Table of Contents

1. [Web Crawling Strategy](#web-crawling-strategy)
2. [Conversational Memory Patterns](#conversational-memory-patterns)
3. [Advanced Text Splitting](#advanced-text-splitting)
4. [Source Attribution System](#source-attribution-system)
5. [Streamlit Architecture](#streamlit-architecture)
6. [Production Considerations](#production-considerations)

---

## Web Crawling Strategy

### Why Tavily?

Traditional web scraping requires:
- HTML parsing with BeautifulSoup
- Handling JavaScript rendering
- Cleaning HTML artifacts
- Managing rate limits manually
- Dealing with anti-scraping measures

**Tavily solves this** by providing:
- AI-powered content extraction
- Pre-cleaned, structured output
- Built-in rate limiting
- JavaScript execution
- Relevance scoring

### Tavily API Flow

```python
# 1. Search-based crawling
response = client.search(
    query="LangChain RAG tutorial",
    search_depth="advanced",  # More thorough
    max_results=5,
    include_domains=["python.langchain.com"]
)

# Returns:
{
    "results": [
        {
            "url": "https://python.langchain.com/docs/tutorials/rag",
            "title": "Build a Retrieval Augmented Generation (RAG) App",
            "content": "Clean, extracted text...",
            "score": 0.95  # Relevance score
        }
    ]
}
```

### Content Quality

Tavily returns **clean content**:
- No HTML tags
- No navigation menus
- No ads or footers
- Just the main article text

This means **better embeddings** because:
- Less noise in vector representations
- More relevant semantic matches
- Smaller chunk sizes needed

### Crawling Strategies

**Strategy 1: Search-based** (used in this module)
```python
crawler.search_langchain_docs("LangChain agents", max_results=5)
```
- Pros: Finds most relevant content
- Cons: May miss some pages

**Strategy 2: URL-based**
```python
urls = [
    "https://python.langchain.com/docs/tutorials/rag",
    "https://python.langchain.com/docs/tutorials/agents"
]
crawler.crawl_specific_urls(urls)
```
- Pros: Guaranteed coverage of specific pages
- Cons: Manual URL management

**Strategy 3: Hybrid** (recommended for production)
```python
# Start with search
docs = crawler.search_langchain_docs("LangChain", max_results=10)

# Add critical pages
critical_urls = ["https://python.langchain.com/docs/get_started/introduction"]
docs.extend(crawler.crawl_specific_urls(critical_urls))
```

---

## Conversational Memory Patterns

### Memory Types in LangChain

| Type | Description | Use Case | Memory Usage |
|------|-------------|----------|--------------|
| **ConversationBufferMemory** | Stores all messages | Short conversations | High |
| **ConversationBufferWindowMemory** | Keeps last N messages | Long conversations | Medium |
| **ConversationSummaryMemory** | Summarizes old messages | Very long conversations | Low |
| **ConversationSummaryBufferMemory** | Hybrid approach | Production apps | Medium |

### Our Implementation

We use **ConversationBufferMemory** with a **10-turn limit**:

```python
class ConversationMemoryManager:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
```

**Why 10 turns?**
- Balances context vs. token limits
- Covers most conversation flows
- Prevents context window overflow
- ~2000-3000 tokens typically

### Coreference Resolution

**The Problem**:
```
User: "What is LangChain?"
AI: "LangChain is a framework..."
User: "How do I install it?"  ← What is "it"?
```

**The Solution**:
Include conversation history in the prompt:

```python
prompt = f"""
Previous conversation:
Human: What is LangChain?
Assistant: LangChain is a framework...

Current question: How do I install it?

Answer:
"""
```

The LLM uses the history to understand "it" = "LangChain".

### Memory in Retrieval Chains

**Challenge**: Standard retrieval chains don't have memory.

**Solution**: Inject history into the prompt:

```python
# Build chat history string
chat_history = ""
for msg in conversation:
    role = "Human" if msg["role"] == "user" else "Assistant"
    chat_history += f"{role}: {msg['content']}\n"

# Pass to chain
result = retrieval_chain.invoke({
    "input": current_question,
    "chat_history": chat_history  # ← Injected here
})
```

### Memory Management Best Practices

1. **Limit history length**: Prevent token overflow
2. **Clear on topic change**: Detect topic shifts and reset
3. **Summarize old messages**: For very long conversations
4. **Store externally**: Use database for persistence across sessions

---

## Advanced Text Splitting

### Character vs. Recursive Splitting

**CharacterTextSplitter** (Module 01):
```python
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
```
- Splits at exact character count
- May break mid-sentence
- No semantic awareness

**RecursiveCharacterTextSplitter** (Module 03):
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
```
- Tries separators in order
- Preserves paragraphs
- Keeps sentences together
- Better semantic coherence

### How Recursive Splitting Works

```
Input text (1500 chars):
"Paragraph 1...\n\nParagraph 2...\n\nParagraph 3..."

Step 1: Try splitting on "\n\n" (paragraphs)
→ Chunk 1: "Paragraph 1..." (800 chars) ✓
→ Chunk 2: "Paragraph 2..." (700 chars) ✓

Result: 2 chunks, both under 1000 chars
```

**If chunks still too large**:
```
Step 2: Try splitting on "\n" (lines)
Step 3: Try splitting on " " (words)
Step 4: Last resort: split on characters
```

### Chunk Overlap

**Why overlap?**

Without overlap:
```
Chunk 1: "...LangChain provides tools for"
Chunk 2: "building LLM applications..."
```
Context is lost at the boundary!

With 200-char overlap:
```
Chunk 1: "...LangChain provides tools for building LLM applications..."
Chunk 2: "...tools for building LLM applications with memory..."
```
Context preserved!

**Trade-offs**:
- ✅ Better context continuity
- ✅ Fewer missed retrievals
- ❌ More storage (duplicate content)
- ❌ Slightly slower ingestion

**Optimal overlap**: 10-20% of chunk size
- 1000 char chunks → 100-200 char overlap

---

## Source Attribution System

### Metadata Flow

```
1. Web Crawling
   ↓
   Document {
       content: "LangChain is...",
       metadata: {
           url: "https://...",
           title: "Getting Started",
           type: "web"
       }
   }

2. Text Splitting
   ↓
   Chunk {
       content: "LangChain is...",
       metadata: {  ← Preserved!
           url: "https://...",
           title: "Getting Started",
           type: "web"
       }
   }

3. Embedding & Storage
   ↓
   Pinecone stores metadata alongside vectors

4. Retrieval
   ↓
   Retrieved chunks include metadata

5. Display
   ↓
   Show source URLs in UI
```

### Metadata Schema

```python
{
    "source": "https://python.langchain.com/docs/tutorials/rag",
    "title": "Build a RAG App",
    "type": "web",  # or "local"
    "score": 0.95,  # Similarity score
}
```

### Deduplication

**Problem**: Same URL retrieved multiple times

**Solution**:
```python
seen_urls = set()
unique_sources = []

for doc in retrieved_docs:
    url = doc.metadata["source"]
    if url not in seen_urls:
        seen_urls.add(url)
        unique_sources.append(doc)
```

### Citation Formats

**Simple**:
```
Sources:
1. Build a RAG App
   https://python.langchain.com/docs/tutorials/rag
```

**With Preview**:
```
Sources:
1. Build a RAG App
   https://python.langchain.com/docs/tutorials/rag
   "LangChain provides a framework for building RAG applications..."
```

**Inline** (advanced):
```
LangChain is a framework [1] that provides tools for RAG [2].

[1] https://python.langchain.com/docs/get_started/introduction
[2] https://python.langchain.com/docs/tutorials/rag
```

---

## Streamlit Architecture

### Session State Management

Streamlit **reruns the entire script** on every interaction!

**Problem**: Variables reset on each rerun

**Solution**: `st.session_state`

```python
# Initialize once
if "messages" not in st.session_state:
    st.session_state.messages = []

# Persists across reruns
st.session_state.messages.append({"role": "user", "content": "Hello"})
```

### Caching with `@st.cache_resource`

**Problem**: Reinitializing LLM/vectorstore on every rerun is slow

**Solution**: Cache expensive operations

```python
@st.cache_resource
def initialize_system():
    embeddings = CohereEmbeddings(...)
    llm = ChatGoogleGenerativeAI(...)
    vectorstore = PineconeVectorStore(...)
    return retrieval_chain

# Called once, cached forever
chain = initialize_system()
```

**When to cache**:
- ✅ Model initialization
- ✅ Database connections
- ✅ Loading large files
- ❌ User-specific data
- ❌ Frequently changing data

### Chat Interface Pattern

```python
# 1. Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Get new input
user_input = st.chat_input("Ask a question...")

# 3. Process and display
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate response
    with st.chat_message("assistant"):
        response = generate_response(user_input)
        st.markdown(response)
    
    # Add to history
    st.session_state.messages.append({"role": "assistant", "content": response})
```

### Expandable Sections

```python
with st.expander("📚 View Sources", expanded=False):
    for source in sources:
        st.markdown(f"**{source['title']}**")
        st.markdown(f"[{source['url']}]({source['url']})")
```

**Benefits**:
- Cleaner UI
- Optional information
- Better mobile experience

---

## Production Considerations

### Scaling Strategies

**1. Caching Layer**
```python
import redis

cache = redis.Redis()

def get_answer(question):
    # Check cache first
    cached = cache.get(question)
    if cached:
        return cached
    
    # Generate if not cached
    answer = retrieval_chain.invoke({"input": question})
    cache.set(question, answer, ex=3600)  # 1 hour TTL
    return answer
```

**2. Async Processing**
```python
import asyncio

async def process_query(question):
    # Parallel retrieval and generation
    retrieval_task = asyncio.create_task(retrieve_docs(question))
    
    docs = await retrieval_task
    answer = await generate_answer(docs, question)
    
    return answer
```

**3. Load Balancing**
- Use multiple Pinecone replicas
- Round-robin LLM requests
- Queue system for high traffic

### Cost Optimization

**Embeddings** (Cohere):
- Free tier: 100 calls/min
- Cache embeddings for common queries
- Batch embed during ingestion

**LLM** (Gemini):
- Free tier: 60 requests/min
- Use streaming for better UX
- Implement rate limiting

**Vector DB** (Pinecone):
- Free tier: 1 index, 100k vectors
- Archive old documents
- Use namespaces for multi-tenancy

### Error Handling

```python
try:
    result = retrieval_chain.invoke({"input": query})
except RateLimitError:
    st.error("Too many requests. Please wait a moment.")
except PineconeException:
    st.error("Database error. Please try again.")
except Exception as e:
    st.error(f"Unexpected error: {e}")
    # Log to monitoring service
    logger.error(f"Query failed: {query}", exc_info=True)
```

### Monitoring

**Key Metrics**:
- Query latency (p50, p95, p99)
- Retrieval accuracy
- User satisfaction (thumbs up/down)
- Error rates
- API costs

**Tools**:
- LangSmith for LangChain tracing
- Streamlit analytics
- Custom logging

### Security

**1. API Key Management**
```python
# ❌ Never do this
api_key = "sk-1234567890"

# ✅ Use environment variables
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Use secret management
from google.cloud import secretmanager
api_key = get_secret("openai-api-key")
```

**2. Input Validation**
```python
def validate_input(query: str) -> bool:
    if len(query) > 500:
        return False
    if contains_malicious_content(query):
        return False
    return True
```

**3. Rate Limiting**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
def query_endpoint(request):
    # Process query
    pass
```

---

## Summary

This module demonstrates:
- ✅ **Web crawling** with Tavily for dynamic content
- ✅ **Conversational memory** for multi-turn interactions
- ✅ **Advanced text splitting** for better chunks
- ✅ **Source attribution** for transparency
- ✅ **Streamlit** for production-ready UI
- ✅ **Production patterns** for scaling

**Next Steps**:
- Add re-ranking for better retrieval
- Implement streaming responses
- Deploy to Streamlit Cloud
- Add user feedback loop
- Integrate with other data sources
