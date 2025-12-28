"""
Example Use Cases for Reflection Agent

This module demonstrates various use cases for the reflection agent.
"""

from graph import graph
from state import ReflectionState


def run_example(description: str, user_input: str, max_iterations: int = 3):
    """Run a single example."""
    print("\n" + "=" * 70)
    print(f"Example: {description}")
    print("=" * 70)
    print(f"\nInput: {user_input}\n")
    
    initial_state: ReflectionState = {
        "input": user_input,
        "draft": "",
        "reflection": "",
        "iteration": 0,
        "max_iterations": max_iterations
    }
    
    final_state = graph.invoke(initial_state)
    
    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)
    print(f"\n{final_state['draft']}\n")


def main():
    """Run all examples."""
    print("=" * 70)
    print("🦜 Reflection Agent - Example Use Cases")
    print("=" * 70)
    
    # Example 1: Tweet Improvement
    run_example(
        "Tweet Improvement",
        """Make this tweet better:
        
@LangChainAI — newly Tool Calling feature is seriously underrated.
After a long wait, it's here- making the implementation of agents 
across different models with function calling - super easy.
Made a video covering their newest blog post""",
        max_iterations=3
    )
    
    # Example 2: Email Polish
    run_example(
        "Professional Email",
        """Make this email more professional:
        
Hey, just wanted to check if you got my last email about the project.
Let me know when you can. Thanks.""",
        max_iterations=2
    )
    
    # Example 3: Code Documentation
    run_example(
        "Code Documentation",
        """Improve this function docstring:
        
def process_data(data):
    # does stuff with data
    return result""",
        max_iterations=2
    )
    
    # Example 4: Blog Post Introduction
    run_example(
        "Blog Post Intro",
        """Write an engaging introduction for a blog post about LangGraph:
        
LangGraph is a new library for building stateful applications with LLMs.""",
        max_iterations=3
    )
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
