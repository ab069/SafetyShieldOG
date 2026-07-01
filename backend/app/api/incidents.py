from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.incident import IncidentCreate, IncidentUpdate, IncidentResponse
from app.services.incident_service import (
    create_incident, get_incidents, get_incident,
    update_incident, delete_incident, get_incident_stats,
)
from app.agents.hse_analyzer import analyze_incident_trends
import uuid

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create(data: IncidentCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_incident(db, user.id, data)

@router.get("/", response_model=list[IncidentResponse])
async def list_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_incidents(db, skip, limit)

@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_incident_stats(db)

@router.get("/trends")
async def trends(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    incidents = await get_incidents(db, limit=200)
    return analyze_incident_trends(incidents)

@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_one(incident_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    incident = await get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return incident

@router.put("/{incident_id}", response_model=IncidentResponse)
async def update(incident_id: uuid.UUID, data: IncidentUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    incident = await update_incident(db, incident_id, data)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return incident

@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(incident_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    ok = await delete_incident(db, incident_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
