from typing import Dict, Any

class JobTransformer:
    @staticmethod
    def transform(api_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms external API job data into internal Job model format.
        """
        # Data validation
        if not isinstance(api_data, dict):
            return None
            
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
                if parts:
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

        # Map to Job model fields
        return {
            "title": api_data.get("title", "Untitled Position"),
            "company": api_data.get("organization", "Unknown Company"),
            "description": description,
            "requirements": "See detailed requirements on official listing.",
            "organization_url": api_data.get("organization_url"),
            "location": location,
            "date_posted": api_data.get("date_posted"),
            "salary": salary,
            "source_id": str(api_data.get("id")),
            "user_id": "external-system" 
        }
