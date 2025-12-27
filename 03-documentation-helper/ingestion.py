"""
Enhanced Document Ingestion Pipeline

This module processes both local files and web-crawled content, creating
embeddings and storing them in Pinecone with metadata for source attribution.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from crawler import LangChainDocCrawler

load_dotenv()


def load_local_documents(file_path: str) -> List[Document]:
    """
    Load documents from local file.
    
    Args:
        file_path: Path to the local text file
        
    Returns:
        List of Document objects
    """
    print(f"📂 Loading local file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return []
    
    try:
        loader = TextLoader(file_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} local document(s)\n")
        return documents
    except Exception as e:
        print(f"❌ Error loading local file: {e}\n")
        return []


def load_web_documents() -> List[Document]:
    """
    Load documents from web using Tavily crawler.
    
    Returns:
        List of Document objects from web sources
    """
    print("🌐 Crawling LangChain documentation from web...")
    
    try:
        crawler = LangChainDocCrawler()
        web_docs = crawler.get_langchain_basics()
        
        # Convert to LangChain Document format with metadata
        documents = []
        for doc in web_docs:
            if doc["content"].strip():  # Only add non-empty content
                documents.append(
                    Document(
                        page_content=doc["content"],
                        metadata={
                            "source": doc["url"],
                            "title": doc["title"],
                            "type": "web",
                        }
                    )
                )
        
        print(f"✅ Loaded {len(documents)} web document(s)\n")
        return documents
        
    except Exception as e:
        print(f"⚠️  Web crawling failed: {e}")
        print("Continuing with local documents only...\n")
        return []


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Split documents into chunks using RecursiveCharacterTextSplitter.
    
    This is more intelligent than CharacterTextSplitter as it:
    - Tries to split on paragraph boundaries first
    - Falls back to sentence boundaries
    - Preserves semantic coherence better
    
    Args:
        documents: List of documents to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of chunked documents with preserved metadata
    """
    print(f"✂️  Splitting documents (chunk_size={chunk_size}, overlap={chunk_overlap})...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],  # Try these in order
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks\n")
    
    return chunks


def create_embeddings_and_store(
    chunks: List[Document],
    index_name: str
) -> PineconeVectorStore:
    """
    Create embeddings and store in Pinecone vector database.
    
    Args:
        chunks: List of document chunks to embed
        index_name: Name of the Pinecone index
        
    Returns:
        PineconeVectorStore instance
    """
    print(f"🧠 Creating embeddings with Cohere...")
    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    
    print(f"📊 Storing {len(chunks)} chunks in Pinecone index '{index_name}'...")
    
    try:
        vectorstore = PineconeVectorStore.from_documents(
            chunks,
            embeddings,
            index_name=index_name
        )
        print(f"✅ Successfully stored all chunks in Pinecone!\n")
        return vectorstore
        
    except Exception as e:
        print(f"❌ Error storing in Pinecone: {e}")
        raise


def main():
    """Main ingestion pipeline."""
    print("=" * 70)
    print("LangChain Documentation Helper - Ingestion Pipeline")
    print("=" * 70 + "\n")
    
    # Get index name from environment
    index_name = os.getenv("INDEX_NAME")
    if not index_name:
        raise ValueError("INDEX_NAME not found in .env file")
    
    print(f"🎯 Target Pinecone Index: {index_name}\n")
    
    # Step 1: Load documents from multiple sources
    all_documents = []
    
    # Load local file (from Module 01)
    local_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "01-rag-basics",
        "mediumblog1.txt"
    )
    local_docs = load_local_documents(local_file)
    all_documents.extend(local_docs)
    
    # Load web documents
    web_docs = load_web_documents()
    all_documents.extend(web_docs)
    
    if not all_documents:
        print("❌ No documents loaded. Exiting...")
        return
    
    print(f"📚 Total documents loaded: {len(all_documents)}")
    print(f"   - Local: {len(local_docs)}")
    print(f"   - Web: {len(web_docs)}\n")
    
    # Step 2: Split documents into chunks
    chunks = split_documents(
        all_documents,
        chunk_size=1000,
        chunk_overlap=200  # Overlap for better context
    )
    
    # Step 3: Create embeddings and store
    vectorstore = create_embeddings_and_store(chunks, index_name)
    
    print("=" * 70)
    print("✨ Ingestion Complete!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   - Total documents processed: {len(all_documents)}")
    print(f"   - Total chunks created: {len(chunks)}")
    print(f"   - Stored in index: {index_name}")
    print(f"\n🚀 Ready to query! Run: streamlit run app.py")


if __name__ == "__main__":
    main()
