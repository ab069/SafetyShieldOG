from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.ptw import PermitCreate, PermitUpdate, PermitResponse
from app.services.ptw_service import (
    create_permit, get_permits, get_permit,
    update_permit, delete_permit, get_permit_stats,
)
from app.agents.hse_analyzer import assess_permit_risk
import uuid

router = APIRouter(prefix="/permits", tags=["permits"])

@router.post("/", response_model=PermitResponse, status_code=status.HTTP_201_CREATED)
async def create(data: PermitCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_permit(db, user.id, data)

@router.get("/", response_model=list[PermitResponse])
async def list_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_permits(db, skip, limit)

@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_permit_stats(db)

@router.get("/{permit_id}", response_model=PermitResponse)
async def get_one(permit_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    permit = await get_permit(db, permit_id)
    if not permit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return permit

@router.put("/{permit_id}", response_model=PermitResponse)
async def update(permit_id: uuid.UUID, data: PermitUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    permit = await update_permit(db, permit_id, data)
    if not permit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return permit

@router.post("/{permit_id}/approve", response_model=PermitResponse)
async def approve(permit_id: uuid.UUID, issuer: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    permit = await get_permit(db, permit_id)
    if not permit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    risk = assess_permit_risk(permit.work_type, permit.risk_assessment)
    if risk["risk_level"] == "critical":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot approve critical risk permit without additional controls")
    return await update_permit(db, permit_id, PermitUpdate(status="approved", permit_issuer=issuer))

@router.post("/{permit_id}/reject", response_model=PermitResponse)
async def reject(permit_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await update_permit(db, permit_id, PermitUpdate(status="cancelled"))

@router.delete("/{permit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(permit_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    ok = await delete_permit(db, permit_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
