from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from app.services.resume import ResumeService
from app.services.application import ApplicationService

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

@router.post("/upload")
async def upload_and_store_resume(file: UploadFile = File(...)):
    """
    Upload a resume (PDF) to be parsed, anonymized, and stored.
    Returns the resume_id for later use when applying to jobs.
    """
    extracted_text = ResumeService.NLP_pipeline(file)
    return extracted_text




 

