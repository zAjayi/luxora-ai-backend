from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.models.brand_voice import BrandVoice
from app.schemas.brand_voice import BrandVoiceCreate, BrandVoiceUpdate, BrandVoiceResponse

router = APIRouter()

@router.post("/", response_model=BrandVoiceResponse)
async def create_brand_voice(brand_voice: BrandVoiceCreate, db: AsyncSession = Depends(get_db)):
    db_brand_voice = BrandVoice(**brand_voice.model_dump())
    db.add(db_brand_voice)
    await db.commit()
    await db.refresh(db_brand_voice)
    return db_brand_voice

@router.get("/", response_model=List[BrandVoiceResponse])
async def list_brand_voices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BrandVoice))
    return result.scalars().all()

@router.get("/{id}", response_model=BrandVoiceResponse)
async def get_brand_voice(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BrandVoice).where(BrandVoice.id == id))
    brand_voice = result.scalars().first()
    if not brand_voice:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    return brand_voice

@router.put("/{id}", response_model=BrandVoiceResponse)
async def update_brand_voice(id: UUID, brand_voice: BrandVoiceUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BrandVoice).where(BrandVoice.id == id))
    db_brand_voice = result.scalars().first()
    if not db_brand_voice:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    
    update_data = brand_voice.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_brand_voice, field, value)
    
    db.add(db_brand_voice)
    await db.commit()
    await db.refresh(db_brand_voice)
    return db_brand_voice

@router.delete("/{id}")
async def delete_brand_voice(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BrandVoice).where(BrandVoice.id == id))
    db_brand_voice = result.scalars().first()
    if not db_brand_voice:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    
    await db.delete(db_brand_voice)
    await db.commit()
    return {"message": "Brand voice deleted successfully"}
