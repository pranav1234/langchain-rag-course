"""
Main CLI Interface for Reflexion Agent

This module provides an interactive command-line interface
for running the Reflexion agent with cross-task learning.
"""

from graph import graph, global_memory
from state import ReflexionState


def run_reflexion_agent(
    task: str,
    max_attempts: int = 5
) -> ReflexionState:
    """
    Run the Reflexion agent on a task.
    
    Args:
        task: Task description
        max_attempts: Maximum number of attempts
        
    Returns:
        Final state with solution
    """
    # Get relevant lessons from global memory
    relevant_lessons = global_memory.get_relevant_lessons(task, limit=5)
    
    # Initialize state
    initial_state: ReflexionState = {
        "task": task,
        "solution": "",
        "validation_result": {},
        "reflection": "",
        "memory": relevant_lessons,  # Start with past lessons!
        "attempt": 0,
        "max_attempts": max_attempts,
        "success": False
    }
    
    # Run the graph
    final_state = graph.invoke(initial_state)
    
    return final_state


def main():
    """Main CLI loop."""
    print("=" * 70)
    print("🧠 LangGraph Reflexion Agent")
    print("=" * 70)
    print("\nThis agent learns from past failures and applies lessons to new tasks!")
    print("Try multiple related tasks to see cross-task learning in action.\n")
    
    # Show memory stats
    stats = global_memory.get_stats()
    print(f"📊 Memory: {stats['total_memories']} memories ({stats['successes']} successes)")
    print()
    
    task_count = 0
    
    while True:
        try:
            # Get user input
            print("-" * 70)
            task = input("\n📝 Enter a task (or 'quit' to exit):\n> ").strip()
            
            if not task:
                print("⚠️  Please enter a task.")
                continue
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Special commands
            if task.lower() == 'stats':
                stats = global_memory.get_stats()
                print("\n📊 Memory Statistics:")
                print(f"   Total memories: {stats['total_memories']}")
                print(f"   Successes: {stats['successes']}")
                print(f"   Failures: {stats['failures']}")
                print(f"   Success rate: {stats['success_rate']:.1%}")
                continue
            
            if task.lower() == 'lessons':
                lessons = global_memory.get_all_lessons()
                print("\n💡 All Lessons Learned:")
                for i, lesson in enumerate(lessons, 1):
                    print(f"\n{i}. {lesson}")
                continue
            
            if task.lower() == 'clear':
                global_memory.clear()
                print("\n🗑️  Memory cleared!")
                continue
            
            # Get max attempts
            try:
                max_attempts_input = input("\n🔢 Max attempts (default 5): ").strip()
                max_attempts = int(max_attempts_input) if max_attempts_input else 5
                max_attempts = max(1, min(max_attempts, 10))  # Clamp 1-10
            except ValueError:
                max_attempts = 5
                print("Using default: 5 attempts")
            
            # Run Reflexion agent
            task_count += 1
            print(f"\n🚀 Starting task #{task_count}: {task}")
            
            final_state = run_reflexion_agent(task, max_attempts)
            
            # Display final result
            print("\n" + "=" * 70)
            if final_state['success']:
                print("✅ TASK COMPLETED SUCCESSFULLY!")
            else:
                print("❌ TASK FAILED (Max attempts reached)")
            print("=" * 70)
            
            if final_state['success']:
                print(f"\nFinal Solution:\n{final_state['solution']}\n")
            
            print(f"📊 Statistics:")
            print(f"   - Total attempts: {final_state['attempt']}")
            print(f"   - Max attempts: {final_state['max_attempts']}")
            print(f"   - Lessons learned this task: {len(final_state['memory']) - len(global_memory.get_relevant_lessons(task, limit=5))}")
            
            # Show updated memory stats
            stats = global_memory.get_stats()
            print(f"\n📚 Global Memory:")
            print(f"   - Total memories: {stats['total_memories']}")
            print(f"   - Success rate: {stats['success_rate']:.1%}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
