from langgraph.graph import StateGraph, START, END
from graph.state import AnalysisState

# Note: We are importing these agent functions assuming they exist. 
# We will write the actual implementation for these in the next steps!
from agents.repo_analyzer import analyze_repository
from agents.code_reviewer import review_code
from agents.security_agent import analyze_security
from agents.complexity_agent import calculate_complexity
from agents.ai_authenticity import analyze_ai_probability
from agents.refactoring_agent import suggest_refactoring
from agents.report_generator import generate_report

def create_analysis_graph():
    """Builds and compiles the LangGraph DAG for CodeGuardian AI."""
    
    # Initialize the graph with our state schema
    workflow = StateGraph(AnalysisState)

    # 1. Add Nodes (Registering the agent functions)
    workflow.add_node("repo_analyzer", analyze_repository)
    workflow.add_node("code_reviewer", review_code)
    workflow.add_node("security_agent", analyze_security)
    workflow.add_node("complexity_agent", calculate_complexity)
    workflow.add_node("ai_authenticity", analyze_ai_probability)
    workflow.add_node("refactoring_agent", suggest_refactoring)
    workflow.add_node("report_generator", generate_report)

    # 2. Define Edges (The flow of execution)
    
    # Entry Point -> Repo Analyzer
    workflow.add_edge(START, "repo_analyzer")
    
    # FAN-OUT: Repo Analyzer -> Parallel Analysis Agents
    workflow.add_edge("repo_analyzer", "code_reviewer")
    workflow.add_edge("repo_analyzer", "security_agent")
    workflow.add_edge("repo_analyzer", "complexity_agent")
    workflow.add_edge("repo_analyzer", "ai_authenticity")
    
    # FAN-IN: Parallel Analysis Agents -> Refactoring Agent
    # LangGraph waits for all incoming edges to complete before executing the target node.
    workflow.add_edge("code_reviewer", "refactoring_agent")
    workflow.add_edge("security_agent", "refactoring_agent")
    workflow.add_edge("complexity_agent", "refactoring_agent")
    workflow.add_edge("ai_authenticity", "refactoring_agent")
    
    # Refactoring -> Report Generation
    workflow.add_edge("refactoring_agent", "report_generator")
    
    # Report Generation -> Exit Point
    workflow.add_edge("report_generator", END)

    # Compile the graph into a runnable application
    return workflow.compile()

# Create a globally importable instance of the compiled graph
analysis_app = create_analysis_graph()