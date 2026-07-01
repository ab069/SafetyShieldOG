from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.observation import SafetyObservation
from app.schemas.observation import ObservationCreate, ObservationUpdate
import uuid

async def create_observation(db: AsyncSession, user_id: uuid.UUID, data: ObservationCreate) -> SafetyObservation:
    obs = SafetyObservation(user_id=user_id, **data.model_dump())
    db.add(obs)
    await db.commit()
    await db.refresh(obs)
    return obs

async def get_observations(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[SafetyObservation]:
    result = await db.execute(select(SafetyObservation).order_by(SafetyObservation.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

async def get_observation(db: AsyncSession, obs_id: uuid.UUID) -> SafetyObservation | None:
    result = await db.execute(select(SafetyObservation).where(SafetyObservation.id == obs_id))
    return result.scalar_one_or_none()

async def update_observation(db: AsyncSession, obs_id: uuid.UUID, data: ObservationUpdate) -> SafetyObservation | None:
    obs = await get_observation(db, obs_id)
    if not obs:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(obs, key, val)
    await db.commit()
    await db.refresh(obs)
    return obs

async def delete_observation(db: AsyncSession, obs_id: uuid.UUID) -> bool:
    obs = await get_observation(db, obs_id)
    if not obs:
        return False
    await db.delete(obs)
    await db.commit()
    return True

async def get_observation_stats(db: AsyncSession) -> dict:
    total = await db.scalar(select(func.count(SafetyObservation.id)))
    open_count = await db.scalar(select(func.count(SafetyObservation.id)).where(SafetyObservation.status == "open"))
    result = await db.execute(select(SafetyObservation.category, func.count(SafetyObservation.id)).group_by(SafetyObservation.category))
    by_category = {row[0]: row[1] for row in result}
    return {"total": total or 0, "open": open_count or 0, "by_category": by_category}
