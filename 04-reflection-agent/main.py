"""
Main CLI Interface for Reflection Agent

This module provides an interactive command-line interface
for running the reflection agent.
"""

from graph import graph
from state import ReflectionState


def run_reflection_agent(
    user_input: str,
    max_iterations: int = 3
) -> ReflectionState:
    """
    Run the reflection agent on user input.
    
    Args:
        user_input: User's content request
        max_iterations: Maximum number of refinement iterations
        
    Returns:
        Final state with polished content
    """
    # Initialize state
    initial_state: ReflectionState = {
        "input": user_input,
        "draft": "",
        "reflection": "",
        "iteration": 0,
        "max_iterations": max_iterations
    }
    
    # Run the graph
    final_state = graph.invoke(initial_state)
    
    return final_state


def main():
    """Main CLI loop."""
    print("=" * 70)
    print("🦜 LangGraph Reflection Agent")
    print("=" * 70)
    print("\nThis agent improves content through iterative reflection.")
    print("It will generate, reflect, and refine your content multiple times.\n")
    
    while True:
        try:
            # Get user input
            print("-" * 70)
            user_input = input("\n📝 Enter your content request (or 'quit' to exit):\n> ").strip()
            
            if not user_input:
                print("⚠️  Please enter a request.")
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Get max iterations
            try:
                max_iter_input = input("\n🔢 Max iterations (default 3): ").strip()
                max_iterations = int(max_iter_input) if max_iter_input else 3
                max_iterations = max(1, min(max_iterations, 10))  # Clamp between 1-10
            except ValueError:
                max_iterations = 3
                print("Using default: 3 iterations")
            
            # Run reflection agent
            print(f"\n🚀 Starting reflection process with {max_iterations} max iterations...")
            
            final_state = run_reflection_agent(user_input, max_iterations)
            
            # Display final result
            print("\n" + "=" * 70)
            print("✨ FINAL POLISHED CONTENT")
            print("=" * 70)
            print(f"\n{final_state['draft']}\n")
            
            print(f"📊 Statistics:")
            print(f"   - Total iterations: {final_state['iteration']}")
            print(f"   - Max iterations: {final_state['max_iterations']}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()
