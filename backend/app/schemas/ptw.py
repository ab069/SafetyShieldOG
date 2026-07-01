from pydantic import BaseModel
from typing import Any
from datetime import datetime

class PermitCreate(BaseModel):
    permit_number: str
    job_description: str
    work_type: str
    location: str
    requester: str
    risk_assessment: list[Any] = []
    start_time: datetime
    end_time: datetime

class PermitUpdate(BaseModel):
    status: str | None = None
    permit_issuer: str | None = None
    risk_assessment: list[Any] | None = None

class PermitResponse(BaseModel):
    id: str
    user_id: str
    permit_number: str
    job_description: str
    work_type: str
    location: str
    requester: str
    risk_assessment: list[Any]
    permit_issuer: str | None
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
