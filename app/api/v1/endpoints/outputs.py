from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.db.session import get_db
from app.models.repurposed_output import RepurposedOutput
from app.models.repurpose_job import RepurposeJob
from app.schemas.repurpose import RepurposedOutputResponse
from app.ai.inference_client import generate_repurposed_content

router = APIRouter()

@router.post("/{id}/regenerate", response_model=RepurposedOutputResponse)
async def regenerate_output(id: UUID, db: AsyncSession = Depends(get_db)):
    # 1. Fetch output
    result = await db.execute(
        select(RepurposedOutput)
        .options(selectinload(RepurposedOutput.job))
        .filter(RepurposedOutput.id == id)
    )
    output = result.scalars().first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")
        
    job = output.job
    if not job:
        raise HTTPException(status_code=404, detail="Parent Job not found")
    
    # 2. Call AI just for this specific platform
    # Since generate_repurposed_content currently takes a list of platforms, we pass just this platform
    # It returns a dict like { "twitter": ["..."] }
    new_data = await generate_repurposed_content(
        source_text=job.source_text,
        platforms=[output.platform],
        tone=job.tone,
        brand_voice_description=None # Could fetch from brand voice table later if needed
    )
    
    platforms_data = new_data.get(output.platform, [])
    if not platforms_data or len(platforms_data) == 0:
        raise HTTPException(status_code=500, detail="AI generation returned nothing")
        
    # We could replace the content, or perhaps take the first variant from the new array
    new_content = platforms_data[0]
    
    # 3. Update the Output record
    output.content = new_content
    await db.commit()
    await db.refresh(output)
    
    return output
