from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sse_starlette.sse import EventSourceResponse
from uuid import UUID
from typing import List
from app.db.session import get_db, AsyncSessionLocal
from app.models.article_field import ArticleField
from app.models.article_job import ArticleJob
from app.models.article_output import ArticleOutput
from app.schemas.article import (
    ArticleFieldCreate,
    ArticleFieldUpdate,
    ArticleFieldResponse,
    ArticleRequest,
    ArticleJobResponse,
)
from app.core.config import settings
from openai import AsyncOpenAI
from app.ai.streaming_parser import XMLStreamingParser, ChunkAccumulator
from app.ai.prompt_builder import build_article_system_prompt, build_article_user_prompt
import json

# Initialize the OpenAI client pointing to OpenRouter
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

router = APIRouter()

# ============ Article Fields CRUD ============

@router.post("/fields", response_model=ArticleFieldResponse)
async def create_article_field(field: ArticleFieldCreate, db: AsyncSession = Depends(get_db)):
    db_field = ArticleField(**field.model_dump())
    db.add(db_field)
    await db.commit()
    await db.refresh(db_field)
    return db_field

@router.get("/fields", response_model=List[ArticleFieldResponse])
async def list_article_fields(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArticleField))
    return result.scalars().all()

@router.get("/fields/{id}", response_model=ArticleFieldResponse)
async def get_article_field(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArticleField).where(ArticleField.id == id))
    field = result.scalars().first()
    if not field:
        raise HTTPException(status_code=404, detail="Article field not found")
    return field

@router.put("/fields/{id}", response_model=ArticleFieldResponse)
async def update_article_field(id: UUID, field: ArticleFieldUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArticleField).where(ArticleField.id == id))
    db_field = result.scalars().first()
    if not db_field:
        raise HTTPException(status_code=404, detail="Article field not found")
    
    update_data = field.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        setattr(db_field, field_name, value)
    
    db.add(db_field)
    await db.commit()
    await db.refresh(db_field)
    return db_field

@router.delete("/fields/{id}")
async def delete_article_field(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArticleField).where(ArticleField.id == id))
    db_field = result.scalars().first()
    if not db_field:
        raise HTTPException(status_code=404, detail="Article field not found")
    
    await db.delete(db_field)
    await db.commit()
    return {"message": "Article field deleted successfully"}

# ============ Article Generation Stream ============

@router.post("/stream")
async def generate_article_stream(request: Request, payload: ArticleRequest, db: AsyncSession = Depends(get_db)):
    """
    Streams the generated article content using XML tags and accumulated chunks.
    """
    # Get the field details
    field_result = await db.execute(select(ArticleField).where(ArticleField.id == payload.field_id))
    field = field_result.scalars().first()
    if not field:
        raise HTTPException(status_code=404, detail="Article field not found")
    
    # Create the job
    job = ArticleJob(
        source_text=payload.source_text,
        field_id=payload.field_id,
        tone=payload.tone,
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
            
            # Build prompts for article generation
            system_prompt = build_article_system_prompt()
            user_prompt = build_article_user_prompt(
                source_text=payload.source_text,
                field_name=field.name,
                field_description=field.description,
                tone=payload.tone
            )
            
            # Stream from OpenAI client
            response = await client.chat.completions.create(
                model="google/gemma-4-31b-it",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True
            )
            
            async for chunk in response:
                if await request.is_disconnected():
                    break
                
                if chunk.choices[0].delta.content:
                    delta = chunk.choices[0].delta.content
                    full_response += delta
                    
                    # Accumulate chunks
                    accumulated = chunk_accumulator.add(delta)
                    if accumulated:
                        parsed_events = xml_parser.consume(accumulated)
                        for ev in parsed_events:
                            yield {
                                "event": "message",
                                "data": json.dumps(ev)
                            }
            
            # Flush remaining chunks
            remaining = chunk_accumulator.flush()
            if remaining:
                parsed_events = xml_parser.consume(remaining)
                for ev in parsed_events:
                    yield {
                        "event": "message",
                        "data": json.dumps(ev)
                    }
            
            # Parse and save the output
            try:
                # Extract article content from XML
                import xml.etree.ElementTree as ET
                root = ET.fromstring(f"<root>{full_response}</root>")
                article_elem = root.find("article")
                
                article_content = ""
                if article_elem is not None and article_elem.text:
                    article_content = article_elem.text
                else:
                    # Fallback: use full response if no XML tags found
                    article_content = full_response
                
                # Save the article output
                async with AsyncSessionLocal() as bg_db:
                    output = ArticleOutput(
                        job_id=job.id,
                        content=article_content
                    )
                    bg_db.add(output)
                    await bg_db.commit()
                    
                    # Update job status
                    job_result = await bg_db.execute(
                        select(ArticleJob).where(ArticleJob.id == job.id)
                    )
                    job_record = job_result.scalars().first()
                    if job_record:
                        job_record.status = "completed"
                        await bg_db.commit()
                
            except Exception as e:
                print(f"Error parsing article response: {e}")
                async with AsyncSessionLocal() as bg_db:
                    job_result = await bg_db.execute(
                        select(ArticleJob).where(ArticleJob.id == job.id)
                    )
                    job_record = job_result.scalars().first()
                    if job_record:
                        job_record.status = "failed"
                        await bg_db.commit()
        
        except Exception as e:
            print(f"Error during article generation: {e}")
            async with AsyncSessionLocal() as bg_db:
                job_result = await bg_db.execute(
                    select(ArticleJob).where(ArticleJob.id == job.id)
                )
                job_record = job_result.scalars().first()
                if job_record:
                    job_record.status = "failed"
                    await bg_db.commit()
    
    return EventSourceResponse(event_generator())

@router.get("/{job_id}", response_model=ArticleJobResponse)
async def get_article_job(job_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArticleJob).where(ArticleJob.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Article job not found")
    return job
