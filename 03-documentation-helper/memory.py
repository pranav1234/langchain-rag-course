"""
Conversational Memory System

This module implements conversation memory with context management
for multi-turn conversations in the documentation helper.
"""

from typing import List, Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage


class ConversationMemoryManager:
    """Manages conversation history and context for the documentation helper."""
    
    def __init__(self, max_history: int = 10):
        """
        Initialize conversation memory.
        
        Args:
            max_history: Maximum number of conversation turns to keep
        """
        self.max_history = max_history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"  # For retrieval chains
        )
    
    def add_user_message(self, message: str):
        """Add a user message to the conversation history."""
        self.memory.chat_memory.add_user_message(message)
    
    def add_ai_message(self, message: str):
        """Add an AI response to the conversation history."""
        self.memory.chat_memory.add_ai_message(message)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        Get formatted chat history.
        
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        messages = self.memory.chat_memory.messages
        
        # Limit to max_history most recent messages
        if len(messages) > self.max_history * 2:  # *2 because user+ai = 2 messages
            messages = messages[-(self.max_history * 2):]
        
        formatted_history = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted_history.append({
                    "role": "user",
                    "content": msg.content
                })
            elif isinstance(msg, AIMessage):
                formatted_history.append({
                    "role": "assistant",
                    "content": msg.content
                })
        
        return formatted_history
    
    def get_context_string(self) -> str:
        """
        Get conversation history as a formatted string for prompt context.
        
        Returns:
            Formatted string of conversation history
        """
        history = self.get_chat_history()
        
        if not history:
            return ""
        
        context_parts = []
        for msg in history:
            role = "Human" if msg["role"] == "user" else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def clear(self):
        """Clear all conversation history."""
        self.memory.clear()
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """Get memory variables for chain integration."""
        return self.memory.load_memory_variables({})


def create_memory_aware_prompt(base_prompt: str, include_history: bool = True) -> str:
    """
    Create a prompt template that includes conversation history.
    
    Args:
        base_prompt: Base prompt template
        include_history: Whether to include conversation history
        
    Returns:
        Enhanced prompt with history placeholder
    """
    if not include_history:
        return base_prompt
    
    history_section = """
Previous Conversation:
{chat_history}

Current Question: {input}
"""
    
    return base_prompt + "\n\n" + history_section


def main():
    """Demo: Conversation memory management."""
    print("=" * 60)
    print("Conversation Memory Demo")
    print("=" * 60 + "\n")
    
    # Create memory manager
    memory = ConversationMemoryManager(max_history=5)
    
    # Simulate a conversation
    conversations = [
        ("What is LangChain?", "LangChain is a framework for developing applications powered by language models."),
        ("How do I install it?", "You can install LangChain using pip: pip install langchain"),
        ("What about the vector stores?", "LangChain supports various vector stores like Pinecone, Chroma, and FAISS."),
        ("Show me an example", "Here's a simple example of using LangChain with a vector store..."),
    ]
    
    print("Simulating conversation:\n")
    for i, (user_msg, ai_msg) in enumerate(conversations, 1):
        print(f"Turn {i}:")
        print(f"  User: {user_msg}")
        print(f"  AI: {ai_msg}\n")
        
        memory.add_user_message(user_msg)
        memory.add_ai_message(ai_msg)
    
    # Display formatted history
    print("=" * 60)
    print("Formatted Chat History:")
    print("=" * 60 + "\n")
    
    history = memory.get_chat_history()
    for msg in history:
        role = msg["role"].upper()
        print(f"[{role}]: {msg['content']}\n")
    
    # Display context string
    print("=" * 60)
    print("Context String for Prompts:")
    print("=" * 60 + "\n")
    print(memory.get_context_string())
    
    # Test memory variables
    print("\n" + "=" * 60)
    print("Memory Variables:")
    print("=" * 60 + "\n")
    print(memory.get_memory_variables())


if __name__ == "__main__":
    main()
