from etl.extract import JobExtractor
from etl.transform import JobTransformer
from etl.load import JobLoader

class JobPipeline:
    def __init__(self):
        self.extractor = JobExtractor()
        self.transformer = JobTransformer()
        self.loader = JobLoader()

    def run(self, title: str = "software engineer", location: str = "us", date: str = "any", pages: int = 1):
        """
        Runs the full ETL pipeline.
        """
        total_added = 0
        
        for i in range(pages):
            offset = i * 10 # Assuming 10 items per page default or similar
            
            print(f"--- Pipeline Step 1: Extract (Page {i+1}) ---")
            raw_jobs = self.extractor.fetch_jobs(title, location, date, offset)
            print(f"Extracted {len(raw_jobs)} items.")
            
            if not raw_jobs:
                break
                
            print(f"--- Pipeline Step 2: Transform ---")
            transformed_jobs = []
            for raw in raw_jobs:
                transformed = self.transformer.transform(raw)
                if transformed:
                    transformed_jobs.append(transformed)
            
            print(f"--- Pipeline Step 3: Load ---")
            added = self.loader.load_batch(transformed_jobs)
            total_added += added
            print(f"Loaded {added} new jobs from this batch.")
            
        print(f"=== ETL Pipeline Complete. Total New Jobs: {total_added} ===")

if __name__ == "__main__":
    pipeline = JobPipeline()
    pipeline.run(title="software engineer", location="San Francisco, CA")
