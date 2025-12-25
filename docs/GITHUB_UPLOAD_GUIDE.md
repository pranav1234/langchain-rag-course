# How to Upload Your LangChain Course to GitHub

## Quick Steps

### 1. Check Git Status
```bash
git status
```

### 2. Add Files to Git
```bash
# Add all files except those in .gitignore
git add .

# Or add specific files
git add main.py ingestion.py
```

### 3. Commit Your Changes
```bash
git commit -m "Add RAG system with Gemini and Cohere"
```

### 4. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `langchain-course` (or any name you like)
3. Description: "RAG system with Gemini, Cohere, and Pinecone"
4. Choose Public or Private
5. **Don't** initialize with README (you already have code)
6. Click "Create repository"

### 5. Add Remote and Push
```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/langchain-course.git

# Push to GitHub
git push -u origin main
```

---

## Important: Protect Your API Keys!

### Check .gitignore
Your `.env` file should already be in `.gitignore`. Let me verify:

```bash
cat .gitignore | grep .env
```

If `.env` is NOT in `.gitignore`, add it:
```bash
echo ".env" >> .gitignore
```

### What NOT to commit:
- ❌ `.env` (contains API keys)
- ❌ `.venv/` (virtual environment)
- ❌ `__pycache__/` (Python cache)
- ❌ `*.pyc` (compiled Python)

### What TO commit:
- ✅ `main.py`
- ✅ `ingestion.py`
- ✅ `callbacks.py`
- ✅ `pyproject.toml`
- ✅ `README.md`
- ✅ All documentation files

---

## Create a README

I'll create a README.md for your repository:

```markdown
# LangChain RAG Course

A complete implementation of RAG (Retrieval-Augmented Generation) using LangChain, Gemini, Cohere, and Pinecone.

## Features

- 🤖 **Agent with Tools**: Manual ReAct loop implementation
- 📚 **RAG System**: Question-answering from documents
- 🔍 **Semantic Search**: Using Cohere embeddings
- 💾 **Vector Database**: Pinecone for storage
- ✨ **LLM**: Google Gemini for generation

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_key
COHERE_API_KEY=your_cohere_key
PINECONE_API_KEY=your_pinecone_key
INDEX_NAME=your_index_name
```

### 3. Run Ingestion (One-time)
```bash
python ingestion.py
```

### 4. Query the System
```bash
python main.py
```

## Architecture

- **Embeddings**: Cohere `embed-english-v3.0` (1024 dimensions)
- **Vector DB**: Pinecone
- **LLM**: Gemini `gemini-2.5-flash-lite`

## Files

- `main.py` - Query system with RAG
- `ingestion.py` - Document processing and storage
- `callbacks.py` - LLM callback handlers
- `RAG_IMPLEMENTATION_EXPLAINED.md` - Detailed explanation

## License

MIT
```

---

## Complete Commands

Run these in order:

```bash
# 1. Check what will be committed
git status

# 2. Add files
git add .

# 3. Commit
git commit -m "Initial commit: RAG system with Gemini and Cohere"

# 4. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/langchain-course.git

# 5. Push
git push -u origin main
```

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/langchain-course.git
```

### Error: "branch main doesn't exist"
```bash
git branch -M main
git push -u origin main
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

---

## After Pushing

Your repository will be at:
```
https://github.com/YOUR_USERNAME/langchain-course
```

You can now:
- Share the link
- Clone it on other machines
- Collaborate with others
- Track changes over time

---

## Optional: Create requirements.txt

```bash
pip freeze > requirements.txt
```

This helps others install the same dependencies.
