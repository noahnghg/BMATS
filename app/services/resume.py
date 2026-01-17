from utils.parser import extract_text_from_pdf 
from utils.anonymizer import anonymizer_instance 
from utils.semantics import semantics_instance 
from fastapi import HTTPException, UploadFile

class ResumeService:

    @staticmethod
    def NLP_pipeline(file: UploadFile) -> dict:
        """
        Full NLP pipeline for resume processing:
        1. Parse PDF to extract raw text
        2. Anonymize the text (remove PII)
        3. Extract entities (skills, experience, education)
        4. Return processed results
        """
        # Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")
        
        # Step 1: Parse PDF
        try:
            raw_text = extract_text_from_pdf(file.file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")

        if not raw_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the provided PDF.")

        # Step 2: Anonymize
        anonymized_text = anonymizer_instance.anonymize_text(raw_text)

        # Step 3: Extract entities using semantics module
        extracted_entities = semantics_instance._extract_entities(anonymized_text)

        return extracted_entities