from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Resume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None  # For future multi-user support
    filename: str
    anonymized_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
