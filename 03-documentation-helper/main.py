"""
Main Query Engine with Conversational Memory

This module provides a CLI interface for querying the documentation
with conversational memory support.
"""

import os
from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore

from memory import ConversationMemoryManager

load_dotenv()


def create_retrieval_chain_with_memory(
    vectorstore: PineconeVectorStore,
    llm: ChatGoogleGenerativeAI,
    memory: ConversationMemoryManager
):
    """
    Create a retrieval chain with conversational memory.
    
    Args:
        vectorstore: Pinecone vector store
        llm: Language model
        memory: Conversation memory manager
        
    Returns:
        Configured retrieval chain
    """
    # Get the retrieval QA prompt
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    
    # Create document chain
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    
    # Create retrieval chain
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        combine_docs_chain=combine_docs_chain
    )
    
    return retrieval_chain


def format_response(result: dict) -> str:
    """
    Format the response with answer and sources.
    
    Args:
        result: Result dictionary from retrieval chain
        
    Returns:
        Formatted response string
    """
    answer = result.get("answer", "No answer found.")
    context = result.get("context", [])
    
    response = f"\n{'='*70}\n"
    response += "ANSWER:\n"
    response += f"{'='*70}\n"
    response += f"{answer}\n"
    
    if context:
        response += f"\n{'='*70}\n"
        response += "SOURCES:\n"
        response += f"{'='*70}\n"
        
        seen_sources = set()
        for i, doc in enumerate(context, 1):
            source = doc.metadata.get("source", "Unknown")
            title = doc.metadata.get("title", "")
            
            # Avoid duplicate sources
            if source not in seen_sources:
                seen_sources.add(source)
                if title:
                    response += f"{i}. {title}\n   {source}\n\n"
                else:
                    response += f"{i}. {source}\n\n"
    
    return response


def main():
    """Main CLI query loop with conversational memory."""
    print("=" * 70)
    print("LangChain Documentation Helper - CLI Version")
    print("=" * 70)
    print("\nInitializing system...\n")
    
    # Initialize components
    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    
    index_name = os.getenv("INDEX_NAME")
    if not index_name:
        raise ValueError("INDEX_NAME not found in .env file")
    
    print(f"📊 Connecting to Pinecone index: {index_name}")
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    
    # Initialize memory
    memory = ConversationMemoryManager(max_history=5)
    
    # Create retrieval chain
    retrieval_chain = create_retrieval_chain_with_memory(vectorstore, llm, memory)
    
    print("✅ System ready!\n")
    print("=" * 70)
    print("Ask questions about LangChain documentation")
    print("Type 'quit' to exit, 'clear' to clear conversation history")
    print("=" * 70 + "\n")
    
    # Query loop
    while True:
        try:
            # Get user input
            query = input("\n🤔 Your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == 'clear':
                memory.clear()
                print("🧹 Conversation history cleared!")
                continue
            
            # Add to memory
            memory.add_user_message(query)
            
            # Get conversation history as list of messages
            chat_history = []
            history = memory.get_chat_history()
            for msg in history[:-1]:  # Exclude current message
                if msg["role"] == "user":
                    chat_history.append(HumanMessage(content=msg["content"]))
                else:
                    chat_history.append(AIMessage(content=msg["content"]))
            
            # Query the system
            print("\n🔍 Searching documentation...")
            result = retrieval_chain.invoke({
                "input": query,
                "chat_history": chat_history
            })
            
            # Add response to memory
            answer = result.get("answer", "")
            memory.add_ai_message(answer)
            
            # Display formatted response
            print(format_response(result))
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()
