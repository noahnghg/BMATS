from fastapi import APIRouter 
from models.application import ApplicationSubmit 
from app.services.application import ApplicationService



router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)

@router.post("/")
async def create_application(application: ApplicationSubmit): 
    return ApplicationService.create_application(application)

@router.get("/{userId}")
async def get_applications_of_user(userId: str): 
    return ApplicationService.get_applications_of_user(userId)

