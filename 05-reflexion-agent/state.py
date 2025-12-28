"""
State Definition for Reflexion Agent

This module defines the state structure with episodic memory
for the Reflexion workflow in LangGraph.
"""

from typing import TypedDict, List


class ReflexionState(TypedDict):
    """
    State for the Reflexion agent workflow.
    
    This state includes episodic memory that persists lessons
    learned from past failures, enabling cross-task learning.
    """
    
    # Current task description
    task: str
    
    # Current solution attempt
    solution: str
    
    # Validation results from external checks
    validation_result: dict
    
    # Reflection/analysis of failure
    reflection: str
    
    # Episodic memory: lessons learned from past attempts
    memory: List[str]
    
    # Current attempt number (starts at 0)
    attempt: int
    
    # Maximum attempts allowed
    max_attempts: int
    
    # Whether the task succeeded
    success: bool
