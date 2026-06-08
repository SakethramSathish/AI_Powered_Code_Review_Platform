import json
from typing import Dict, Any
from graph.state import AnalysisState
from tools.llm_clients import call_gemini_llm

def review_code(state: AnalysisState) -> Dict[str, Any]:
    """
    Agent 2: Code Review Agent
    Analyzes source files for code quality, readability, and maintainability.
    """
    print("--- [Agent: Code Reviewer] Starting quality analysis ---")
    
    files = state.get("files", [])
    if not files:
        return {"review_findings": []}

    # Prepare the payload by combining file contents
    # For MVP, we concatenate them. For production, we'd process large repos in chunks.
    code_context = ""
    for file_obj in files:
        filename = file_obj.get("filename", "unknown_file")
        content = file_obj.get("content", "")
        code_context += f"\n--- File: {filename} ---\n{content}\n"

    prompt = f"""
    You are an expert Software Engineer performing a code review.
    Analyze the following source code for:
    1. Naming conventions
    2. Modularity and function length
    3. Readability and formatting
    4. Maintainability and Best Practices

    Return ONLY a valid JSON array of objects. Do not include markdown code blocks (like ```json).
    Each object must exactly match this structure:
    {{
        "title": "Brief summary",
        "category": "Quality",
        "severity": "Low|Medium|High",
        "file_path": "filename",
        "line_number": null,
        "description": "Detailed explanation",
        "recommendation": "Actionable fix"
    }}

    Source Code Context:
    {code_context}
    """

    try:
        # Call the Gemini LLM
        response_text = call_gemini_llm(
            prompt=prompt, 
            model_name="gemma-4-31b-it"
        )
        
        # Strip potential markdown formatting if the LLM includes it despite instructions
        clean_json_str = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        findings = json.loads(clean_json_str)
        
        # Calculate a rough quality score based on findings (starting at 100)
        score = 100
        for finding in findings:
            penalty = {"Low": 2, "Medium": 5, "High": 10}.get(finding.get("severity", "Low"), 2)
            score -= penalty
            
        print(f"-> Code Review Complete. Found {len(findings)} issues. Estimated Score: {max(0, score)}")
        
        return {
            "review_findings": findings,
            # We can stash the calculated score in a temporary key or merge it later 
            # in the report generator. Let's pass it along.
            "quality_score": max(0, score) 
        }

    except Exception as e:
        print(f"[-] Code Review Agent Error: {str(e)}")
        # Graceful degradation: return empty findings if the LLM fails or JSON parsing breaks
        return {"review_findings": []}