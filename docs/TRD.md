# Technical Requirements Document (TRD)
**Project Name:** CodeGuardian AI
**Date:** 2026-06-09

## 1. System Architecture Overview
CodeGuardian AI is decoupled into a FastAPI backend and a Streamlit frontend, driven by a LangGraph multi-agent orchestrator.

### 1.1 Frontend (UI)
*   **Framework:** Streamlit
*   **Responsibilities:** File uploads, GitHub URL ingestion, polling backend for results, displaying the final Markdown report and dashboard metrics.

### 1.2 Backend (API)
*   **Framework:** FastAPI
*   **Endpoints:**
    *   `/upload`: Accepts direct file/ZIP uploads.
    *   `/upload-github`: Accepts GitHub URLs for cloning.
    *   `/analyze`: Triggers the LangGraph workflow.
*   **Responsibilities:** REST API routing, background workflow execution, and storage management (File I/O, JSON state).

### 1.3 Orchestration & Agents
*   **Framework:** LangGraph (Directed Acyclic Graph)
*   **LLM Provider:** Google Gemma/Gemini API
*   **Specialized Agents:**
    1.  **Security Agent:** Scans for vulnerabilities.
    2.  **Code Review Agent:** General code quality and linting checks.
    3.  **AI Authenticity Agent:** Detects AI vs. human authorship.
    4.  **Complexity Agent:** Measures maintainability and cyclomatic complexity.
    5.  **Refactoring Agent:** Suggests architectural improvements.
    6.  **Report Generator:** Compiles findings from all other agents into a final report.

## 2. Technology Stack
*   **Language:** Python 3.10+
*   **API Framework:** FastAPI
*   **UI Framework:** Streamlit
*   **Orchestration:** LangGraph
*   **AI Models:** Google Gemma-4-31b-it (via Google API)
*   **Server:** Uvicorn

## 3. Data Storage & Management
*   **Local File System (`/storage/`):**
    *   `uploads/`: Temporary storage for cloned repos and uploaded files.
    *   `analysis/`: JSON state saves for LangGraph state persistence.
    *   `reports/`: Generated Markdown reports.

## 4. Security & Environment
*   Secrets (e.g., `GOOGLE_API_KEY`) are managed via a `.env` file.
*   Input validation is enforced via Pydantic schemas in the FastAPI backend.
*   Local storage must be periodically cleaned up to prevent disk exhaustion from large repository clones.

## 5. Deployment
*   The application currently runs locally using two separate processes (`uvicorn` for backend, `streamlit run` for frontend).
*   *Future Consideration:* Containerization via Docker (Dockerfile and docker-compose.yml exist in the repository).
