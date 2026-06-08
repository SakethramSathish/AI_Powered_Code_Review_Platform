from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    analysis_id: str = Field(..., description="Unique identifier for the uploaded session")
    status: str = Field(..., description="Status of the upload process")
    file_count: int = Field(..., description="Number of source files successfully extracted")

class AnalysisRequest(BaseModel):
    analysis_id: str = Field(..., description="The ID of the uploaded files session to analyze")
    project_name: Optional[str] = Field("CodeGuardian_Project", description="Optional custom name for the project")

class GitHubUploadRequest(BaseModel):
    github_url: str = Field(..., description="The URL of the GitHub repository")

class FindingItem(BaseModel):
    title: str = Field(..., description="Brief summary of the issue found")
    category: str = Field(..., description="Category (e.g., Quality, Security, Bug)")
    severity: str = Field(..., description="Severity level: Low, Medium, High, Critical")
    file_path: str = Field(..., description="File where the finding was detected")
    line_number: Optional[int] = Field(None, description="Line number if applicable")
    description: str = Field(..., description="Detailed explanation of the issue")
    recommendation: str = Field(..., description="Actionable fix or refactoring advice")

class RecommendationItem(BaseModel):
    title: str = Field(..., description="Area of improvement")
    description: str = Field(..., description="Explanation of why this change is suggested")
    code_before: Optional[str] = Field(None, description="Original code pattern")
    code_after: Optional[str] = Field(None, description="Suggested implementation")

class AnalysisResponse(BaseModel):
    analysis_id: str
    project_name: str
    language: str
    quality_score: int = Field(..., ge=0, le=100, description="Overall code quality score out of 100")
    security_score: int = Field(..., ge=0, le=100, description="Overall security rating out of 100")
    maintainability_score: int = Field(..., ge=0, le=100, description="Overall maintainability index out of 100")
    ai_probability: float = Field(..., ge=0.0, le=1.0, description="Estimated probability of heavy AI involvement")
    findings: List[FindingItem] = Field(default_factory=list)
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    status: str

class HistoryItem(BaseModel):
    analysis_id: str
    project_name: str
    language: str
    timestamp: str
    quality_score: int
    ai_probability: float