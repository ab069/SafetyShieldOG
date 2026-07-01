import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class SafetyObservation(Base):
    __tablename__ = "observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    observation_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(String(20), default="open")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
