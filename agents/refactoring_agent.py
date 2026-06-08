import json
from typing import Dict, Any
from graph.state import AnalysisState
from tools.llm_clients import call_gemini_llm

def suggest_refactoring(state: AnalysisState) -> Dict[str, Any]:
    """
    Agent 6: Refactoring Agent
    Consolidates findings from previous parallel agents and suggests 
    concrete code improvements and architectural refactoring.
    """
    print("--- [Agent: Refactoring] Generating architecture & code improvements ---")
    
    files = state.get("files", [])
    if not files:
        return {"refactoring_suggestions": []}

    # Gather findings from previous nodes in the LangGraph
    review_issues = state.get("review_findings", [])
    security_issues = state.get("security_findings", [])
    complexity_metrics = state.get("complexity_metrics", {})
    
    # If the codebase is perfect (rare), we don't need to refactor
    if not review_issues and not security_issues and complexity_metrics.get("maintainability_score", 100) > 95:
        return {"refactoring_suggestions": []}

    # Prepare context
    code_context = ""
    for file_obj in files:
        filename = file_obj.get("filename", "unknown_file")
        content = file_obj.get("content", "")
        code_context += f"\n--- File: {filename} ---\n{content}\n"

    # Summarize the issues for the LLM to focus on
    issues_summary = f"""
    Quality Issues Found: {len(review_issues)}
    Security Vulnerabilities Found: {len(security_issues)}
    Maintainability Score: {complexity_metrics.get("maintainability_score", "Unknown")}
    """

    prompt = f"""
    You are a Principal Software Engineer. You are reviewing a codebase that has already been flagged for specific issues.
    Based on the source code provided, suggest 2 to 4 major refactoring recommendations.
    Focus on structural improvements, design patterns, and fixing the most critical security/quality flaws.

    Return ONLY a valid JSON array of objects. Do not include markdown code blocks.
    Each object must exactly match this structure:
    {{
        "title": "Area of improvement (e.g., 'Implement Repository Pattern' or 'Secure Database Connection')",
        "description": "Explanation of why this change is necessary and how it improves the codebase.",
        "code_before": "A snippet of the current problematic code",
        "code_after": "A snippet of the suggested improved implementation"
    }}

    Codebase Summary:
    {issues_summary}

    Source Code Context:
    {code_context}
    """

    try:
        response_text = call_gemini_llm(prompt=prompt, model_name="gemma-4-31b-it")
        
        # Clean and parse JSON
        clean_json_str = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        recommendations = json.loads(clean_json_str) if clean_json_str else []
        
        print(f"-> Refactoring Analysis Complete. Generated {len(recommendations)} recommendations.")
        
        return {
            "refactoring_suggestions": recommendations
        }

    except Exception as e:
        print(f"[-] Refactoring Agent Error: {str(e)}")
        # Safe fallback
        return {"refactoring_suggestions": []}