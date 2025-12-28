"""
Example Use Cases for Reflexion Agent

This module demonstrates cross-task learning with related tasks.
"""

from graph import graph, global_memory
from state import ReflexionState


def run_task(description: str, task: str, max_attempts: int = 5):
    """Run a single task."""
    print("\n" + "=" * 70)
    print(f"Task: {description}")
    print("=" * 70)
    print(f"\nDescription: {task}\n")
    
    # Get relevant lessons
    relevant_lessons = global_memory.get_relevant_lessons(task, limit=5)
    
    initial_state: ReflexionState = {
        "task": task,
        "solution": "",
        "validation_result": {},
        "reflection": "",
        "memory": relevant_lessons,
        "attempt": 0,
        "max_attempts": max_attempts,
        "success": False
    }
    
    final_state = graph.invoke(initial_state)
    
    print("\n" + "=" * 70)
    if final_state['success']:
        print("✅ SUCCESS")
    else:
        print("❌ FAILED")
    print("=" * 70)
    print(f"Attempts: {final_state['attempt']}/{final_state['max_attempts']}")
    
    return final_state


def main():
    """Run all examples demonstrating cross-task learning."""
    print("=" * 70)
    print("🧠 Reflexion Agent - Cross-Task Learning Demo")
    print("=" * 70)
    print("\nThis demo shows how the agent learns from failures")
    print("and applies lessons to new, related tasks.\n")
    
    # Clear memory for fresh start
    global_memory.clear()
    print("🗑️  Starting with empty memory\n")
    
    # Example Set 1: String Manipulation
    print("\n" + "🔤 " * 20)
    print("EXAMPLE SET 1: String Manipulation Tasks")
    print("🔤 " * 20)
    
    run_task(
        "Reverse a String",
        "Write a function to reverse a string",
        max_attempts=3
    )
    
    run_task(
        "Check Palindrome",
        "Write a function to check if a string is a palindrome",
        max_attempts=3
    )
    
    run_task(
        "Count Vowels",
        "Write a function to count vowels in a string",
        max_attempts=3
    )
    
    # Show learning progress
    print("\n" + "=" * 70)
    print("📊 LEARNING PROGRESS - String Tasks")
    print("=" * 70)
    
    stats = global_memory.get_stats()
    print(f"\nTotal memories: {stats['total_memories']}")
    print(f"Successes: {stats['successes']}")
    print(f"Failures: {stats['failures']}")
    print(f"Success rate: {stats['success_rate']:.1%}")
    
    print("\n💡 Key Lessons Learned:")
    for i, lesson in enumerate(global_memory.get_all_lessons()[-3:], 1):
        print(f"\n{i}. {lesson[:150]}...")
    
    # Example Set 2: Show that lessons transfer
    print("\n\n" + "🔄 " * 20)
    print("EXAMPLE SET 2: Applying Learned Patterns")
    print("🔄 " * 20)
    print("\nThese tasks should succeed faster due to learned lessons!\n")
    
    run_task(
        "Remove Whitespace",
        "Write a function to remove all whitespace from a string",
        max_attempts=3
    )
    
    # Final stats
    print("\n" + "=" * 70)
    print("📊 FINAL STATISTICS")
    print("=" * 70)
    
    stats = global_memory.get_stats()
    print(f"\nTotal memories: {stats['total_memories']}")
    print(f"Successes: {stats['successes']}")
    print(f"Failures: {stats['failures']}")
    print(f"Success rate: {stats['success_rate']:.1%}")
    
    print("\n💡 All Lessons Learned:")
    for i, lesson in enumerate(global_memory.get_all_lessons(), 1):
        print(f"\n{i}. {lesson}")
    
    print("\n" + "=" * 70)
    print("✅ Demo completed!")
    print("=" * 70)
    print("\nKey Takeaway: The agent learned from early failures")
    print("and applied those lessons to succeed faster on later tasks!")


if __name__ == "__main__":
    main()
