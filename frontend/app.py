import streamlit as st
import requests
import time

import os

# Update this if you deploy the backend somewhere else
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="CodeGuardian AI", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ CodeGuardian AI")
st.markdown("### Intelligent Software Quality & Authenticity Analysis")

# --- Sidebar: History Dashboard ---
with st.sidebar:
    st.header("Analysis History")
    
    if st.button("🗑️ Clear All History", use_container_width=True):
        res = requests.delete(f"{API_BASE_URL}/history")
        if res.status_code == 200:
            st.success("History cleared!")
            if "current_analysis" in st.session_state:
                del st.session_state["current_analysis"]
            st.rerun()
            
    try:
        history_res = requests.get(f"{API_BASE_URL}/history")
        if history_res.status_code == 200:
            history = history_res.json()
            if not history:
                st.info("No past analyses found.")
            for item in history:
                # Format timestamp
                date_str = item['timestamp'][:10]
                
                st.caption(f"{date_str} - {item['language']}")
                st.markdown(f"**{item['project_name']}**")
                
                # Mini scorecard
                colA, colB = st.columns(2)
                colA.metric("Quality", f"{item['quality_score']}")
                colB.metric("AI Prob", f"{item['ai_probability']*100:.0f}%")
                
                if st.button(f"Load {item['analysis_id'][:8]}", key=item['analysis_id']):
                    st.session_state["current_analysis"] = item['analysis_id']
                st.divider()
    except requests.exceptions.ConnectionError:
        st.error("Backend API is offline. Please start FastAPI.")

# --- Main UI: Upload & Trigger ---
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        project_name = st.text_input("Project Name", "My Codebase")
    with col2:
        source_type = st.radio("Source Type", ["Upload Files/ZIP", "GitHub Repository"], horizontal=True)
        if source_type == "Upload Files/ZIP":
            uploaded_files = st.file_uploader(
                "Upload Source Code (Individual Files or ZIP)", 
                accept_multiple_files=True
            )
            github_url = None
        else:
            github_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
            uploaded_files = None

start_disabled = not uploaded_files and not github_url

if st.button("Start Analysis", type="primary", use_container_width=True, disabled=start_disabled):
    
    with st.spinner("Preparing files..."):
        if source_type == "Upload Files/ZIP":
            # 1. Upload Files
            files_payload = [
                ("files", (file.name, file.getvalue(), file.type)) 
                for file in uploaded_files
            ]
            upload_res = requests.post(f"{API_BASE_URL}/upload", files=files_payload)
        else:
            # 1. Clone GitHub Repo
            st.info("Cloning repository... this may take a moment.")
            upload_res = requests.post(f"{API_BASE_URL}/upload-github", json={"github_url": github_url})
            
        if upload_res.status_code == 200:
            analysis_id = upload_res.json()["analysis_id"]
            st.session_state["current_analysis"] = analysis_id
            
            # 2. Trigger the LangGraph background workflow
            requests.post(
                f"{API_BASE_URL}/analyze", 
                json={"analysis_id": analysis_id, "project_name": project_name}
            )
        else:
            st.error(f"Upload failed: {upload_res.text}")

st.divider()

# --- Main UI: Results Rendering ---
if "current_analysis" in st.session_state:
    analysis_id = st.session_state["current_analysis"]
    
    status_placeholder = st.empty()
    
    # 3. Polling loop
    status = "processing"
    state_data = {}
    
    with st.spinner("Agents are analyzing the codebase..."):
        while status in ["processing", "processing_started"]:
            try:
                state_res = requests.get(f"{API_BASE_URL}/analysis/{analysis_id}")
                if state_res.status_code == 200:
                    state_data = state_res.json()
                    status = state_data.get("status", "failed")
                else:
                    status = "failed"
            except requests.exceptions.ConnectionError:
                status = "failed"
                
            if status in ["processing", "processing_started"]:
                time.sleep(3) # Wait 3 seconds before polling again
    
    # 4. Display Results
    if status == "completed":
        st.success(f"Analysis Complete for: {state_data.get('project_name')}")
        
        # High-Level Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Code Quality", f"{state_data.get('quality_score', 0)}/100")
        m2.metric("Security Score", f"{state_data.get('security_score', 0)}/100")
        m3.metric("Maintainability", f"{state_data.get('maintainability_score', 0)}/100")
        
        ai_prob = state_data.get('ai_probability', {}).get('ai_probability', 0) * 100
        m4.metric("AI Authorship Prob", f"{ai_prob:.1f}%")
        
        # Deep Dive Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🧠 AI Authenticity", 
            "🔒 Security Findings", 
            "✨ Quality Findings", 
            "🛠️ Refactoring", 
            "📄 Raw Report"
        ])
        
        with tab1:
            st.markdown("### Authorship Breakdown")
            ai_data = state_data.get("ai_probability", {})
            st.info(f"**Agent Reasoning:** {ai_data.get('reasoning', 'N/A')}")
            
            c1, c2 = st.columns(2)
            c1.metric("Human Probability", f"{ai_data.get('human_probability', 1.0) * 100:.1f}%")
            c2.metric("Confidence Score", f"{ai_data.get('confidence', 0.0) * 100:.1f}%")
            
            st.markdown("### Complexity Metrics")
            st.json(state_data.get("complexity_metrics", {}))
        
        with tab2:
            st.markdown("### Security Vulnerabilities")
            findings = state_data.get("security_findings", [])
            if not findings:
                st.success("No major security vulnerabilities detected!")
            for finding in findings:
                with st.expander(f"🔴 {finding.get('title')} ({finding.get('severity')})"):
                    st.write(f"**File:** `{finding.get('file_path')}`")
                    st.write(f"**Description:** {finding.get('description')}")
                    st.write(f"**Recommendation:** {finding.get('recommendation')}")
        
        with tab3:
            st.markdown("### Code Quality Issues")
            findings = state_data.get("review_findings", [])
            if not findings:
                st.success("No major code quality issues detected!")
            for finding in findings:
                with st.expander(f"🟡 {finding.get('title')} ({finding.get('severity')})"):
                    st.write(f"**File:** `{finding.get('file_path')}`")
                    st.write(f"**Description:** {finding.get('description')}")
                    st.write(f"**Recommendation:** {finding.get('recommendation')}")

        with tab4:
            st.markdown("### Recommended Refactoring")
            suggestions = state_data.get("refactoring_suggestions", [])
            if not suggestions:
                st.info("Codebase structure is solid. No major refactoring needed.")
                
            for rec in suggestions:
                st.markdown(f"#### {rec.get('title')}")
                st.write(rec.get('description'))
                
                colA, colB = st.columns(2)
                with colA:
                    st.caption("Current Code:")
                    st.code(rec.get('code_before', '# No context provided'), language=state_data.get('language', 'python').lower())
                with colB:
                    st.caption("Suggested Implementation:")
                    st.code(rec.get('code_after', '# No fix provided'), language=state_data.get('language', 'python').lower())
                st.divider()
        
        with tab5:
            st.markdown("### Executive Summary")
            report_md = state_data.get("final_report", "No report generated.")
            st.markdown(report_md)
            
            st.download_button(
                label="Download Full Report (Markdown)", 
                data=report_md, 
                file_name=f"{state_data.get('project_name', 'project')}_CodeGuardian_Report.md",
                mime="text/markdown"
            )
            
    elif status == "failed":
        st.error("The background analysis crashed.")
        st.write(state_data.get("final_report", "Check backend terminal logs for the stack trace."))