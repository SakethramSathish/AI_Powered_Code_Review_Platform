from typing import Dict, Any
from datetime import datetime
from graph.state import AnalysisState

def generate_report(state: AnalysisState) -> Dict[str, Any]:
    """
    Agent 7: Report Generator
    Consolidates the entire state into a final Markdown report.
    """
    print("--- [Agent: Report Generator] Compiling final analysis report ---")
    
    project_name = state.get("project_name", "Unknown Project")
    language = state.get("language", "Unknown")
    
    # Retrieve all findings
    quality_score = state.get("quality_score", 0)
    security_score = state.get("security_score", 0)
    complexity_data = state.get("complexity_metrics", {})
    maintainability_score = state.get("maintainability_score", 0)
    
    ai_data = state.get("ai_probability", {})
    ai_prob_percent = ai_data.get("ai_probability", 0.0) * 100
    human_prob_percent = ai_data.get("human_probability", 1.0) * 100
    
    review_findings = state.get("review_findings", [])
    security_findings = state.get("security_findings", [])
    refactoring_suggestions = state.get("refactoring_suggestions", [])

    # Begin Markdown Assembly
    md = f"# CodeGuardian AI Analysis Report\n\n"
    md += f"**Project:** {project_name}  \n"
    md += f"**Primary Language:** {language}  \n"
    md += f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n"
    
    md += "---\n\n## 1. Executive Summary\n\n"
    md += "| Metric | Score |\n|---|---|\n"
    md += f"| **Code Quality** | {quality_score}/100 |\n"
    md += f"| **Security** | {security_score}/100 |\n"
    md += f"| **Maintainability** | {maintainability_score}/100 |\n\n"
    
    md += "### AI Authorship Probability\n"
    md += f"- **Human Authored:** {human_prob_percent:.1f}%\n"
    md += f"- **AI Assisted:** {ai_prob_percent:.1f}%\n"
    md += f"- *Reasoning:* {ai_data.get('reasoning', 'No reasoning provided.')}\n\n"
    
    md += "---\n\n## 2. Security Vulnerabilities\n\n"
    if security_findings:
        for finding in security_findings:
            md += f"### 🔴 {finding.get('title')} ({finding.get('severity')} Severity)\n"
            md += f"- **File:** `{finding.get('file_path')}`\n"
            md += f"- **Description:** {finding.get('description')}\n"
            md += f"- **Recommendation:** {finding.get('recommendation')}\n\n"
    else:
        md += "✅ No major security vulnerabilities detected.\n\n"

    md += "---\n\n## 3. Code Quality & Anti-Patterns\n\n"
    if review_findings:
        for finding in review_findings:
            md += f"### 🟡 {finding.get('title')} ({finding.get('severity')} Severity)\n"
            md += f"- **File:** `{finding.get('file_path')}`\n"
            md += f"- **Description:** {finding.get('description')}\n"
            md += f"- **Recommendation:** {finding.get('recommendation')}\n\n"
    else:
        md += "✅ No major code quality issues detected.\n\n"

    md += "---\n\n## 4. Refactoring Recommendations\n\n"
    if refactoring_suggestions:
        for idx, rec in enumerate(refactoring_suggestions, 1):
            md += f"### {idx}. {rec.get('title')}\n"
            md += f"{rec.get('description')}\n\n"
            if rec.get('code_before'):
                md += "**Current Implementation:**\n```python\n" + rec.get('code_before') + "\n```\n\n"
            if rec.get('code_after'):
                md += "**Suggested Implementation:**\n```python\n" + rec.get('code_after') + "\n```\n\n"
    else:
        md += "✅ Code architecture is solid; no major refactoring suggested.\n\n"

    print("-> Report Generation Complete.")
    
    return {
        "final_report": md,
        "status": "completed"
    }