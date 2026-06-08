import re
import ast
from typing import Dict, Any

def extract_loc_metrics(content: str) -> Dict[str, int]:
    """
    Calculates Lines of Code (LOC), blank lines, and approximate comment lines.
    Provides deterministic sizing metrics for the LLM.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    
    # Basic comment approximation (handles #, //, and single-line /*)
    comment_lines = sum(1 for line in lines if line.strip().startswith(('#', '//', '/*')))
    
    return {
        "total_lines": total_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "source_lines": total_lines - blank_lines - comment_lines
    }

def estimate_cyclomatic_complexity(content: str, language: str) -> int:
    """
    Provides a baseline deterministic cyclomatic complexity score.
    For Python, uses the AST. For other languages, uses regex keyword heuristics.
    """
    complexity = 1  # Base complexity for the file/module

    if language.lower() == "python":
        try:
            tree = ast.parse(content)
            # Walk the tree and add 1 for every decision point
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.IfExp, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
                    complexity += 1
            return complexity
        except SyntaxError:
            # If the Python code is malformed, fall back to the regex heuristic
            pass 
            
    # Regex Heuristic for C-family and other languages (Java, JS, C++, Go, etc.)
    # We count decision-making keywords and operators.
    decision_patterns = [
        r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\bcase\b', 
        r'\bcatch\b', r'&&', r'\|\|', r'\?'
    ]
    
    # Remove strings and comments from content to avoid false positives
    clean_content = re.sub(r'".*?"|\'.*?\'', '', content)
    clean_content = re.sub(r'//.*|/\*[\s\S]*?\*/', '', clean_content)
    
    for pattern in decision_patterns:
        complexity += len(re.findall(pattern, clean_content))

    return complexity

def get_file_stats(content: str, language: str) -> Dict[str, Any]:
    """
    Consolidates all deterministic static analysis metrics into a single dictionary.
    """
    loc_data = extract_loc_metrics(content)
    complexity = estimate_cyclomatic_complexity(content, language)
    
    return {
        **loc_data,
        "cyclomatic_complexity": complexity
    }