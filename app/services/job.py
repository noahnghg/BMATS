from typing import List, Optional
from models.job import Job
from core.database import add_job, get_job, get_all_jobs, search_jobs as db_search_jobs

class JobService:
    @staticmethod
    def create_job(data: Job) -> Job:
        """Creates a new job posting."""
        job = Job(
            title=data.title,
            company=data.company,
            description=data.description,
            requirements=data.requirements
        )
        return add_job(job)

    @staticmethod
    def get_all_jobs() -> List[Job]:
        """Returns all job postings."""
        return get_all_jobs()

    @staticmethod
    def get_job_by_id(job_id: str) -> Optional[Job]:
        """Returns a job by its ID."""
        return get_job(job_id)

    @staticmethod
    def search_jobs(query: str) -> List[Job]:
        """Searches jobs by title, company, or description."""
        if not query:
            return get_all_jobs()
        return db_search_jobs(query)
