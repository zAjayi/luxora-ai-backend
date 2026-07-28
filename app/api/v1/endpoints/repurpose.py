from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sse_starlette.sse import EventSourceResponse
from app.schemas.repurpose import RepurposeRequest
from app.ai.inference_client import stream_repurposed_content
from app.db.session import get_db, AsyncSessionLocal
from app.models.repurpose_job import RepurposeJob
from app.models.repurposed_output import RepurposedOutput
from app.models.brand_voice import BrandVoice
import json

router = APIRouter()


class SingleOutputStreamExtractor:
    def __init__(self) -> None:
        self.buffer = ""
        self.platform_name = "linkedin"
        self.in_variant = False
        self.tail_guard = len('</variant>') - 1

    def consume(self, chunk: str) -> list[dict]:
        self.buffer += chunk
        events: list[dict] = []

        while True:
            if not self.in_variant:
                platform_start = self.buffer.find('<platform name="')
                if platform_start == -1:
                    return events

                platform_name_start = platform_start + len('<platform name="')
                platform_name_end = self.buffer.find('">', platform_name_start)
                if platform_name_end == -1:
                    return events

                self.platform_name = self.buffer[platform_name_start:platform_name_end]

                variant_start = self.buffer.find('<variant>', platform_name_end)
                if variant_start == -1:
                    return events

                self.buffer = self.buffer[variant_start + len('<variant>'):]
                self.in_variant = True
                continue

            variant_end = self.buffer.find('</variant>')
            if variant_end == -1:
                if len(self.buffer) <= self.tail_guard:
                    return events

                text = self.buffer[:-self.tail_guard]
                self.buffer = self.buffer[-self.tail_guard:]
                if text:
                    events.append({
                        "platform": self.platform_name,
                        "variant_index": 0,
                        "text": text,
                    })
                return events

            text = self.buffer[:variant_end]
            if text:
                events.append({
                    "platform": self.platform_name,
                    "variant_index": 0,
                    "text": text,
                })

            self.buffer = self.buffer[variant_end + len('</variant>'):]
            self.in_variant = False
            return events

    def flush(self) -> list[dict]:
        events: list[dict] = []
        if self.in_variant and self.buffer.strip():
            events.append({
                "platform": self.platform_name,
                "variant_index": 0,
                "text": self.buffer,
            })
        self.buffer = ""
        self.in_variant = False
        return events

@router.post("/stream")
async def repurpose_content_stream(request: Request, payload: RepurposeRequest, db: AsyncSession = Depends(get_db)):
    """
    Streams the repurposed content using XML tags and accumulated chunks.
    Accumulates chunks before parsing to improve performance.
    """
    brand_voice_desc = payload.brand_voice_description
    if payload.brand_voice_id:
        result = await db.execute(select(BrandVoice).where(BrandVoice.id == payload.brand_voice_id))
        brand_voice = result.scalars().first()
        if brand_voice:
            brand_voice_desc = brand_voice.style_guide_text
    # Create the job initially
    job = RepurposeJob(
        source_text=payload.source,
        source_url=payload.source_url,
        platforms=payload.platforms,
        tone=payload.tone,
        source_type="text",
        status="processing"
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    async def event_generator():
        streamed_text = ""
        extractor = SingleOutputStreamExtractor()
        
        try:
            # First send the job_id
            yield {
                "event": "job_created",
                "data": str(job.id)
            }
            
            # Yield chunks as they arrive from the AI model
            async for chunk in stream_repurposed_content(
                source=payload.source,
                platforms=payload.platforms,
                tone=payload.tone,
                brand_voice_description=brand_voice_desc,
                instruction=payload.instruction
            ):
                # If client disconnects, stop streaming
                if await request.is_disconnected():
                    break
                
                parsed_events = extractor.consume(chunk)
                for ev in parsed_events:
                    streamed_text += ev["text"]
                    yield {
                        "event": "message",
                        "data": json.dumps(ev)
                    }

            remaining_events = extractor.flush()
            for ev in remaining_events:
                streamed_text += ev["text"]
                yield {
                    "event": "message",
                    "data": json.dumps(ev)
                }

            # Persist the single streamed result
            try:
                async with AsyncSessionLocal() as bg_db:
                    output = RepurposedOutput(
                        job_id=job.id,
                        platform=extractor.platform_name,
                        variant_index=1,
                        content=streamed_text.strip()
                    )
                    bg_db.add(output)
                    
                    bg_job = await bg_db.get(RepurposeJob, job.id)
                    if bg_job:
                        bg_job.status = "completed"
                        await bg_db.commit()
            except Exception as ex:
                async with AsyncSessionLocal() as bg_db:
                    bg_job = await bg_db.get(RepurposeJob, job.id)
                    if bg_job:
                        bg_job.status = "failed"
                        await bg_db.commit()
            
            # Send a completion event when done
            yield {
                "event": "done",
                "data": "[DONE]"
            }
        except Exception as e:
            async with AsyncSessionLocal() as bg_db:
                bg_job = await bg_db.get(RepurposeJob, job.id)
                if bg_job:
                    bg_job.status = "failed"
                    await bg_db.commit()
            yield {
                "event": "error",
                "data": str(e)
            }

    return EventSourceResponse(event_generator())
