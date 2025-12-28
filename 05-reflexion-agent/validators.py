"""
External Validators for Reflexion Agent

This module provides validation mechanisms to objectively
evaluate solutions with actual tests and rules.
"""

import sys
import io
from typing import List, Dict, Any
import traceback


def validate_code(code: str, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate Python code by running test cases.
    
    Args:
        code: Python code to validate
        tests: List of test cases with 'input' and 'expected' keys
        
    Returns:
        Dictionary with validation results
    """
    try:
        # Create a namespace for execution
        namespace = {}
        
        # Execute the code
        exec(code, namespace)
        
        # Find the function (assume first function defined)
        func_name = None
        for name, obj in namespace.items():
            if callable(obj) and not name.startswith('_'):
                func_name = name
                break
        
        if not func_name:
            return {
                "success": False,
                "error": "No function found in code",
                "passed_tests": 0,
                "total_tests": len(tests),
                "details": []
            }
        
        func = namespace[func_name]
        
        # Run tests
        passed = 0
        details = []
        
        for i, test in enumerate(tests):
            try:
                test_input = test.get("input")
                expected = test.get("expected")
                
                # Handle different input types
                if isinstance(test_input, (list, tuple)):
                    result = func(*test_input)
                else:
                    result = func(test_input)
                
                if result == expected:
                    passed += 1
                    details.append({
                        "test": i + 1,
                        "passed": True,
                        "input": test_input,
                        "expected": expected,
                        "got": result
                    })
                else:
                    details.append({
                        "test": i + 1,
                        "passed": False,
                        "input": test_input,
                        "expected": expected,
                        "got": result,
                        "error": f"Expected {expected}, got {result}"
                    })
            except Exception as e:
                details.append({
                    "test": i + 1,
                    "passed": False,
                    "input": test_input,
                    "error": str(e)
                })
        
        success = passed == len(tests)
        error = "" if success else f"Passed {passed}/{len(tests)} tests"
        
        return {
            "success": success,
            "error": error,
            "passed_tests": passed,
            "total_tests": len(tests),
            "details": details
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Code execution error: {str(e)}\n{traceback.format_exc()}",
            "passed_tests": 0,
            "total_tests": len(tests),
            "details": []
        }


def validate_logic(solution: str, rules: List[str]) -> Dict[str, Any]:
    """
    Validate solution against logical rules.
    
    Args:
        solution: Solution text to validate
        rules: List of rules that must be satisfied
        
    Returns:
        Dictionary with validation results
    """
    violations = []
    
    for rule in rules:
        # Simple keyword-based validation
        # In production, use more sophisticated NLP
        if rule.lower() not in solution.lower():
            violations.append(f"Missing: {rule}")
    
    success = len(violations) == 0
    error = "; ".join(violations) if violations else ""
    
    return {
        "success": success,
        "error": error,
        "rules_checked": len(rules),
        "violations": violations
    }


def validate_format(output: str, expected_format: str) -> Dict[str, Any]:
    """
    Validate output format.
    
    Args:
        output: Output to validate
        expected_format: Expected format description
        
    Returns:
        Dictionary with validation results
    """
    # Simple format validation
    # In production, use regex or schema validation
    
    format_checks = {
        "json": lambda s: s.strip().startswith('{') and s.strip().endswith('}'),
        "list": lambda s: s.strip().startswith('[') and s.strip().endswith(']'),
        "number": lambda s: s.strip().replace('.', '').replace('-', '').isdigit(),
        "text": lambda s: len(s.strip()) > 0
    }
    
    check_func = format_checks.get(expected_format.lower(), lambda s: True)
    success = check_func(output)
    error = "" if success else f"Output does not match expected format: {expected_format}"
    
    return {
        "success": success,
        "error": error,
        "expected_format": expected_format
    }


if __name__ == "__main__":
    """Demo: Validators"""
    print("=" * 70)
    print("Validators Demo")
    print("=" * 70 + "\n")
    
    # Test 1: Code Validator
    print("1. CODE VALIDATOR")
    print("-" * 70)
    
    code = """
def reverse(s):
    if not s:
        return ""
    return s[::-1]
"""
    
    tests = [
        {"input": "hello", "expected": "olleh"},
        {"input": "", "expected": ""},
        {"input": "a", "expected": "a"},
        {"input": "racecar", "expected": "racecar"}
    ]
    
    result = validate_code(code, tests)
    print(f"Success: {result['success']}")
    print(f"Passed: {result['passed_tests']}/{result['total_tests']}")
    if not result['success']:
        print(f"Error: {result['error']}")
    
    # Test 2: Logic Validator
    print("\n2. LOGIC VALIDATOR")
    print("-" * 70)
    
    solution = "The function checks for empty input and handles edge cases properly."
    rules = ["empty input", "edge cases"]
    
    result = validate_logic(solution, rules)
    print(f"Success: {result['success']}")
    if not result['success']:
        print(f"Violations: {result['violations']}")
    
    # Test 3: Format Validator
    print("\n3. FORMAT VALIDATOR")
    print("-" * 70)
    
    output = '{"result": "success"}'
    result = validate_format(output, "json")
    print(f"Success: {result['success']}")
    if not result['success']:
        print(f"Error: {result['error']}")
