from sqlmodel import Session, select
from core.database import engine, Job, add_job
from typing import Dict, Any

class JobLoader:
    def __init__(self):
        self.engine = engine

    def load_job(self, job_data: Dict[str, Any]) -> bool:
        """
        Loads a single job into the database if it doesn't already exist.
        Returns True if loaded, False if skipped.
        """
        if not job_data:
            return False

        source_id = job_data.get("source_id")
        
        with Session(self.engine) as session:
            # Check for duplicates using source_id
            if source_id:
                existing = session.exec(select(Job).where(Job.source_id == source_id)).first()
                if existing:
                    return False
            
            # Create and save job
            db_job = Job(**job_data)
            session.add(db_job)
            session.commit()
            return True
            
    def load_batch(self, jobs_data: list) -> int:
        """
        Loads a batch of jobs. Returns count of new jobs added.
        """
        count = 0
        for job in jobs_data:
            if self.load_job(job):
                count += 1
        return count
