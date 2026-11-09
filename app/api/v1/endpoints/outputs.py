from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.api.deps import get_authenticated_user
from app.db.session import get_db
from app.models.repurposed_output import RepurposedOutput
from app.models.repurpose_job import RepurposeJob
from app.models.user import User
from app.schemas.repurpose import RepurposedOutputResponse
from app.ai.inference_client import generate_repurposed_content

router = APIRouter()

@router.post("/{id}/regenerate", response_model=RepurposedOutputResponse)
async def regenerate_output(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    result = await db.execute(
        select(RepurposedOutput)
        .options(selectinload(RepurposedOutput.job))
        .where(RepurposedOutput.id == id)
    )
    output = result.scalars().first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    job = output.job
    if not job:
        raise HTTPException(status_code=404, detail="Parent Job not found")
    if job.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Output not found")

    new_data = await generate_repurposed_content(
        source=job.source_text or "",
        platforms=[output.platform],
        tone=job.tone,
        brand_voice_description=None
    )

    platforms_data = new_data.get(output.platform, [])
    if not platforms_data or len(platforms_data) == 0:
        raise HTTPException(status_code=500, detail="AI generation returned nothing")

    new_content = platforms_data[0]
    output.content = new_content
    await db.commit()
    await db.refresh(output)

    return output
