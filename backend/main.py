from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.api.endpoints import router as api_router

# Load environment variables from .env file (override=True ensures it picks up changes if you edit the file while the server is running)
load_dotenv(override=True)

app = FastAPI(
    title="CodeGuardian AI API",
    description="Agentic API backend for the CodeGuardian AI platform",
    version="1.0.0"
)

# Configure CORS so the Streamlit UI (typically port 8501) can talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP. In production, restrict this to Streamlit's URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "CodeGuardian AI API is running.", 
        "documentation": "Visit /docs for the Swagger UI."
    }