from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.services.resume import ResumeProcessorService

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

class ResumeProcessedResponse(BaseModel):
    filename: str
    anonymized_text: str
    original_text_length: int

@router.post("/upload", response_model=ResumeProcessedResponse)
async def process_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a resume (PDF) to be parsed and anonymized.
    """
    result = ResumeProcessorService.process_resume(file)
    return result
