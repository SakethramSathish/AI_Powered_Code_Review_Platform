import os
import shutil
from typing import List, Dict, Any
from graph.workflow import analysis_app
from backend.services.storage import save_analysis_state, UPLOADS_DIR, REPORTS_DIR

def load_files_from_disk(analysis_id: str) -> List[Dict[str, str]]:
    """Loads extracted source code files from the upload directory."""
    files = []
    session_dir = UPLOADS_DIR / analysis_id
    
    if not session_dir.exists():
        return files
        
    for root, _, filenames in os.walk(session_dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            try:
                # Read file content. Ignore binaries/images.
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                files.append({
                    "filename": filename,
                    "content": content
                })
            except UnicodeDecodeError:
                # Skip binary files seamlessly
                continue
                
    return files

def run_analysis_workflow(analysis_id: str, project_name: str) -> None:
    """
    Executes the LangGraph DAG in the background.
    Updates the JSON state file upon completion.
    """
    print(f"[*] Starting background analysis for session: {analysis_id}")
    
    # 1. Define the initial state for the LangGraph
    initial_state = {
        "analysis_id": analysis_id,
        "project_name": project_name,
        "language": "Unknown",
        "files": load_files_from_disk(analysis_id),
        "review_findings": [],
        "security_findings": [],
        "complexity_metrics": {},
        "ai_probability": {},
        "refactoring_suggestions": [],
        "final_report": "",
        "status": "processing"
    }
    
    # Save the 'processing' state immediately so the frontend knows it's working
    save_analysis_state(analysis_id, initial_state)
    
    try:
        # 2. Invoke the compiled LangGraph DAG
        final_state = analysis_app.invoke(initial_state)
        
        # 3. Mark as completed and save final state to JSON
        final_state["status"] = "completed"
        save_analysis_state(analysis_id, final_state)
        
        # 4. Save the generated Markdown Report to the reports directory
        report_path = REPORTS_DIR / f"{analysis_id}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(final_state.get("final_report", "# Report Generation Failed"))
            
        print(f"[+] Analysis successfully completed for {analysis_id}")
        
    except Exception as e:
        print(f"[-] Workflow failed for {analysis_id}: {str(e)}")
        # Save failed state so the frontend doesn't hang infinitely
        initial_state["status"] = "failed"
        initial_state["final_report"] = f"Analysis crashed: {str(e)}"
        save_analysis_state(analysis_id, initial_state)
    finally:
        # 5. Clean up temporary files to save storage
        session_dir = UPLOADS_DIR / analysis_id
        if session_dir.exists():
            import stat
            def remove_readonly(func, path, excinfo):
                os.chmod(path, stat.S_IWRITE)
                func(path)
                
            try:
                shutil.rmtree(session_dir, onerror=remove_readonly)
                print(f"[*] Cleaned up temporary files for {analysis_id}")
            except Exception as e:
                print(f"[-] Failed to clean up {analysis_id}: {str(e)}")