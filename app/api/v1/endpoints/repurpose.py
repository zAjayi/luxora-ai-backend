from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from app.schemas.repurpose import RepurposeRequest
from app.ai.inference_client import stream_repurposed_content

router = APIRouter()

@router.post("/stream")
async def repurpose_content_stream(request: Request, payload: RepurposeRequest):
    """
    Streams the repurposed content token-by-token using Server-Sent Events (SSE).
    """
    async def event_generator():
        try:
            # Yield chunks as they arrive from the AI model
            async for chunk in stream_repurposed_content(
                source_text=payload.source_text,
                platforms=payload.platforms,
                tone=payload.tone,
                brand_voice_description=payload.brand_voice_description
            ):
                # If client disconnects, stop streaming
                if await request.is_disconnected():
                    break
                
                yield {
                    "event": "message",
                    "data": chunk
                }
            
            # Send a completion event when done
            yield {
                "event": "done",
                "data": "[DONE]"
            }
        except Exception as e:
            yield {
                "event": "error",
                "data": str(e)
            }

    return EventSourceResponse(event_generator())
