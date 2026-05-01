from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import repurpose, brand_voices

app = FastAPI(title="LuxoraAI API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repurpose.router, prefix="/api/v1/repurpose", tags=["Repurpose"])
app.include_router(brand_voices.router, prefix="/api/v1/brand-voices", tags=["Brand Voices"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LuxoraAI API"}
