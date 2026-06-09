# Product Requirements Document (PRD)
**Project Name:** CodeGuardian AI
**Date:** 2026-06-09

## 1. Executive Summary
CodeGuardian AI is an intelligent, multi-agent code review platform. It leverages advanced LLM orchestration (LangGraph) and Google's Gemma models to automatically analyze code quality, flag security vulnerabilities, gauge maintainability, and suggest architectural refactoring. The platform aims to reduce manual code review overhead and improve overall software security and quality.

## 2. Target Audience
*   **Software Engineers:** Looking for immediate feedback on their code before submitting PRs.
*   **Security Teams:** Needing automated early-stage vulnerability detection.
*   **Engineering Managers:** Wanting high-level metrics on code complexity and maintainability.

## 3. Key Features
1.  **Multi-Source Ingestion:** Users can upload individual files, ZIP archives, or provide a public GitHub URL to automatically clone and analyze repositories.
2.  **Deep Vulnerability Scanning:** Automated identification of security flaws with actionable remediation steps.
3.  **AI Authorship Detection:** Evaluates the probability of AI-generated vs. human-written code.
4.  **Automated Refactoring:** Provides before-and-after code snippets for architectural and structural improvements.
5.  **Executive Reporting:** Compiles all agent findings into a cohesive, downloadable Markdown report.

## 4. User Flow
1.  **Input:** User accesses the Streamlit dashboard and inputs code (File upload, ZIP, or GitHub URL).
2.  **Processing:** The system triggers the FastAPI backend, which initiates the LangGraph workflow. Specialized agents process the code concurrently.
3.  **Review:** User polls or waits for the UI to display real-time or completed analysis results.
4.  **Export:** User downloads the comprehensive Markdown report containing findings and refactoring suggestions.

## 5. Non-Functional Requirements
*   **Performance:** The system should handle concurrent analysis requests without crashing.
*   **Usability:** The Streamlit dashboard must be intuitive and require zero training to use.
*   **Extensibility:** The LangGraph architecture must allow for easy addition of new specialized agents in the future.
