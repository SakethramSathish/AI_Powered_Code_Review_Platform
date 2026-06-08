import os
from typing import Dict, Any
from graph.state import AnalysisState

def analyze_repository(state: AnalysisState) -> Dict[str, Any]:
    """
    Agent 1: Repository Analyzer
    Analyzes the uploaded files to determine the primary programming language,
    project structure, and potential frameworks.
    """
    project_name = state.get("project_name", "Unknown Project")
    print(f"--- [Agent: Repo Analyzer] Initializing analysis for: {project_name} ---")
    
    files = state.get("files", [])
    if not files:
        print("Error: No files found in state.")
        return {"status": "failed_no_files"}

    extension_counts = {}
    framework_indicators = []
    
    # 1. Parse files for extensions and framework specific files
    for file_obj in files:
        filename = file_obj.get("filename", "")
        ext = os.path.splitext(filename)[1].lower()
        
        # Count extensions
        if ext:
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
            
        # 2. Detect common dependency management files to infer frameworks
        if filename in ["requirements.txt", "Pipfile", "pyproject.toml"]:
            framework_indicators.append("Python environment detected")
        elif filename == "package.json":
            framework_indicators.append("Node.js/NPM detected")
        elif filename == "pom.xml":
            framework_indicators.append("Java/Maven detected")
        elif filename == "CMakeLists.txt":
            framework_indicators.append("C/C++ CMake project")
        elif filename == "go.mod":
            framework_indicators.append("Go Modules detected")

    # 3. Determine the primary language based on the most frequent file extension
    primary_language = "Unknown"
    if extension_counts:
        # Map common extensions to language names
        ext_to_lang = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".c": "C",
            ".cpp": "C++",
            ".go": "Go",
            ".rb": "Ruby"
        }
        
        most_common_ext = max(extension_counts, key=extension_counts.get)
        primary_language = ext_to_lang.get(most_common_ext, f"Custom ({most_common_ext})")

    print(f"-> Primary Language Detected: {primary_language}")
    print(f"-> Frameworks Detected: {', '.join(framework_indicators) if framework_indicators else 'None'}")

    # LangGraph automatically merges this returned dictionary into the global AnalysisState
    return {
        "language": primary_language,
        "status": "repo_analyzed"
    }