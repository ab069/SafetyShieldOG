from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.ptw import PermitToWork
from app.schemas.ptw import PermitCreate, PermitUpdate
import uuid

async def create_permit(db: AsyncSession, user_id: uuid.UUID, data: PermitCreate) -> PermitToWork:
    permit = PermitToWork(user_id=user_id, **data.model_dump())
    db.add(permit)
    await db.commit()
    await db.refresh(permit)
    return permit

async def get_permits(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[PermitToWork]:
    result = await db.execute(select(PermitToWork).order_by(PermitToWork.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

async def get_permit(db: AsyncSession, permit_id: uuid.UUID) -> PermitToWork | None:
    result = await db.execute(select(PermitToWork).where(PermitToWork.id == permit_id))
    return result.scalar_one_or_none()

async def update_permit(db: AsyncSession, permit_id: uuid.UUID, data: PermitUpdate) -> PermitToWork | None:
    permit = await get_permit(db, permit_id)
    if not permit:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(permit, key, val)
    await db.commit()
    await db.refresh(permit)
    return permit

async def delete_permit(db: AsyncSession, permit_id: uuid.UUID) -> bool:
    permit = await get_permit(db, permit_id)
    if not permit:
        return False
    await db.delete(permit)
    await db.commit()
    return True

async def get_permit_stats(db: AsyncSession) -> dict:
    total = await db.scalar(select(func.count(PermitToWork.id)))
    active = await db.scalar(select(func.count(PermitToWork.id)).where(PermitToWork.status == "active"))
    result = await db.execute(select(PermitToWork.work_type, func.count(PermitToWork.id)).group_by(PermitToWork.work_type))
    by_type = {row[0]: row[1] for row in result}
    return {"total": total or 0, "active": active or 0, "by_type": by_type}
