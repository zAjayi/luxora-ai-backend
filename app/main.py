from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base  # Ensure all models are loaded
from app.api.v1.endpoints import repurpose, brand_voices, jobs, outputs

app = FastAPI(title="LuxoraAI API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Reverted to wildcard to fix SSE streaming CORS constraint
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repurpose.router, prefix="/api/v1/repurpose", tags=["Repurpose"])
app.include_router(brand_voices.router, prefix="/api/v1/brand-voices", tags=["Brand Voices"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(outputs.router, prefix="/api/v1/outputs", tags=["Outputs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LuxoraAI API"}
