from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.incident import HSEIncident
from app.schemas.incident import IncidentCreate, IncidentUpdate
import uuid

async def create_incident(db: AsyncSession, user_id: uuid.UUID, data: IncidentCreate) -> HSEIncident:
    incident = HSEIncident(user_id=user_id, **data.model_dump())
    db.add(incident)
    await db.commit()
    await db.refresh(incident)
    return incident

async def get_incidents(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[HSEIncident]:
    result = await db.execute(select(HSEIncident).order_by(HSEIncident.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

async def get_incident(db: AsyncSession, incident_id: uuid.UUID) -> HSEIncident | None:
    result = await db.execute(select(HSEIncident).where(HSEIncident.id == incident_id))
    return result.scalar_one_or_none()

async def update_incident(db: AsyncSession, incident_id: uuid.UUID, data: IncidentUpdate) -> HSEIncident | None:
    incident = await get_incident(db, incident_id)
    if not incident:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(incident, key, val)
    await db.commit()
    await db.refresh(incident)
    return incident

async def delete_incident(db: AsyncSession, incident_id: uuid.UUID) -> bool:
    incident = await get_incident(db, incident_id)
    if not incident:
        return False
    await db.delete(incident)
    await db.commit()
    return True

async def get_incident_stats(db: AsyncSession) -> dict:
    total = await db.scalar(select(func.count(HSEIncident.id)))
    open_count = await db.scalar(select(func.count(HSEIncident.id)).where(HSEIncident.status.in_(["reported", "investigating"])))
    result = await db.execute(select(HSEIncident.severity, func.count(HSEIncident.id)).group_by(HSEIncident.severity))
    by_severity = {row[0]: row[1] for row in result}
    result2 = await db.execute(select(HSEIncident.incident_type, func.count(HSEIncident.id)).group_by(HSEIncident.incident_type))
    by_type = {row[0]: row[1] for row in result2}
    return {"total": total or 0, "open": open_count or 0, "by_severity": by_severity, "by_type": by_type}
