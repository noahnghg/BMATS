from typing import List, Optional
from fastapi import HTTPException
from models.application import ApplicationSubmit, ApplicationStored
from core.database import add_application, get_applications_for_user, get_job, get_user, Application
from utils.semantics import semantics_instance

class ApplicationService:
    @staticmethod
    def create_application(application: ApplicationSubmit) -> Application:
        """
        Create an application:
        1. Fetch job details from jobId
        2. Fetch user data (skills, experience, education) from userId
        3. Calculate final score
        4. Store application
        """
        # Get job details
        job = get_job(application.jobId)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get user data
        user = get_user(application.userId)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Combine user data into a single string for scoring
        user_data = f"{user.skills} {user.experience} {user.education}"
        
        # Combine job details
        job_string = f"{job.title} {job.description} {job.requirements}"
        
        # Calculate score
        score = ApplicationService.calculate_final_score(job_string, user_data)
        
        # Create application record
        stored_app = Application(
            job_id=application.jobId,
            user_id=application.userId,
            score=score
        )
        
        return add_application(stored_app)

    @staticmethod 
    def get_applications_of_user(userId: str) -> List[dict]:
        """Get applications with job details for a user."""
        applications = get_applications_for_user(userId)
        result = []
        for app in applications:
            job = get_job(app.job_id)
            result.append({
                "id": app.id,
                "job_id": app.job_id,
                "user_id": app.user_id,
                "score": app.score,
                "job_title": job.title if job else "Unknown",
                "job_description": job.description if job else "",
                "job_company": job.company if job else "Unknown",
                "job_requirements": job.requirements if job else ""
            })
        return result

    @staticmethod 
    def calculate_final_score(job_string: str, user_data: str) -> float:
        return semantics_instance.get_final_score(job_string, user_data)