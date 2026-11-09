import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.db.base import Base  # Ensure all models are loaded
from app.api.v1.endpoints import repurpose, brand_voices, jobs, outputs, auth
from app.core.config import settings

app = FastAPI(title="LuxoraAI API", version="1.0.0")

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=settings.SENTRY_DSN)
    app.add_middleware(SentryAsgiMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://your-production-frontend-domain.com",  # TODO: Update with your actual production frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(repurpose.router, prefix="/api/v1/repurpose", tags=["Repurpose"])
app.include_router(brand_voices.router, prefix="/api/v1/brand-voices", tags=["Brand Voices"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(outputs.router, prefix="/api/v1/outputs", tags=["Outputs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LuxoraAI API"}
