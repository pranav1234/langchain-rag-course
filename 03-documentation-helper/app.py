"""
Streamlit Web Interface for LangChain Documentation Helper

A chat-like interface similar to chat.langchain.com for querying
LangChain documentation with conversational memory.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LangChain Documentation Helper",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .source-title {
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize the RAG system components (cached for performance)."""
    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    
    index_name = os.getenv("INDEX_NAME")
    if not index_name:
        raise ValueError("INDEX_NAME not found in .env file")
    
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    
    # Create retrieval chain
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        combine_docs_chain=combine_docs_chain
    )
    
    return retrieval_chain


def format_sources(context):
    """Format source documents for display."""
    if not context:
        return None
    
    sources = []
    seen_urls = set()
    
    for doc in context:
        source = doc.metadata.get("source", "Unknown")
        title = doc.metadata.get("title", "")
        doc_type = doc.metadata.get("type", "local")
        
        # Avoid duplicates
        if source not in seen_urls:
            seen_urls.add(source)
            sources.append({
                "title": title if title else source,
                "url": source,
                "type": doc_type,
                "preview": doc.page_content[:200] + "..."
            })
    
    return sources


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🦜 LangChain Documentation Helper</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask questions about LangChain documentation</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This is an AI-powered documentation assistant that helps you find answers 
        in LangChain documentation using:
        
        - 🔍 **Semantic Search** with Pinecone
        - 🧠 **Conversational Memory** for context
        - 🌐 **Web Crawling** with Tavily
        - 🤖 **Gemini LLM** for answers
        """)
        
        st.divider()
        
        st.header("💡 Example Questions")
        example_questions = [
            "What is LangChain?",
            "How do I create a retrieval chain?",
            "What are LangChain agents?",
            "How does LCEL work?",
            "What is a vector store?",
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}", use_container_width=True):
                st.session_state.example_question = question
        
        st.divider()
        
        if st.button("🧹 Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        st.caption("Built with LangChain, Streamlit, and ❤️")
    
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize the system
    try:
        with st.spinner("🔄 Initializing system..."):
            retrieval_chain = initialize_system()
    except Exception as e:
        st.error(f"❌ Error initializing system: {e}")
        st.info("💡 Make sure you have run `python ingestion.py` first to populate the vector database.")
        st.stop()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 View Sources", expanded=False):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source['title']}**")
                        if source['type'] == 'web':
                            st.markdown(f"🔗 [{source['url']}]({source['url']})")
                        else:
                            st.markdown(f"📄 {source['url']}")
                        st.caption(source['preview'])
                        st.divider()
    
    # Handle example question from sidebar
    if "example_question" in st.session_state:
        user_input = st.session_state.example_question
        del st.session_state.example_question
    else:
        # Chat input
        user_input = st.chat_input("Ask a question about LangChain...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Build chat history as list of message objects
                    chat_history = []
                    for msg in st.session_state.messages[:-1]:  # Exclude current message
                        if msg["role"] == "user":
                            chat_history.append(HumanMessage(content=msg["content"]))
                        else:
                            chat_history.append(AIMessage(content=msg["content"]))
                    
                    # Query the system
                    result = retrieval_chain.invoke({
                        "input": user_input,
                        "chat_history": chat_history
                    })
                    
                    answer = result.get("answer", "I couldn't find an answer to that question.")
                    context = result.get("context", [])
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Format and display sources
                    sources = format_sources(context)
                    
                    if sources:
                        with st.expander("📚 View Sources", expanded=False):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**{i}. {source['title']}**")
                                if source['type'] == 'web':
                                    st.markdown(f"🔗 [{source['url']}]({source['url']})")
                                else:
                                    st.markdown(f"📄 {source['url']}")
                                st.caption(source['preview'])
                                st.divider()
                    
                    # Add assistant message to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources if sources else []
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })


if __name__ == "__main__":
    main()
