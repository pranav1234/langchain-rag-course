# RAG Basics - Retrieval-Augmented Generation

This module demonstrates a complete RAG (Retrieval-Augmented Generation) implementation using LangChain.

## 📚 What's Inside

- **`main.py`**: Query system with retrieval chain
- **`ingestion.py`**: Document processing and embedding pipeline
- **`mediumblog1.txt`**: Sample document about vector databases

## 🎯 What You'll Learn

1. Document loading and chunking
2. Creating vector embeddings with Cohere
3. Storing vectors in Pinecone
4. Semantic search and retrieval
5. Generating answers with Gemini LLM

## 🚀 Quick Start

### 1. Ingest Documents (One-time)
```bash
python ingestion.py
```

This will:
- Load `mediumblog1.txt`
- Split into ~20 chunks (1000 chars each)
- Convert to embeddings (Cohere)
- Store in Pinecone

### 2. Query the System
```bash
python main.py
```

Ask questions like:
- "What is Pinecone in machine learning?"
- "What are vector databases?"
- "How does semantic search work?"

## 🏗️ Architecture

```
Document (mediumblog1.txt)
    ↓
TextLoader - Load file
    ↓
CharacterTextSplitter - Split into chunks
    ↓
CohereEmbeddings - Convert to vectors (1024-d)
    ↓
Pinecone - Store vectors
    ↓
[QUERY TIME]
    ↓
User Question → Embed → Search Pinecone → Retrieve top 4 chunks
    ↓
Format Prompt with context
    ↓
Gemini LLM - Generate answer
```

## 🔧 Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Embeddings** | Cohere `embed-english-v3.0` | Convert text to 1024-d vectors |
| **Vector DB** | Pinecone | Store and search vectors |
| **LLM** | Gemini `gemini-2.5-flash-lite` | Generate answers |
| **Text Splitter** | CharacterTextSplitter | Split docs into chunks |

## 📝 Code Walkthrough

### ingestion.py
```python
# 1. Load document
loader = TextLoader("mediumblog1.txt")
document = loader.load()

# 2. Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(document)

# 3. Create embeddings and store
embeddings = CohereEmbeddings(model="embed-english-v3.0")
PineconeVectorStore.from_documents(texts, embeddings, index_name=INDEX_NAME)
```

### main.py
```python
# 1. Connect to Pinecone
vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

# 2. Create retrieval chain
retrieval_chain = create_retrieval_chain(
    retriever=vectorstore.as_retriever(),
    combine_docs_chain=combine_docs_chain
)

# 3. Query
result = retrieval_chain.invoke({"input": "What is Pinecone?"})
```

## 🎓 Key Concepts

### Vector Embeddings
- Numerical representations of text
- Similar text → similar vectors
- 1024 dimensions = 1024 numbers per chunk

### Semantic Search
- Search by meaning, not keywords
- Uses cosine similarity
- Finds conceptually related content

### RAG Pipeline
1. **Retrieve**: Find relevant chunks from vector DB
2. **Augment**: Add chunks to prompt as context
3. **Generate**: LLM creates answer from context

## 🔍 How It Works

**Example Query**: "What is Pinecone?"

1. **Embed query** → `[0.15, -0.32, 0.78, ...]` (1024 numbers)
2. **Search Pinecone** → Find 4 most similar chunks
3. **Retrieved chunks**:
   - "Pinecone is a fully managed cloud-based vector database..."
   - "Pinecone is designed to be fast and scalable..."
   - "Some Pinecone Features:..."
   - "Experimenting with Vector Databases..."
4. **Format prompt**:
   ```
   Context: [4 chunks]
   Question: What is Pinecone?
   Answer:
   ```
5. **Gemini generates**: "In machine learning, Pinecone is a fully managed..."

## 📊 Performance

- **Ingestion**: ~10-15 seconds for 20 chunks
- **Query**: ~2-3 seconds
  - Embedding: ~0.5s
  - Search: ~0.2s
  - Generation: ~1-2s

## 🛠️ Customization

### Change chunk size
```python
text_splitter = CharacterTextSplitter(
    chunk_size=500,      # Smaller chunks
    chunk_overlap=100    # Add overlap
)
```

### Retrieve more chunks
```python
vectorstore.as_retriever(search_kwargs={"k": 10})
```

### Use different models
```python
# Different LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Different embeddings
embeddings = CohereEmbeddings(model="embed-multilingual-v3.0")
```

## 📚 Next Steps

After mastering this module:
1. Try different chunking strategies
2. Experiment with chunk overlap
3. Add metadata filtering
4. Implement re-ranking
5. Add conversation memory

## 🔗 Related Documentation

See `/docs` folder for:
- `RAG_IMPLEMENTATION_EXPLAINED.md` - Deep dive
- `COHERE_SETUP.md` - API key setup
- `GITHUB_UPLOAD_GUIDE.md` - Git workflow
