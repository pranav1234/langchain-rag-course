"""
LangGraph Workflow for Reflection Agent

This module builds the graph structure with nodes and edges
for the iterative reflection process.
"""

from langgraph.graph import StateGraph, END
from state import ReflectionState
from chains import generate_content, refine_content, reflect_on_content


def generate_node(state: ReflectionState) -> ReflectionState:
    """
    Generation node: Creates or refines content.
    
    On first iteration: Generates initial content
    On subsequent iterations: Refines based on reflection
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with new draft
    """
    print(f"\n{'='*70}")
    print(f"ITERATION {state['iteration'] + 1}")
    print(f"{'='*70}")
    
    if state["iteration"] == 0:
        # First iteration: generate initial content
        print("📝 Generating initial content...")
        draft = generate_content(state["input"])
    else:
        # Subsequent iterations: refine based on reflection
        print("✨ Refining based on feedback...")
        draft = refine_content(state["draft"], state["reflection"])
    
    # Update state
    state["draft"] = draft
    state["iteration"] += 1
    
    print(f"\nDraft:\n{draft}")
    
    return state


def reflect_node(state: ReflectionState) -> ReflectionState:
    """
    Reflection node: Critiques the current draft.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with reflection
    """
    print(f"\n🤔 Reflecting on content...")
    
    reflection = reflect_on_content(state["draft"])
    state["reflection"] = reflection
    
    print(f"\nReflection:\n{reflection}")
    
    return state


def should_continue(state: ReflectionState) -> str:
    """
    Decision function: Determines if we should continue iterating.
    
    Args:
        state: Current workflow state
        
    Returns:
        "continue" to loop back to generate, "end" to finish
    """
    if state["iteration"] >= state["max_iterations"]:
        print(f"\n{'='*70}")
        print(f"✅ Reached max iterations ({state['max_iterations']})")
        print(f"{'='*70}")
        return "end"
    else:
        print(f"\n🔄 Continuing to iteration {state['iteration'] + 1}...")
        return "continue"


# Build the graph
def create_graph():
    """
    Create and compile the reflection agent graph.
    
    Returns:
        Compiled LangGraph application
    """
    # Create graph
    workflow = StateGraph(ReflectionState)
    
    # Add nodes
    workflow.add_node("generate", generate_node)
    workflow.add_node("reflect", reflect_node)
    
    # Set entry point
    workflow.set_entry_point("generate")
    
    # Add edges
    # Always reflect after generating
    workflow.add_edge("generate", "reflect")
    
    # Conditional edge: continue or end
    workflow.add_conditional_edges(
        "reflect",
        should_continue,
        {
            "continue": "generate",  # Loop back to generate
            "end": END               # Finish workflow
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
    print("Reflection Agent Graph Structure")
    print("=" * 70 + "\n")
    
    print("Nodes:")
    print("  1. generate - Creates or refines content")
    print("  2. reflect - Provides critique and feedback")
    
    print("\nEdges:")
    print("  - Entry: generate (start here)")
    print("  - generate → reflect (always)")
    print("  - reflect → generate (if iteration < max_iterations)")
    print("  - reflect → END (if iteration >= max_iterations)")
    
    print("\nFlow:")
    print("  Start → Generate → Reflect → Continue? → Yes → Generate → ...")
    print("                                    ↓")
    print("                                   No")
    print("                                    ↓")
    print("                                   END")
    
    print("\n" + "=" * 70)
    print("Graph created successfully!")
    print("Run 'python main.py' to use the reflection agent.")
    print("=" * 70)
