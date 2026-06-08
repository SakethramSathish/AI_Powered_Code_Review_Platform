# 🛡️ CodeGuardian AI: Agentic Code Review Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-000000?style=for-the-badge)](#)
[![Gemma-4-31b](https://img.shields.io/badge/Model-Gemma--4--31b--it-orange?style=for-the-badge)](https://ai.google.dev/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

CodeGuardian AI is an intelligent, multi-agent code review platform built with FastAPI, Streamlit, and LangGraph. It ingests GitHub repositories or local files, orchestrating specialized LLM agents (powered by Google's Gemma models) to concurrently analyze code quality, flag security vulnerabilities, gauge maintainability, and suggest architectural refactoring.

---

## 🏷️ Tags
`generative-ai` `code-review` `fastapi` `streamlit` `langgraph` `agentic-workflow` `security-analysis` `gemma-llm` `python` `static-analysis`

---

## ✨ Key Features
1. **Multi-Source Ingestion:** Upload individual files, ZIP archives, or drop in a public GitHub URL to automatically clone and analyze entire repositories.
2. **LangGraph Agentic Orchestration:** Utilizes a Directed Acyclic Graph (DAG) to run concurrent, specialized AI agents.
3. **Deep Vulnerability Scanning:** Identifies security flaws and provides actionable remediation steps.
4. **AI Authorship Detection:** Evaluates the probability of AI-generated vs. human-written code.
5. **Automated Refactoring:** Provides before-and-after code snippets for architectural and structural improvements.
6. **Executive Reporting:** Compiles findings into a cohesive, downloadable Markdown report.

---

## 🏗️ System Architecture

CodeGuardian AI is decoupled into a robust FastAPI backend and a responsive Streamlit frontend, driven by a LangGraph multi-agent orchestrator.

```mermaid
flowchart TD
    %% Styling
    classDef ui fill:#FF4B4B,stroke:#bd3737,color:#ffffff,stroke-width:2px;
    classDef api fill:#009485,stroke:#005c53,color:#ffffff,stroke-width:2px;
    classDef graph fill:#000000,stroke:#333333,color:#ffffff,stroke-width:2px;
    classDef agent fill:#f97316,stroke:#c2410c,color:#ffffff,stroke-width:2px;
    classDef storage fill:#3b82f6,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;

    subgraph UI ["🎨 Frontend"]
        Streamlit["Streamlit Dashboard\n(Uploads, History, UI)"]:::ui
    end

    subgraph API ["⚙️ Backend (FastAPI)"]
        Endpoints["REST API Endpoints\n(/upload, /upload-github, /analyze)"]:::api
        Runner["Background Workflow Runner"]:::api
        StorageSvc["Storage Service\n(JSON State, File I/O)"]:::storage
    end

    subgraph ORCHESTRATION ["🧠 LangGraph Workflow"]
        State["Graph State Schema"]:::graph
        Router["DAG Orchestrator"]:::graph
        
        SecAgent["Security Agent"]:::agent
        QualAgent["Code Review Agent"]:::agent
        AuthAgent["AI Authenticity Agent"]:::agent
        CompAgent["Complexity Agent"]:::agent
        RefAgent["Refactoring Agent"]:::agent
        RepAgent["Report Generator"]:::agent
    end

    %% Flow
    Streamlit -->|File/URL| Endpoints
    Endpoints -->|Save/Clone| StorageSvc
    Endpoints -.->|Triggers| Runner
    Runner -->|Invoke| Router
    
    Router --> SecAgent
    Router --> QualAgent
    Router --> AuthAgent
    Router --> CompAgent
    Router --> RefAgent
    
    SecAgent --> RepAgent
    QualAgent --> RepAgent
    AuthAgent --> RepAgent
    CompAgent --> RepAgent
    RefAgent --> RepAgent
    
    RepAgent -->|Save Report| StorageSvc
    Streamlit -->|Poll Results| Endpoints
```

---

## 📂 Folder Structure

```text
AI-Powered Code Review Platform/
│
├── agents/                     # Specialized LLM Agents
│   ├── ai_authenticity.py      # Detects AI vs Human authorship
│   ├── code_reviewer.py        # General code quality & linting
│   ├── complexity_agent.py     # Maintainability & Cyclomatic Complexity
│   ├── refactoring_agent.py    # Architecture improvements
│   ├── report_generator.py     # Final Markdown compiler
│   └── security_agent.py       # Vulnerability scanner
│
├── backend/                    # FastAPI Server
│   ├── api/
│   │   └── endpoints.py        # REST routes (/upload, /history)
│   ├── services/
│   │   ├── runner.py           # Background LangGraph execution
│   │   └── storage.py          # Local File/JSON DB management
│   ├── main.py                 # FastAPI application entrypoint
│   └── schemas.py              # Pydantic data validation models
│
├── frontend/                   # User Interface
│   └── app.py                  # Main Streamlit dashboard
│
├── graph/                      # LangGraph Orchestration
│   └── workflow.py             # DAG definition & State typing
│
├── tools/                      # Shared Utilities
│   ├── llm_clients.py          # Google Gemini/Gemma API client wrapper
│   └── static_analysis.py      # Regex/AST based static metrics
│
├── storage/                    # Auto-generated Persistence
│   ├── analysis/               # JSON State saves
│   ├── reports/                # Generated Markdown reports
│   └── uploads/                # Temporary source file storage
│
├── .env                        # API Keys & Secrets
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google API Key with access to Gemma/Gemini models.
- Git (required for cloning GitHub repositories via the UI).

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/code-guardian-ai.git
cd code-guardian-ai

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your Google API key:
```env
GOOGLE_API_KEY="your_google_api_key_here"
# or
GEMINI_API_KEY="your_google_api_key_here"
```

### 4. Running the Application
You will need to run the backend and frontend simultaneously in two separate terminals.

**Terminal 1 (Backend):**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
streamlit run frontend/app.py
```

Navigate to `http://localhost:8501` in your browser to start reviewing code!
