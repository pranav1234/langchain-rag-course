"""
Prompt Chains for Reflexion Agent

This module defines the LLM chains for generation with memory
and reflection with failure analysis.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.7)


# Generation Prompt (with memory)
GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert problem solver. Generate a solution to the task.

IMPORTANT: Learn from past experiences!

Past Lessons Learned:
{memory}

Apply these lessons to avoid repeating past mistakes.

Guidelines:
- Write clean, correct code
- Handle edge cases (empty input, None, etc.)
- Include proper error handling
- Follow best practices"""),
    ("user", "Task: {task}\n\nGenerate a Python function to solve this task.")
])

# Reflection Prompt (analyzes failures)
REFLECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert code reviewer analyzing why a solution failed.

Provide a specific, actionable lesson that can be applied to future tasks.

Focus on:
- What went wrong
- Why it failed
- How to avoid this in the future
- General principles that apply beyond this specific task"""),
    ("user", """Task: {task}

Your Solution:
{solution}

Validation Error:
{error}

Analyze this failure and extract ONE specific lesson to remember.""")
])


# Create chains
generation_chain = GENERATION_PROMPT | llm
reflection_chain = REFLECTION_PROMPT | llm


def generate_solution(task: str, memory: list) -> str:
    """
    Generate a solution using past lessons.
    
    Args:
        task: Task description
        memory: List of past lessons
        
    Returns:
        Generated solution code
    """
    memory_text = "\n".join(f"- {lesson}" for lesson in memory) if memory else "No past lessons yet."
    
    result = generation_chain.invoke({
        "task": task,
        "memory": memory_text
    })
    return result.content


def reflect_on_failure(task: str, solution: str, error: str) -> str:
    """
    Analyze failure and extract lesson.
    
    Args:
        task: Task description
        solution: Failed solution
        error: Error message
        
    Returns:
        Lesson learned
    """
    result = reflection_chain.invoke({
        "task": task,
        "solution": solution,
        "error": error
    })
    return result.content


if __name__ == "__main__":
    """Demo: Test the chains"""
    print("=" * 70)
    print("Chains Demo")
    print("=" * 70 + "\n")
    
    # Test generation with no memory
    print("1. GENERATION (No Memory)")
    print("-" * 70)
    task = "Write a function to reverse a string"
    solution = generate_solution(task, [])
    print(f"Task: {task}")
    print(f"Solution:\n{solution}\n")
    
    # Simulate a failure
    print("2. REFLECTION (After Failure)")
    print("-" * 70)
    error = "Failed on empty string input - returned error instead of empty string"
    reflection = reflect_on_failure(task, solution, error)
    print(f"Error: {error}")
    print(f"Lesson Learned:\n{reflection}\n")
    
    # Test generation with memory
    print("3. GENERATION (With Memory)")
    print("-" * 70)
    task2 = "Write a function to check if a string is a palindrome"
    memory = [reflection]
    solution2 = generate_solution(task2, memory)
    print(f"Task: {task2}")
    print(f"Memory: {memory[0][:100]}...")
    print(f"Solution:\n{solution2}\n")
