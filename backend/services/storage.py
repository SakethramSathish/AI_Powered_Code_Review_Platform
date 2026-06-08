import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import UploadFile

# Resolve base directories based on the project structure
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
ANALYSIS_DIR = STORAGE_DIR / "analysis"
REPORTS_DIR = STORAGE_DIR / "reports"
LOGS_DIR = STORAGE_DIR / "logs"

# Ensure all storage directories exist at startup
for dir_path in [UPLOADS_DIR, ANALYSIS_DIR, REPORTS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

def save_upload_files(analysis_id: str, files: List[UploadFile]) -> int:
    """
    Saves uploaded files to the local file system under a specific analysis ID.
    Handles ZIP extraction automatically.
    """
    session_dir = UPLOADS_DIR / analysis_id
    session_dir.mkdir(exist_ok=True)
    
    saved_count = 0
    for file in files:
        file_path = session_dir / file.filename
        
        # Write the file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Handle ZIP extraction if necessary
        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(session_dir)
            os.remove(file_path)  # Clean up the zip file after extraction
            
            # Count extracted files (excluding directories)
            for root, _, extracted_files in os.walk(session_dir):
                saved_count += len(extracted_files)
        else:
            saved_count += 1
            
    return saved_count

def save_github_repo(analysis_id: str, github_url: str) -> int:
    """
    Clones a GitHub repository to the local file system under a specific analysis ID.
    Removes the .git directory to avoid analyzing git internals.
    """
    session_dir = UPLOADS_DIR / analysis_id
    session_dir.mkdir(exist_ok=True)
    
    import subprocess
    try:
        # Clone the repository with depth 1 to save time and space
        result = subprocess.run(
            ["git", "clone", "--depth", "1", github_url, str(session_dir)],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Git clone failed: {e.stderr}")
        return 0
        
    # Remove the .git directory (handling read-only files on Windows)
    import stat
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    git_dir = session_dir / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir, onerror=remove_readonly)
        
    # Count extracted files
    saved_count = 0
    for root, _, extracted_files in os.walk(session_dir):
        saved_count += len(extracted_files)
        
    return saved_count

def save_analysis_state(analysis_id: str, state_data: Dict[str, Any]) -> None:
    """Saves the current LangGraph state to a JSON file."""
    file_path = ANALYSIS_DIR / f"{analysis_id}.json"
    with open(file_path, "w") as f:
        json.dump(state_data, f, indent=4)

def get_analysis_state(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific analysis state by ID."""
    file_path = ANALYSIS_DIR / f"{analysis_id}.json"
    if not file_path.exists():
        return None
    with open(file_path, "r") as f:
        return json.load(f)

def get_all_history() -> List[Dict[str, Any]]:
    """Retrieves lightweight metadata for all past analyses to populate the history dashboard."""
    history = []
    for file_path in ANALYSIS_DIR.glob("*.json"):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                
                # Default to 0/empty if analysis crashed or is incomplete
                history.append({
                    "analysis_id": data.get("analysis_id", file_path.stem),
                    "project_name": data.get("project_name", "Unknown"),
                    "language": data.get("language", "Unknown"),
                    "timestamp": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "quality_score": data.get("quality_score", 0),
                    "ai_probability": data.get("ai_probability", {}).get("ai_probability", 0.0)
                })
        except json.JSONDecodeError:
            continue
            
    # Sort history so the newest analyses appear first
    history.sort(key=lambda x: x["timestamp"], reverse=True)
    return history

def clear_all_history() -> None:
    """Clears all past analysis states and reports."""
    for file_path in ANALYSIS_DIR.glob("*.json"):
        try:
            file_path.unlink()
        except OSError:
            pass
    for file_path in REPORTS_DIR.glob("*.md"):
        try:
            file_path.unlink()
        except OSError:
            pass