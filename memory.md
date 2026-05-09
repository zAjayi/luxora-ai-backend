# LuxoraAI Backend - Project Memory

## 1. Project Reference
- **Project Name:** LuxoraAI
- **Description:** AI-powered content repurposing platform designed to help content creators transform existing content into platform-optimized social media posts.
- **Tech Stack:** FastAPI (Python), PostgreSQL, SQLAlchemy (Async), Alembic, OpenRouter API (Google Gemma series).
- **Core Loop:** Input Text -> Structure Request (Target Platforms, Tone, Brand Voice) -> OpenRouter LLM Inference -> Return Platform-Specific Formatted Output.

## 2. Implementation Tracking & Progress

### ✅ Completed Milestones
- **Project Initial Setup:** 
  - Full FastAPI project structure initialized (`app/api`, `app/core`, `app/db`, `app/models`, `app/schemas`, `app/services`, `app/ai`).
  - Database connection handling (`app/db/session.py` with SQLAlchemy `AsyncSession`).
  - Alembic initialization (`alembic.ini`, `alembic/env.py`) with initial schema migration (`versions/90305d544f93_initial_schema.py`).
- **Data Models:**
  - `User`, `RepurposeJob`, `RepurposedOutput`, and `BrandVoice` models implemented.
- **AI Integration (`app/ai`):**
  - Prompt construction via `prompt_builder.py` mapped to platform, tone, and brand constraints.
  - Base and Streaming completions integrated via `inference_client.py` using `openai.AsyncOpenAI` mapped to OpenRouter.
- **API Endpoints (`app/api/v1`):**
  - `repurpose.py` created with robust Server-Sent Events (SSE) streaming capabilities via `@router.post("/stream")` which consumes chunks from the LLM, parses JSON dynamically, and saves job data concurrently.
  - Setup of other endpoints (`brand_voices.py`, `jobs.py`, `outputs.py`).

### 🔄 In-Progress / Next Steps
- Verify error handling and edge cases around streaming LLM responses.
- Ensure database models are matching expected states from streaming completions.
- Finalize connections between generated `RepurposedOutput` arrays and `RepurposeJob` entities during active runs.
- Frontend React integration mapping with SSE endpoints.

## 3. Key Architectural Notes
- The AI Engine targets `google/gemma-4-31b-it` via OpenRouter.
- The Repurpose streaming parses a dynamically generated JSON output token-by-token (custom `StreamingJSONParser`) so the UI receives immediate feedback.

*(Note: Keep this file updated as new endpoints or architectural variations are introduced.)*