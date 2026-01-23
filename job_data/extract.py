import requests
import os
import dotenv
from typing import Dict, Any, List

dotenv.load_dotenv()

class JobExtractor:
    def __init__(self):
        self.api_key = os.getenv("RAPID_API_KEY")
        self.host_url = "https://internships-api.p.rapidapi.com/active-jb-7d"
        self.headers = {
            "x-rapidapi-host": "internships-api.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }

    def fetch_jobs(self, title: str = "software engineer", location: str = "us", date: str = "any", offset: int = 0) -> List[Dict[str, Any]]:
        """
        Fetches raw job data from the API.
        """
        params = {
            "title_filter": title,
            "location_filter": location,
            "date_filter": date,
            "offset": str(offset)
        }
        
        print(f"EXTRACT: Fetching jobs for query: '{title}' in '{location}'...")
        try:
            response = requests.get(self.host_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Normalize response to a list
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                if "job_postings" in data:
                    return data["job_postings"]
                elif "jobs" in data:
                    return data["jobs"]
                else:
                    # Fallback: assume dict values are jobs or it's a single page dict
                    # Using values() just in case it's id-keyed
                    return list(data.values())
            return []
            
        except Exception as e:
            print(f"EXTRACT ERROR: {e}")
            return []
