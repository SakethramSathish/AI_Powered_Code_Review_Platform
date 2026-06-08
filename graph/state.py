from typing import TypedDict, List, Dict, Any, Optional

class AnalysisState(TypedDict):
    """
    Represents the state of the code analysis workflow as it passes through LangGraph agents.
    """
    analysis_id: str
    project_name: str
    language: str

    # List of dictionaries containing file metadata and raw content
    # Example: [{"filename": "main.py", "content": "def foo(): pass"}]
    files: List[Dict[str, str]]

    #Agent Outputs
    review_findings: List[Dict[str, Any]]
    security_findings: List[Dict[str, Any]]
    complexity_metrics: Dict[str, Any]
    
    # Scores
    quality_score: int
    security_score: int
    maintainability_score: int

    # AI Authenticity (from Gemma 4 31B analysis)
    # Example: {"human_probability": 0.1, "ai_probability": 0.9, "confidence": 0.85}
    ai_probability: Dict[str, float]

    refactoring_suggestions: List[Dict[str, Any]]

    # Final generated markdown/PDF content path or string
    final_report: str
    
    # Workflow status tracking
    status: str