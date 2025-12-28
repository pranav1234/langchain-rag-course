"""
Episodic Memory Manager for Reflexion Agent

This module manages the agent's episodic memory, storing lessons
learned from past failures and successes for future tasks.
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime


class EpisodicMemory:
    """
    Manages episodic memory for the Reflexion agent.
    
    Stores lessons learned from task attempts and provides
    retrieval mechanisms for relevant past experiences.
    """
    
    def __init__(self, memory_file: str = "reflexion_memory.json"):
        """
        Initialize episodic memory.
        
        Args:
            memory_file: Path to JSON file for persistent storage
        """
        self.memory_file = memory_file
        self.memories: List[Dict[str, Any]] = []
        self.load()
    
    def add_lesson(
        self,
        task: str,
        solution: str,
        error: str,
        lesson: str,
        success: bool = False
    ):
        """
        Add a new lesson to episodic memory.
        
        Args:
            task: The task description
            solution: The attempted solution
            error: Error message (if failed)
            lesson: Lesson learned from this attempt
            success: Whether the attempt succeeded
        """
        memory_entry = {
            "task": task,
            "solution": solution,
            "error": error,
            "lesson": lesson,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        self.memories.append(memory_entry)
        self.save()
    
    def get_all_lessons(self) -> List[str]:
        """
        Get all lessons from memory.
        
        Returns:
            List of lesson strings
        """
        return [m["lesson"] for m in self.memories]
    
    def get_relevant_lessons(self, task: str, limit: int = 5) -> List[str]:
        """
        Get lessons relevant to the current task.
        
        For simplicity, returns the most recent lessons.
        In production, you'd use semantic similarity.
        
        Args:
            task: Current task description
            limit: Maximum number of lessons to return
            
        Returns:
            List of relevant lesson strings
        """
        # Simple approach: return most recent lessons
        # In production: use embeddings for semantic search
        recent_lessons = self.get_all_lessons()[-limit:]
        return recent_lessons
    
    def get_success_patterns(self) -> List[Dict[str, Any]]:
        """
        Get patterns from successful attempts.
        
        Returns:
            List of successful memory entries
        """
        return [m for m in self.memories if m["success"]]
    
    def get_failure_patterns(self) -> List[Dict[str, Any]]:
        """
        Get patterns from failed attempts.
        
        Returns:
            List of failed memory entries
        """
        return [m for m in self.memories if not m["success"]]
    
    def save(self):
        """Save memory to disk."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump({"memories": self.memories}, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
    
    def load(self):
        """Load memory from disk."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.memories = data.get("memories", [])
                print(f"✅ Loaded {len(self.memories)} memories from {self.memory_file}")
            except Exception as e:
                print(f"Warning: Could not load memory: {e}")
                self.memories = []
        else:
            print(f"📝 Starting with empty memory (no {self.memory_file} found)")
            self.memories = []
    
    def clear(self):
        """Clear all memories."""
        self.memories = []
        self.save()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory stats
        """
        total = len(self.memories)
        successes = len(self.get_success_patterns())
        failures = len(self.get_failure_patterns())
        
        return {
            "total_memories": total,
            "successes": successes,
            "failures": failures,
            "success_rate": successes / total if total > 0 else 0
        }


if __name__ == "__main__":
    """Demo: Episodic memory management"""
    print("=" * 70)
    print("Episodic Memory Demo")
    print("=" * 70 + "\n")
    
    # Create memory manager
    memory = EpisodicMemory("demo_memory.json")
    
    # Add some lessons
    print("Adding lessons to memory...\n")
    
    memory.add_lesson(
        task="Reverse a string",
        solution="def reverse(s): return s[::-1]",
        error="Failed on empty string",
        lesson="Always check for empty input before processing",
        success=False
    )
    
    memory.add_lesson(
        task="Check palindrome",
        solution="def is_palindrome(s): if not s: return True; return s == s[::-1]",
        error="",
        lesson="Applied empty check from previous task - worked!",
        success=True
    )
    
    memory.add_lesson(
        task="Count vowels",
        solution="def count_vowels(s): if not s: return 0; ...",
        error="",
        lesson="Empty check pattern continues to work",
        success=True
    )
    
    # Display all lessons
    print("All Lessons Learned:")
    print("-" * 70)
    for i, lesson in enumerate(memory.get_all_lessons(), 1):
        print(f"{i}. {lesson}")
    
    # Display stats
    print("\n" + "=" * 70)
    print("Memory Statistics:")
    print("=" * 70)
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Display success patterns
    print("\n" + "=" * 70)
    print("Success Patterns:")
    print("=" * 70)
    for pattern in memory.get_success_patterns():
        print(f"\nTask: {pattern['task']}")
        print(f"Lesson: {pattern['lesson']}")
    
    print("\n✅ Memory saved to demo_memory.json")
