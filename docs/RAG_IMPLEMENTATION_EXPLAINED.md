# RAG Implementation - Complete Deep Dive

## Overview

Your RAG (Retrieval-Augmented Generation) system consists of two main scripts that work together to enable question-answering from your documents.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    INGESTION PHASE (One-time)               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  mediumblog1.txt (16KB)                                     │
│         ↓                                                   │
│  TextLoader - Load document                                 │
│         ↓                                                   │
│  CharacterTextSplitter - Split into chunks                  │
│         ↓                                                   │
│  20 chunks (~1000 chars each)                               │
│         ↓                                                   │
│  CohereEmbeddings - Convert to vectors (1024 dimensions)    │
│         ↓                                                   │
│  Pinecone - Store vectors in cloud database                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    QUERY PHASE (Every query)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Question: "What is Pinecone?"                         │
│         ↓                                                   │
│  CohereEmbeddings - Convert question to vector              │
│         ↓                                                   │
│  Pinecone - Search for similar vectors                      │
│         ↓                                                   │
│  Top 4 most relevant chunks retrieved                       │
│         ↓                                                   │
│  Prompt = Question + Retrieved chunks                       │
│         ↓                                                   │
│  Gemini LLM - Generate answer from context                  │
│         ↓                                                   │
│  Final Answer                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File 1: `ingestion.py` - The Data Pipeline

### Purpose
Prepares your documents for semantic search by converting them into vector embeddings and storing them in Pinecone.

### Step-by-Step Breakdown

#### Step 1: Load the Document
```python
loader = TextLoader("/Users/pranavnew/Documents/project/langchain/langchain-course/mediumblog1.txt")
document = loader.load()
```

**What happens:**
- Reads the entire text file
- Returns a `Document` object with:
  - `page_content`: The actual text
  - `metadata`: File path and other info

**Result:** One large document object

---

#### Step 2: Split into Chunks
```python
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(document)
```

**Why split?**
- LLMs have context limits
- Smaller chunks = more precise retrieval
- Better semantic matching

**Parameters:**
- `chunk_size=1000`: Each chunk is ~1000 characters
- `chunk_overlap=0`: No overlap between chunks

**Result:** 20 smaller document chunks

**Example chunks:**
```
Chunk 1: "Pinecone is a fully managed cloud-based vector database..."
Chunk 2: "Weaviate can store and search vectors from various data..."
Chunk 3: "ChatGPT prompts 47 stories · 1439 saves..."
...
```

---

#### Step 3: Create Embeddings
```python
embeddings = CohereEmbeddings(model="embed-english-v3.0")
```

**What are embeddings?**
- Numerical representations of text
- Similar text → similar vectors
- 1024 dimensions (1024 numbers per chunk)

**Example:**
```
Text: "Pinecone is a vector database"
Embedding: [0.23, -0.45, 0.67, ..., 0.12]  # 1024 numbers
```

**Why Cohere?**
- Free tier: 100 calls/minute
- Fast and efficient
- 1024 dimensions (matches your Pinecone index)

---

#### Step 4: Store in Pinecone
```python
PineconeVectorStore.from_documents(
    texts, embeddings, index_name=os.environ["INDEX_NAME"]
)
```

**What happens:**
1. For each of the 20 chunks:
   - Convert text to embedding (1024 numbers)
   - Send to Pinecone with metadata
2. Pinecone stores:
   - Vector (the 1024 numbers)
   - Original text (for retrieval)
   - Metadata (source file path)

**Pinecone Storage:**
```
ID: acc7b09f-ab43-4226-978b-fc27e7da38ce
Vector: [0.23, -0.45, 0.67, ..., 0.12]
Text: "Pinecone is designed to be fast and scalable..."
Metadata: {source: '/Users/.../mediumblog1.txt'}
```

**Result:** 20 vectors stored in Pinecone, ready for search

---

## File 2: `main.py` - The Query System

### Purpose
Answers user questions by retrieving relevant document chunks and using Gemini to generate answers.

### Step-by-Step Breakdown

#### Step 1: Initialize Components
```python
embeddings = CohereEmbeddings(model="embed-english-v3.0")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
```

**Embeddings:** Same model as ingestion (critical!)
**LLM:** Gemini for generating answers
**temperature=0:** Deterministic responses (same question = same answer)

---

#### Step 2: Connect to Pinecone
```python
vectorstore = PineconeVectorStore(
    index_name=os.environ["INDEX_NAME"], 
    embedding=embeddings
)
```

**What this does:**
- Connects to your Pinecone index
- Uses the same embedding model for consistency
- Ready to search the 20 stored vectors

---

#### Step 3: Get RAG Prompt Template
```python
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
```

**What is this?**
- A pre-built prompt template from LangChain Hub
- Optimized for RAG question-answering
- Tells the LLM: "Answer based on the context provided"

**The prompt looks like:**
```
Use the following pieces of context to answer the question.
If you don't know the answer, say you don't know.

Context: {context}

Question: {question}

Answer:
```

---

#### Step 4: Create Document Chain
```python
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
```

**What is "stuff"?**
- A strategy for combining documents
- "Stuffs" all retrieved docs into one prompt
- Simple and effective for small contexts

**Other strategies exist:**
- Map-reduce: Summarize each doc, then combine
- Refine: Iteratively refine answer with each doc
- Map-rerank: Score each doc's relevance

**This chain does:**
1. Takes retrieved documents
2. Formats them with the prompt template
3. Sends to Gemini
4. Returns the answer

---

#### Step 5: Create Retrieval Chain
```python
retrival_chain = create_retrieval_chain(
    retriever=vectorstore.as_retriever(), 
    combine_docs_chain=combine_docs_chain
)
```

**This is the complete RAG pipeline!**

**What `as_retriever()` does:**
- Converts vectorstore to a retriever
- Default: Returns top 4 most similar chunks
- Uses cosine similarity to find matches

**The complete chain:**
```
Question → Embed → Search Pinecone → Get top 4 chunks → 
Format prompt → Send to Gemini → Return answer
```

---

#### Step 6: Execute Query
```python
query = "what is Pinecone in machine learning?"
result = retrival_chain.invoke(input={"input": query})
```

**What happens internally:**

1. **Embed the question:**
   ```
   "what is Pinecone in machine learning?"
   → [0.12, -0.34, 0.56, ..., 0.78]  # 1024 numbers
   ```

2. **Search Pinecone:**
   - Compare query vector with all 20 stored vectors
   - Use cosine similarity to find closest matches
   - Return top 4 most similar chunks

3. **Retrieved chunks:**
   ```
   Chunk 1: "Pinecone is designed to be fast and scalable..."
   Chunk 2: "Pinecone is a fully managed cloud-based vector database..."
   Chunk 3: "Some Pinecone Features:..."
   Chunk 4: "Experimenting with Vector Databases: Chromadb, Pinecone..."
   ```

4. **Format prompt:**
   ```
   Use the following context to answer the question.
   
   Context:
   [Chunk 1 text]
   [Chunk 2 text]
   [Chunk 3 text]
   [Chunk 4 text]
   
   Question: what is Pinecone in machine learning?
   
   Answer:
   ```

5. **Send to Gemini:**
   - Gemini reads the context
   - Generates answer based on retrieved chunks
   - Returns structured response

6. **Result structure:**
   ```python
   {
       'input': 'what is Pinecone in machine learning?',
       'context': [Document(...), Document(...), ...],  # 4 chunks
       'answer': 'In machine learning, Pinecone is a fully managed...'
   }
   ```

---

## Key Concepts Explained

### 1. Vector Embeddings

**What they are:**
- Numerical representations of text
- Capture semantic meaning
- Similar text → similar vectors

**Example:**
```
"dog" → [0.2, 0.8, 0.1, ...]
"puppy" → [0.3, 0.7, 0.2, ...]  # Similar!
"car" → [-0.5, 0.1, 0.9, ...]   # Different!
```

**Why 1024 dimensions?**
- More dimensions = more nuanced meaning
- Cohere's `embed-english-v3.0` produces 1024-d vectors
- Must match Pinecone index dimensions

---

### 2. Semantic Search

**Traditional keyword search:**
```
Query: "vector database"
Matches: Documents containing "vector" AND "database"
```

**Semantic search:**
```
Query: "vector database"
Matches: Documents about:
- Vector databases
- Embedding storage
- Similarity search
- ML data management
```

**How it works:**
1. Convert query to embedding
2. Find vectors with smallest distance
3. Distance = how similar the meaning is

**Distance metrics:**
- **Cosine similarity**: Measures angle between vectors (used by Pinecone)
- **Euclidean distance**: Straight-line distance
- **Dot product**: Vector multiplication

---

### 3. The "Stuff" Strategy

**Why it's called "stuff":**
- Literally "stuffs" all documents into one prompt
- Simple concatenation

**Example:**
```python
# Input: 4 retrieved documents
docs = [doc1, doc2, doc3, doc4]

# Output: One big prompt
prompt = f"""
Context:
{doc1.page_content}
{doc2.page_content}
{doc3.page_content}
{doc4.page_content}

Question: {question}
"""
```

**Limitations:**
- Token limit: Can't stuff too many docs
- Your case: 4 docs × ~1000 chars = ~4000 chars (well within limits)

---

### 4. Retrieval Chain Flow

```
User Input
    ↓
┌─────────────────────┐
│  Retriever          │
│  - Embed query      │
│  - Search Pinecone  │
│  - Get top 4 chunks │
└─────────────────────┘
    ↓
Retrieved Documents
    ↓
┌─────────────────────┐
│  Combine Docs Chain │
│  - Format prompt    │
│  - Add context      │
│  - Send to LLM      │
└─────────────────────┘
    ↓
Final Answer
```

---

## Your Specific Implementation

### Components Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Embeddings** | Cohere `embed-english-v3.0` | Convert text to 1024-d vectors |
| **Vector DB** | Pinecone | Store and search vectors |
| **LLM** | Gemini `gemini-2.5-flash-lite` | Generate answers |
| **Document Loader** | TextLoader | Read text files |
| **Text Splitter** | CharacterTextSplitter | Split into chunks |
| **Prompt** | LangChain Hub template | Format RAG prompts |

### Why These Choices?

**Cohere:**
- ✅ Free tier (100 calls/min)
- ✅ Fast embeddings
- ✅ 1024 dimensions (good balance)

**Pinecone:**
- ✅ Managed service (no setup)
- ✅ Fast similarity search
- ✅ Scales to billions of vectors

**Gemini:**
- ✅ Free tier available
- ✅ Fast responses
- ✅ Good at following instructions

---

## Complete Data Flow Example

### Ingestion (One-time):
```
mediumblog1.txt (16KB)
    ↓ TextLoader
Document(page_content="Pinecone is a fully managed...")
    ↓ CharacterTextSplitter(chunk_size=1000)
[
  Document("Pinecone is designed..."),
  Document("Weaviate can store..."),
  ...  # 20 total
]
    ↓ CohereEmbeddings
[
  [0.23, -0.45, ...],  # 1024 numbers
  [0.12, 0.67, ...],   # 1024 numbers
  ...  # 20 vectors
]
    ↓ Pinecone
Stored in cloud, ready for search
```

### Query (Every time):
```
"What is Pinecone?"
    ↓ CohereEmbeddings
[0.15, -0.32, 0.78, ...]  # Query vector
    ↓ Pinecone.search()
[
  Document("Pinecone is designed..."),  # 95% similar
  Document("Pinecone is a fully..."),   # 93% similar
  Document("Some Pinecone Features:"),  # 89% similar
  Document("Experimenting with..."),    # 85% similar
]
    ↓ Format Prompt
"Context: [4 chunks]\nQuestion: What is Pinecone?\nAnswer:"
    ↓ Gemini
"In machine learning, Pinecone is a fully managed, cloud-based..."
```

---

## Advanced Concepts

### 1. Why Top 4 Chunks?

**Default retriever settings:**
```python
vectorstore.as_retriever()  # Default k=4
```

**You can customize:**
```python
vectorstore.as_retriever(
    search_kwargs={"k": 10}  # Get top 10 chunks
)
```

**Trade-offs:**
- More chunks = more context = better answers
- More chunks = longer prompts = slower + more expensive
- Sweet spot: 3-5 chunks for most use cases

---

### 2. Similarity Scoring

**How Pinecone ranks results:**
```python
# Your query vector
query_vec = [0.15, -0.32, 0.78, ...]

# Stored vectors
doc1_vec = [0.16, -0.30, 0.75, ...]  # Very similar!
doc2_vec = [0.14, -0.35, 0.80, ...]  # Very similar!
doc3_vec = [-0.50, 0.20, -0.10, ...] # Not similar

# Cosine similarity scores
doc1: 0.95  # Top result
doc2: 0.93  # Second
doc3: 0.45  # Not retrieved
```

---

### 3. Metadata Filtering

**You can filter by metadata:**
```python
vectorstore.as_retriever(
    search_kwargs={
        "k": 4,
        "filter": {"source": "mediumblog1.txt"}
    }
)
```

**Use cases:**
- Filter by date
- Filter by author
- Filter by document type

---

## Performance Characteristics

### Ingestion:
- **Time**: ~10-15 seconds for 20 chunks
- **API calls**: 20 embedding calls to Cohere
- **Storage**: 20 vectors in Pinecone

### Query:
- **Time**: ~2-3 seconds total
  - Embedding: ~0.5s
  - Pinecone search: ~0.2s
  - Gemini generation: ~1-2s
- **API calls**: 1 embedding + 1 LLM call

---

## Limitations & Improvements

### Current Limitations:

1. **Chunk size**: Fixed at 1000 chars
   - May split sentences awkwardly
   - **Solution**: Use RecursiveCharacterTextSplitter

2. **No chunk overlap**: Information at boundaries may be lost
   - **Solution**: Set `chunk_overlap=200`

3. **No re-ranking**: Top 4 chunks may not be optimal
   - **Solution**: Use Cohere Rerank API

4. **No conversation memory**: Each query is independent
   - **Solution**: Add ConversationBufferMemory

### Potential Improvements:

```python
# Better text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,  # Overlap for context
    separators=["\n\n", "\n", ". ", " "]  # Smart splitting
)

# Re-ranking
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

compressor = CohereRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# Conversation memory
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)
```

---

## Summary

Your RAG implementation is a **production-ready system** that:

1. ✅ Loads documents from disk
2. ✅ Splits them into semantic chunks
3. ✅ Converts to vector embeddings
4. ✅ Stores in cloud vector database
5. ✅ Retrieves relevant context for queries
6. ✅ Generates accurate answers using LLM

**Key strengths:**
- Uses free-tier services (Cohere + Gemini)
- Scalable (Pinecone can handle billions of vectors)
- Fast (2-3 second query time)
- Accurate (semantic search + powerful LLM)

**This is the foundation for:**
- Chatbots over documentation
- Q&A systems for knowledge bases
- Semantic search engines
- AI assistants with custom knowledge

Congratulations on building a complete RAG system! 🎉
