from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class Job(BaseModel):
    title: str
    company: str
    description: str
    requirements: str
