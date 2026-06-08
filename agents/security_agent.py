import json
from typing import Dict, Any
from graph.state import AnalysisState
from tools.llm_clients import call_gemini_llm

def analyze_security(state: AnalysisState) -> Dict[str, Any]:
    """
    Agent 3: Security Agent
    Scans source files for security vulnerabilities and risky coding patterns.
    """
    print("--- [Agent: Security] Starting vulnerability scan ---")
    
    files = state.get("files", [])
    if not files:
        return {"security_findings": [], "security_score": 100}

    # Prepare context
    code_context = ""
    for file_obj in files:
        filename = file_obj.get("filename", "unknown_file")
        content = file_obj.get("content", "")
        code_context += f"\n--- File: {filename} ---\n{content}\n"

    prompt = f"""
    You are an elite Application Security Engineer performing a static application security testing (SAST) review.
    Analyze the following source code for vulnerabilities including:
    1. Hardcoded credentials, secrets, or API keys
    2. SQL injection or command injection risks
    3. Unsafe file operations or path traversal
    4. Authentication/Authorization weaknesses
    5. Insecure cryptographic practices

    Return ONLY a valid JSON array of objects. Do not include markdown code blocks.
    Each object must exactly match this structure:
    {{
        "title": "Brief summary of vulnerability",
        "category": "Security",
        "severity": "Low|Medium|High|Critical",
        "file_path": "filename",
        "line_number": null,
        "description": "Detailed explanation of the risk",
        "recommendation": "Secure implementation advice"
    }}

    If no security issues are found, return an empty array: []

    Source Code Context:
    {code_context}
    """

    try:
        response_text = call_gemini_llm(prompt=prompt, model_name="gemma-4-31b-it")
        
        # Clean and parse JSON
        clean_json_str = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        findings = json.loads(clean_json_str) if clean_json_str else []
        
        # Calculate security score (Harsh penalties for security flaws)
        score = 100
        for finding in findings:
            penalty = {
                "Low": 5, 
                "Medium": 15, 
                "High": 30, 
                "Critical": 50
            }.get(finding.get("severity", "Medium"), 15)
            score -= penalty
            
        final_score = max(0, score)
        print(f"-> Security Scan Complete. Found {len(findings)} vulnerabilities. Score: {final_score}")
        
        return {
            "security_findings": findings,
            "security_score": final_score
        }

    except Exception as e:
        print(f"[-] Security Agent Error: {str(e)}")
        # Safe fallback
        return {"security_findings": [], "security_score": 0}