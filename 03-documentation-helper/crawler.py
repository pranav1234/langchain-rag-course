"""
Web Crawler for LangChain Documentation

This module uses Tavily to intelligently crawl and extract content from
LangChain documentation websites. It handles URL fetching, content extraction,
and preprocessing for the RAG pipeline.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


class LangChainDocCrawler:
    """Crawls LangChain documentation using Tavily API."""
    
    def __init__(self):
        """Initialize the Tavily client with API key from environment."""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY not found in environment. "
                "Get your free API key at https://tavily.com/"
            )
        self.client = TavilyClient(api_key=api_key)
    
    def search_langchain_docs(
        self, 
        query: str = "LangChain documentation", 
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for LangChain documentation using Tavily.
        
        Args:
            query: Search query to find relevant documentation
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing URL, title, and content
        """
        print(f"🔍 Searching for: {query}")
        
        try:
            # Search with Tavily - focuses on LangChain official docs
            response = self.client.search(
                query=query,
                search_depth="advanced",  # More thorough search
                max_results=max_results,
                include_domains=["python.langchain.com", "docs.langchain.com"],
            )
            
            documents = []
            for result in response.get("results", []):
                doc = {
                    "url": result.get("url", ""),
                    "title": result.get("title", "Untitled"),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0),
                }
                documents.append(doc)
                print(f"  ✅ Found: {doc['title'][:60]}...")
            
            print(f"📚 Retrieved {len(documents)} documents\n")
            return documents
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return []
    
    def crawl_specific_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Crawl specific URLs directly.
        
        Args:
            urls: List of URLs to crawl
            
        Returns:
            List of dictionaries containing URL, title, and content
        """
        print(f"🌐 Crawling {len(urls)} specific URLs...")
        
        documents = []
        for url in urls:
            try:
                # Extract content from URL
                response = self.client.extract(urls=[url])
                
                for result in response.get("results", []):
                    doc = {
                        "url": result.get("url", url),
                        "title": result.get("title", "Untitled"),
                        "content": result.get("raw_content", ""),
                    }
                    documents.append(doc)
                    print(f"  ✅ Crawled: {url}")
                    
            except Exception as e:
                print(f"  ❌ Failed to crawl {url}: {e}")
                continue
        
        print(f"📚 Successfully crawled {len(documents)} URLs\n")
        return documents
    
    def get_langchain_basics(self) -> List[Dict[str, Any]]:
        """
        Get essential LangChain documentation covering core concepts.
        
        Returns:
            List of documents about LangChain basics
        """
        queries = [
            "LangChain getting started tutorial",
            "LangChain chains and LCEL",
            "LangChain retrieval and RAG",
            "LangChain agents and tools",
            "LangChain memory and conversation",
        ]
        
        all_documents = []
        for query in queries:
            docs = self.search_langchain_docs(query, max_results=3)
            all_documents.extend(docs)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_docs = []
        for doc in all_documents:
            if doc["url"] not in seen_urls:
                seen_urls.add(doc["url"])
                unique_docs.append(doc)
        
        return unique_docs


def main():
    """Demo: Crawl LangChain documentation."""
    print("=" * 60)
    print("LangChain Documentation Crawler Demo")
    print("=" * 60 + "\n")
    
    crawler = LangChainDocCrawler()
    
    # Method 1: Search-based crawling
    print("Method 1: Search-based crawling")
    print("-" * 60)
    documents = crawler.search_langchain_docs(
        query="LangChain RAG retrieval tutorial",
        max_results=3
    )
    
    # Display results
    for i, doc in enumerate(documents, 1):
        print(f"\n📄 Document {i}:")
        print(f"   Title: {doc['title']}")
        print(f"   URL: {doc['url']}")
        print(f"   Content Preview: {doc['content'][:200]}...")
        print(f"   Score: {doc.get('score', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("Method 2: Get LangChain basics (multiple queries)")
    print("=" * 60 + "\n")
    
    basics_docs = crawler.get_langchain_basics()
    print(f"\n✅ Total unique documents retrieved: {len(basics_docs)}")
    
    # Show summary
    print("\n📋 Summary of retrieved documentation:")
    for i, doc in enumerate(basics_docs[:10], 1):  # Show first 10
        print(f"   {i}. {doc['title'][:70]}")


if __name__ == "__main__":
    main()
