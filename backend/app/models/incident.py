import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from app.core.database import Base

class HSEIncident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    incident_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    root_cause = Column(JSON, default=list)
    corrective_actions = Column(JSON, default=list)
    status = Column(String(20), default="reported")
    reported_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
