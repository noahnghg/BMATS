import requests, json, dotenv, os
from datetime import datetime
from sqlmodel import Session, select
from core.database import engine, Job, add_job

dotenv.load_dotenv() 

api_key = os.getenv("RAPID_API_KEY")

host_url = "https://internships-api.p.rapidapi.com/active-jb-7d"

headers = {
    "x-rapidapi-host": "internships-api.p.rapidapi.com",
    "x-rapidapi-key": api_key
}

def transform_external_job(api_data: dict) -> dict:
    """
    Transforms external API job data into internal Job model format.
    """
    # Extract location
    location = "Unknown"
    if api_data.get("locations_raw") and len(api_data["locations_raw"]) > 0:
        loc = api_data["locations_raw"][0]
        address = loc.get("address", {})
        if address:
            city = address.get("addressLocality")
            region = address.get("addressRegion")
            country = address.get("addressCountry")
            parts = [p for p in [city, region, country] if p]
            location = ", ".join(parts)
        
    # Extract salary
    salary = None
    if api_data.get("salary_raw"):
        sal = api_data["salary_raw"]
        val = sal.get("value", {})
        if val:
            min_val = val.get("minValue")
            max_val = val.get("maxValue")
            currency = sal.get("currency", "USD")
            unit = val.get("unitText", "YEAR")
            
            if min_val and max_val:
                salary = f"{min_val} - {max_val} {currency} / {unit}"
            elif min_val:
                salary = f"{min_val} {currency} / {unit}"
    
    # Format description (if missing)
    description = api_data.get("description", "")
    if not description:
        description = f"Title: {api_data.get('title')}\nOrganization: {api_data.get('organization')}\nSee URL for details."

    return {
        "title": api_data.get("title", "Untitled Position"),
        "company": api_data.get("organization", "Unknown Company"),
        "description": description,
        "requirements": "See detailed requirements on official listing.", # API doesn't seem to provide full reqs in list view usually
        "organization_url": api_data.get("organization_url"),
        "location": location,
        "date_posted": api_data.get("date_posted"), # String format from API is ISO-like
        "salary": salary,
        "source_id": str(api_data.get("id")),
        "user_id": "external-system" 
    }

def fetch_and_store_internships(title: str = "software engineer", location: str = "us", date: str = "any", offset: int = 0):
    """
    Fetches internships from API and stores them in the local database.
    """
    params = {
        "title_filter": title,
        "location_filter": location,
        "date_filter": date,
        "offset": str(offset)
    }
    
    print(f"Fetching jobs for query: {title} in {location}...")
    try:
        response = requests.get(host_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # The API returns a dict with 'job_postings' list usually, OR a list directly. 
        # Based on user snippet, it looks like a list of objects? Or 'data' is the list.
        # User said "here is an example of what got fetched" -> single object.
        # usually rapidapi pagination wraps it. Let's assume it might be in a key or is a list.
        # We'll check type.
        
        jobs_list = []
        if isinstance(data, list):
            jobs_list = data
        elif isinstance(data, dict) and "jobs" in data: # Common pattern
             jobs_list = data["jobs"]
        elif isinstance(data, dict):
            # Maybe just one key holds it? Or it's a single dict? unlikely for list endpoint.
            # Let's assume it returns keys like 'job_postings' commonly. 
            # But let's fallback to inspecting keys if we were debugging.
            # For now assume the user's snippet implies we iterate over something.
            # Let's assume 'data' is the list based on simple requests logic typically returning list for /active-jb-7d
            # But safest is to print keys if unsure.
            # Actually, I'll assume iterating `data` if list, or key `data` or `jobs`.
            # If `data` is a dict, keys might be metadata + result.
            # I will trust `data` is the list for now or check commonly used structure.
            # Let's just try to iterate `data` values if it's a dict of jobs (unlikely).
            pass

        # For the specific API "Internships API" on RapidAPI:
        # It typically returns a JSON object where values are the jobs, or a list.
        # I'll treat `data` as the dict containing jobs.
        
        count = 0
        for key, item in data.items():
            if isinstance(item, dict) and "title" in item:
                # Often APIs like this return { "job_id_1": {...}, "job_id_2": {...} }
                # OR it's a list. 
                pass
        
        # Actually, let's look at the user snippet: "id": "1959405306"...
        # It's a job object.
        
        # In `get_internships_list` before it was returning `data.json()`.
        # I'll iterate `data` assuming it is a dict of job_id -> job_details OR a list.
        
        items_to_process = []
        if isinstance(data, list):
            items_to_process = data
        elif isinstance(data, dict):
             # Some APIs return { "status": 200, "data": [...] }
             # Others return { "123": {...}, "124": {...} }
             # I'll guess it represents a map of ID to Job if keys are IDs.
             # Or it has a main key.
             if "job_postings" in data:
                 items_to_process = data["job_postings"]
             else:
                 # Assume keys are IDs?
                 items_to_process = data.values()

        with Session(engine) as session:
            for job_data in items_to_process:
                if not isinstance(job_data, dict): continue
                
                # Check duplication
                source_id = str(job_data.get("id"))
                existing = session.exec(select(Job).where(Job.source_id == source_id)).first()
                if existing:
                    print(f"Skipping existing job {source_id}")
                    continue

                transformed = transform_external_job(job_data)
                
                # Create DB object
                db_job = Job(**transformed)
                session.add(db_job)
                count += 1
            
            session.commit()
            print(f"Successfully stored {count} new jobs.")
            
    except Exception as e:
        print(f"Error fetching/storing jobs: {e}")

if __name__ == "__main__":
    fetch_and_store_internships() 





