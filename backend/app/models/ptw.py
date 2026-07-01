import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from app.core.database import Base

class PermitToWork(Base):
    __tablename__ = "permits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    permit_number = Column(String(50), unique=True, nullable=False)
    job_description = Column(Text, nullable=False)
    work_type = Column(String(50), nullable=False)
    location = Column(String(255), nullable=False)
    requester = Column(String(255), nullable=False)
    risk_assessment = Column(JSON, default=list)
    permit_issuer = Column(String(255), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="requested")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
