from fastapi import APIRouter 
from models.job import Job 
from app.services.job import JobService 

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.post("/")
async def create_job(job: Job):
    return JobService.create_job(job)

@router.get("/")
async def get_all_jobs():
    return JobService.get_all_jobs() 
