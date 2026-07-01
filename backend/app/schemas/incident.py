from pydantic import BaseModel
from typing import Any
from datetime import datetime

class IncidentCreate(BaseModel):
    title: str
    incident_type: str
    severity: str
    location: str
    description: str
    root_cause: list[Any] = []
    corrective_actions: list[Any] = []
    reported_by: str

class IncidentUpdate(BaseModel):
    status: str | None = None
    root_cause: list[Any] | None = None
    corrective_actions: list[Any] | None = None

class IncidentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    incident_type: str
    severity: str
    location: str
    description: str
    root_cause: list[Any]
    corrective_actions: list[Any]
    status: str
    reported_by: str
    created_at: datetime

    class Config:
        from_attributes = True
