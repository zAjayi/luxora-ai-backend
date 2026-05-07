from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sse_starlette.sse import EventSourceResponse
from app.schemas.repurpose import RepurposeRequest
from app.ai.inference_client import stream_repurposed_content
from app.db.session import get_db
from app.models.repurpose_job import RepurposeJob
from app.models.repurposed_output import RepurposedOutput
from app.models.brand_voice import BrandVoice
import json

router = APIRouter()

@router.post("/stream")
async def repurpose_content_stream(request: Request, payload: RepurposeRequest, db: AsyncSession = Depends(get_db)):
    """
    Streams the repurposed content token-by-token using Server-Sent Events (SSE).
    """
    brand_voice_desc = payload.brand_voice_description
    if payload.brand_voice_id:
        result = await db.execute(select(BrandVoice).where(BrandVoice.id == payload.brand_voice_id))
        brand_voice = result.scalars().first()
        if brand_voice:
            brand_voice_desc = brand_voice.style_guide_text
    # Create the job initially
    job = RepurposeJob(
        source_text=payload.source_text,
        platforms=payload.platforms,
        tone=payload.tone,
        source_type="text",
        status="processing"
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    class StreamingJSONParser:
        def __init__(self):
            self.state = "search_key"
            self.platform = None
            self.variant_index = 0
            self.is_escaped = False
            self.unicode_buffer = ""
            self.buffer = ""
            self.events = []

        def consume(self, chunk: str):
            for char in chunk:
                if self.state == "search_key":
                    if char == '"':
                        self.state = "read_key"
                        self.buffer = ""
                elif self.state == "read_key":
                    if char == '"':
                        self.platform = self.buffer
                        self.state = "wait_colon"
                    else:
                        self.buffer += char
                elif self.state == "wait_colon":
                    if char == ':':
                        self.state = "wait_array"
                elif self.state == "wait_array":
                    if char == '[':
                        self.state = "in_array"
                        self.variant_index = 0
                elif self.state == "in_array":
                    if char == '"':
                        self.state = "in_string"
                    elif char == ']':
                        self.state = "search_key"
                elif self.state == "in_unicode":
                    self.unicode_buffer += char
                    if len(self.unicode_buffer) == 4:
                        try:
                            decoded = chr(int(self.unicode_buffer, 16))
                            self.events.append({
                                "platform": self.platform,
                                "variant_index": self.variant_index,
                                "text": decoded
                            })
                        except ValueError:
                            pass
                        self.state = "in_string"
                elif self.state == "in_string":
                    if self.is_escaped:
                        if char == 'u':
                            self.state = "in_unicode"
                            self.unicode_buffer = ""
                        else:
                            self.events.append({
                                "platform": self.platform,
                                "variant_index": self.variant_index,
                                "text": {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "/": "/"}.get(char, char)
                            })
                        self.is_escaped = False
                    elif char == '\\':
                        self.is_escaped = True
                    elif char == '"':
                        self.state = "in_array"
                        self.variant_index += 1
                    else:
                        self.events.append({
                            "platform": self.platform,
                            "variant_index": self.variant_index,
                            "text": char
                        })
            
            res = self.events
            self.events = []
            return res

    async def event_generator():
        full_response = ""
        parser = StreamingJSONParser()
        try:
            # First send the job_id
            yield {
                "event": "job_created",
                "data": str(job.id)
            }
            
            # Yield chunks as they arrive from the AI model
            async for chunk in stream_repurposed_content(
                source_text=payload.source_text,
                platforms=payload.platforms,
                tone=payload.tone,
                brand_voice_description=brand_voice_desc
            ):
                # If client disconnects, stop streaming
                if await request.is_disconnected():
                    break
                
                full_response += chunk
                # Parse structure incrementally and yield each character with metadata
                parsed_events = parser.consume(chunk)
                for ev in parsed_events:
                    yield {
                        "event": "message",
                        "data": json.dumps(ev)
                    }
            
            # Parse full response to create outputs
            try:
                # Remove markdown codeblocks if generated by AI
                cleaned_response = full_response
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response.strip("`").replace("json\n", "", 1)
                
                outputs_data = json.loads(cleaned_response)
                
                # Save outputs
                for platform, variants in outputs_data.items():
                    if isinstance(variants, list):
                        for index, content in enumerate(variants):
                            output = RepurposedOutput(
                                job_id=job.id,
                                platform=platform,
                                variant_index=index + 1,
                                content=content
                            )
                            db.add(output)
                
                job.status = "completed"
                await db.commit()
            except Exception as ex:
                job.status = "failed"
                await db.commit()
            
            # Send a completion event when done
            yield {
                "event": "done",
                "data": "[DONE]"
            }
        except Exception as e:
            job.status = "failed"
            await db.commit()
            yield {
                "event": "error",
                "data": str(e)
            }

    return EventSourceResponse(event_generator())
