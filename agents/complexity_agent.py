import json
from typing import Dict, Any
from graph.state import AnalysisState
from tools.llm_clients import call_gemini_llm

def calculate_complexity(state: AnalysisState) -> Dict[str, Any]:
    """
    Agent 4: Complexity Agent
    Calculates code complexity metrics and generates a maintainability score.
    """
    print("--- [Agent: Complexity] Calculating maintainability metrics ---")
    
    files = state.get("files", [])
    if not files:
        return {
            "complexity_metrics": {"error": "No files to analyze"},
            "maintainability_score": 100
        }

    # Prepare context
    code_context = ""
    for file_obj in files:
        filename = file_obj.get("filename", "unknown_file")
        content = file_obj.get("content", "")
        code_context += f"\n--- File: {filename} ---\n{content}\n"

    prompt = f"""
    You are an expert Software Architect analyzing code complexity.
    Evaluate the following source code and estimate standard maintainability metrics.
    
    Return ONLY a valid JSON object. Do not include markdown code blocks.
    The object must exactly match this structure:
    {{
        "maintainability_score": <int between 0 and 100>,
        "average_cyclomatic_complexity": <int>,
        "highest_cyclomatic_complexity": <int>,
        "complex_functions": [
            {{
                "function_name": "name",
                "file_path": "filename",
                "complexity_reason": "Explanation of why it is complex"
            }}
        ],
        "overall_readability": "Brief summary of codebase maintainability"
    }}

    Score Guide:
    - 90-100: Highly modular, flat logic, very easy to maintain.
    - 70-89: Good, but has some nested loops or slightly long functions.
    - 50-69: Moderate "spaghetti" code, needs refactoring.
    - < 50: Highly complex, deep nesting, god objects/functions.

    Source Code Context:
    {code_context}
    """

    try:
        response_text = call_gemini_llm(prompt=prompt, model_name="gemma-4-31b-it")
        
        # Clean and parse JSON
        clean_json_str = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        metrics = json.loads(clean_json_str)
        
        score = metrics.get("maintainability_score", 85)
        print(f"-> Complexity Analysis Complete. Maintainability Score: {score}")
        
        return {
            "complexity_metrics": metrics,
            "maintainability_score": score
        }

    except Exception as e:
        print(f"[-] Complexity Agent Error: {str(e)}")
        # Safe fallback
        return {
            "complexity_metrics": {"error": "Failed to parse complexity metrics."},
            "maintainability_score": 0
        }