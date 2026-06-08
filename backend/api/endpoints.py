import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException

from backend.schemas import UploadResponse, AnalysisRequest, AnalysisResponse, HistoryItem, GitHubUploadRequest
from backend.services.storage import save_upload_files, get_analysis_state, get_all_history, save_github_repo, clear_all_history
from backend.services.runner import run_analysis_workflow

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Handles source code uploads (individual files or ZIP archives)."""
    # Generate a unique ID for this analysis session
    analysis_id = f"analysis_{uuid.uuid4().hex[:8]}"
    
    # Save and extract files
    saved_count = save_upload_files(analysis_id, files)
    
    if saved_count == 0:
        raise HTTPException(status_code=400, detail="No valid files extracted. Please upload valid source files.")
        
    return UploadResponse(
        analysis_id=analysis_id,
        status="uploaded",
        file_count=saved_count
    )

@router.post("/upload-github", response_model=UploadResponse)
async def upload_github(request: GitHubUploadRequest):
    """Handles source code cloning from a GitHub repository."""
    analysis_id = f"analysis_{uuid.uuid4().hex[:8]}"
    
    saved_count = save_github_repo(analysis_id, request.github_url)
    
    if saved_count == 0:
        raise HTTPException(status_code=400, detail="Could not clone repository or it is empty. Ensure git is installed and the URL is valid.")
        
    return UploadResponse(
        analysis_id=analysis_id,
        status="uploaded",
        file_count=saved_count
    )

@router.post("/analyze")
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Triggers the LangGraph agent workflow asynchronously."""
    state = get_analysis_state(request.analysis_id)
    
    # If the state is not already processing/completed, trigger the workflow
    if not state or state.get("status") not in ["processing", "completed"]:
        # Add the runner to FastAPI's background tasks
        background_tasks.add_task(
            run_analysis_workflow, 
            request.analysis_id, 
            request.project_name
        )
        
    return {
        "analysis_id": request.analysis_id, 
        "status": "processing_started",
        "message": "Agent workflow initiated in the background."
    }

@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Retrieves the current state/results of an analysis."""
    state = get_analysis_state(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis ID not found.")
    return state

@router.get("/history", response_model=List[HistoryItem])
async def get_history():
    """Retrieves lightweight metadata for the history dashboard."""
    return get_all_history()

@router.delete("/history")
async def clear_history():
    """Clears all past analysis states and reports."""
    clear_all_history()
    return {"status": "success", "message": "History cleared"}

# Note: The GET /report/{id} endpoint for downloading the PDF/Markdown 
# will be added after we build the Report Generator Agent.