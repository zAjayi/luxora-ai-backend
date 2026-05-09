from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sse_starlette.sse import EventSourceResponse
from app.schemas.repurpose import RepurposeRequest
from app.ai.inference_client import stream_repurposed_content
from app.ai.streaming_parser import XMLStreamingParser, ChunkAccumulator, parse_xml_response_to_json
from app.db.session import get_db, AsyncSessionLocal
from app.models.repurpose_job import RepurposeJob
from app.models.repurposed_output import RepurposedOutput
from app.models.brand_voice import BrandVoice
import json

router = APIRouter()

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
        source_text=payload.source_text,
        platforms=payload.platforms,
        tone=payload.tone,
        source_type="text",
        status="processing"
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    async def event_generator():
        full_response = ""
        xml_parser = XMLStreamingParser()
        chunk_accumulator = ChunkAccumulator(min_chunk_size=50)
        
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
                
                # Accumulate chunks to reduce parsing overhead
                accumulated = chunk_accumulator.add(chunk)
                if accumulated:
                    # Parse accumulated chunks
                    parsed_events = xml_parser.consume(accumulated)
                    for ev in parsed_events:
                        yield {
                            "event": "message",
                            "data": json.dumps(ev)
                        }
            
            # Flush any remaining accumulated chunks
            remaining = chunk_accumulator.flush()
            if remaining:
                parsed_events = xml_parser.consume(remaining)
                for ev in parsed_events:
                    yield {
                        "event": "message",
                        "data": json.dumps(ev)
                    }
            
            # Parse final response to create outputs
            try:
                outputs_data = parse_xml_response_to_json(full_response)
                
                async with AsyncSessionLocal() as bg_db:
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
