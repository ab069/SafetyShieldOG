from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.observation import ObservationCreate, ObservationUpdate, ObservationResponse
from app.services.observation_service import (
    create_observation, get_observations, get_observation,
    update_observation, delete_observation, get_observation_stats,
)
import uuid

router = APIRouter(prefix="/observations", tags=["observations"])

@router.post("/", response_model=ObservationResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ObservationCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_observation(db, user.id, data)

@router.get("/", response_model=list[ObservationResponse])
async def list_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_observations(db, skip, limit)

@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_observation_stats(db)

@router.get("/{obs_id}", response_model=ObservationResponse)
async def get_one(obs_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    obs = await get_observation(db, obs_id)
    if not obs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obs

@router.put("/{obs_id}", response_model=ObservationResponse)
async def update(obs_id: uuid.UUID, data: ObservationUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    obs = await update_observation(db, obs_id, data)
    if not obs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obs

@router.delete("/{obs_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(obs_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    ok = await delete_observation(db, obs_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
