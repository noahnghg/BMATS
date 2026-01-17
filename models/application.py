from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class ApplicationSubmit(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    userId: str 
    jobId: str 

class ApplicationStored(BaseModel): 
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    userId: str 
    jobId: str 
    finalScore: float 
    

