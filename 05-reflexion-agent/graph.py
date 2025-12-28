"""
LangGraph Workflow for Reflexion Agent

This module builds the graph structure with episodic memory
and external validation for learning across tasks.
"""

from langgraph.graph import StateGraph, END
from state import ReflexionState
from chains import generate_solution, reflect_on_failure
from validators import validate_code
from memory import EpisodicMemory

# Global memory instance
global_memory = EpisodicMemory()


def generate_node(state: ReflexionState) -> ReflexionState:
    """
    Generation node: Creates solution using past lessons.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with new solution
    """
    print(f"\n{'='*70}")
    print(f"ATTEMPT {state['attempt'] + 1}")
    print(f"{'='*70}")
    
    print(f"📝 Generating solution...")
    if state['memory']:
        print(f"💡 Using {len(state['memory'])} past lessons")
    
    # Generate solution using memory
    solution = generate_solution(state["task"], state["memory"])
    
    # Update state
    state["solution"] = solution
    state["attempt"] += 1
    
    print(f"\nSolution:\n{solution}")
    
    return state


def validate_node(state: ReflexionState) -> ReflexionState:
    """
    Validation node: Runs external tests on solution.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with validation results
    """
    print(f"\n🧪 Running validation tests...")
    
    # Extract test cases from task (simplified)
    # In production, tests would be provided separately
    tests = get_tests_for_task(state["task"])
    
    # Validate the solution
    result = validate_code(state["solution"], tests)
    
    state["validation_result"] = result
    state["success"] = result["success"]
    
    if result["success"]:
        print(f"✅ All tests passed! ({result['passed_tests']}/{result['total_tests']})")
    else:
        print(f"❌ Tests failed: {result['passed_tests']}/{result['total_tests']}")
        print(f"Error: {result['error']}")
    
    return state


def reflect_node(state: ReflexionState) -> ReflexionState:
    """
    Reflection node: Analyzes failure and stores lesson.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with reflection
    """
    print(f"\n🤔 Reflecting on failure...")
    
    error = state["validation_result"].get("error", "Unknown error")
    
    # Generate reflection
    reflection = reflect_on_failure(
        state["task"],
        state["solution"],
        error
    )
    
    state["reflection"] = reflection
    
    # Add to memory for next attempt
    state["memory"].append(reflection)
    
    # Store in global memory
    global_memory.add_lesson(
        task=state["task"],
        solution=state["solution"],
        error=error,
        lesson=reflection,
        success=False
    )
    
    print(f"\n💡 Lesson Learned:\n{reflection}")
    
    return state


def success_node(state: ReflexionState) -> ReflexionState:
    """
    Success node: Stores successful pattern.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state
    """
    print(f"\n🎉 Success! Storing successful pattern...")
    
    # Store success in global memory
    global_memory.add_lesson(
        task=state["task"],
        solution=state["solution"],
        error="",
        lesson=f"Successful approach for: {state['task']}",
        success=True
    )
    
    return state


def check_validation(state: ReflexionState) -> str:
    """
    Decision function: Check if validation passed.
    
    Args:
        state: Current workflow state
        
    Returns:
        "success" if passed, "failure" if failed
    """
    return "success" if state["success"] else "failure"


def should_retry(state: ReflexionState) -> str:
    """
    Decision function: Determine if we should retry.
    
    Args:
        state: Current workflow state
        
    Returns:
        "retry" to try again, "give_up" to stop
    """
    if state["attempt"] >= state["max_attempts"]:
        print(f"\n{'='*70}")
        print(f"❌ Reached max attempts ({state['max_attempts']})")
        print(f"{'='*70}")
        return "give_up"
    else:
        print(f"\n🔄 Retrying with new lesson (attempt {state['attempt'] + 1})...")
        return "retry"


def get_tests_for_task(task: str) -> list:
    """
    Get test cases for a task.
    
    In production, tests would be provided separately.
    This is a simplified version for demo purposes.
    
    Args:
        task: Task description
        
    Returns:
        List of test cases
    """
    # Simple keyword matching for demo
    task_lower = task.lower()
    
    if "reverse" in task_lower:
        return [
            {"input": "hello", "expected": "olleh"},
            {"input": "", "expected": ""},
            {"input": "a", "expected": "a"},
            {"input": "racecar", "expected": "racecar"}
        ]
    elif "palindrome" in task_lower:
        return [
            {"input": "racecar", "expected": True},
            {"input": "hello", "expected": False},
            {"input": "", "expected": True},
            {"input": "a", "expected": True}
        ]
    elif "vowel" in task_lower:
        return [
            {"input": "hello", "expected": 2},
            {"input": "", "expected": 0},
            {"input": "aeiou", "expected": 5},
            {"input": "xyz", "expected": 0}
        ]
    else:
        # Default tests
        return [
            {"input": "test", "expected": "test"}
        ]


# Build the graph
def create_graph():
    """
    Create and compile the Reflexion agent graph.
    
    Returns:
        Compiled LangGraph application
    """
    # Create graph
    workflow = StateGraph(ReflexionState)
    
    # Add nodes
    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("reflect", reflect_node)
    workflow.add_node("success", success_node)
    
    # Set entry point
    workflow.set_entry_point("generate")
    
    # Add edges
    # Always validate after generating
    workflow.add_edge("generate", "validate")
    
    # Conditional edge after validation
    workflow.add_conditional_edges(
        "validate",
        check_validation,
        {
            "success": "success",  # Store success pattern
            "failure": "reflect"   # Analyze failure
        }
    )
    
    # Success leads to end
    workflow.add_edge("success", END)
    
    # Conditional edge after reflection
    workflow.add_conditional_edges(
        "reflect",
        should_retry,
        {
            "retry": "generate",  # Try again with new lesson
            "give_up": END        # Stop trying
        }
    )
    
    # Compile
    app = workflow.compile()
    
    return app


# Create the graph instance
graph = create_graph()


if __name__ == "__main__":
    """Demo: Visualize the graph structure"""
    print("=" * 70)
    print("Reflexion Agent Graph Structure")
    print("=" * 70 + "\n")
    
    print("Nodes:")
    print("  1. generate - Creates solution using past lessons")
    print("  2. validate - Runs external tests")
    print("  3. reflect - Analyzes failure, stores lesson")
    print("  4. success - Stores successful pattern")
    
    print("\nEdges:")
    print("  - Entry: generate (start here)")
    print("  - generate → validate (always)")
    print("  - validate → success (if tests pass)")
    print("  - validate → reflect (if tests fail)")
    print("  - success → END")
    print("  - reflect → generate (if attempts remain)")
    print("  - reflect → END (if max attempts reached)")
    
    print("\nFlow:")
    print("  Start → Generate → Validate")
    print("                       ↓")
    print("           Success? → Yes → Store Success → END")
    print("                ↓ No")
    print("              Reflect → Store Lesson")
    print("                ↓")
    print("        Attempts left? → Yes → Generate (with new lesson)")
    print("                ↓ No")
    print("               END")
    
    print("\n" + "=" * 70)
    print("Graph created successfully!")
    print("Run 'python main.py' to use the Reflexion agent.")
    print("=" * 70)
