from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.api.deps import get_authenticated_user
from app.db.session import get_db
from app.models.repurpose_job import RepurposeJob
from app.models.user import User
from app.schemas.repurpose import RepurposeJobResponse

router = APIRouter()

@router.get("/", response_model=List[RepurposeJobResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    result = await db.execute(
        select(RepurposeJob)
        .options(selectinload(RepurposeJob.outputs))
        .where(RepurposeJob.user_id == current_user.id)
        .order_by(RepurposeJob.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    jobs = result.scalars().all()
    return jobs

@router.get("/{id}", response_model=RepurposeJobResponse)
async def get_job(id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    result = await db.execute(
        select(RepurposeJob)
        .options(selectinload(RepurposeJob.outputs))
        .where(RepurposeJob.id == id, RepurposeJob.user_id == current_user.id)
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
