from pydantic import BaseModel
from datetime import datetime

class ObservationCreate(BaseModel):
    observation_type: str
    description: str
    location: str
    category: str

class ObservationUpdate(BaseModel):
    status: str | None = None

class ObservationResponse(BaseModel):
    id: str
    user_id: str
    observation_type: str
    description: str
    location: str
    category: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
