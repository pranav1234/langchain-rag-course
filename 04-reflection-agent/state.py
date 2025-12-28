"""
State Definition for Reflection Agent

This module defines the state structure that flows through the
reflection workflow in LangGraph.
"""

from typing import TypedDict


class ReflectionState(TypedDict):
    """
    State for the reflection agent workflow.
    
    This state is passed between nodes and tracks the entire
    reflection process from initial input to final polished output.
    """
    
    # User's original request
    input: str
    
    # Current draft of the content
    draft: str
    
    # Reflection/critique of the current draft
    reflection: str
    
    # Current iteration number (starts at 0)
    iteration: int
    
    # Maximum iterations allowed
    max_iterations: int
