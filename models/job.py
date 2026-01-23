from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class JobCreate(BaseModel):
    """Model for creating a job (user_id comes from URL)"""
    title: str
    company: str
    description: str
    requirements: str

class Job(BaseModel):
    """Full job model including user_id"""
    id: Optional[str] = None
    title: str
    user_id: str
    company: str
    description: str
    requirements: str
    
    # New fields for external API integration
    organization_url: Optional[str] = None
    location: Optional[str] = None
    date_posted: Optional[datetime] = None
    salary: Optional[str] = None
    source_id: Optional[str] = None  # Original ID from external API
