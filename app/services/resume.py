from fastapi import UploadFile, HTTPException
from typing import Dict, Union, BinaryIO
from utils.parser import extract_text_from_pdf
from utils.anonymizer import anonymizer_instance

class ResumeProcessorService:
    @staticmethod
    def process_resume(file: UploadFile) -> Dict[str, any]:
        """
        Processes an uploaded resume file:
        1. Extracts text from PDF
        2. Anonymizes the text
        """
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")
        
        # Extract text directly from the file pointer
        try:
            raw_text = extract_text_from_pdf(file.file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")

        if not raw_text:
             raise HTTPException(status_code=400, detail="Could not extract text from the provided PDF.")

        # Anonymize
        anonymized_text = anonymizer_instance.anonymize_text(raw_text)

        return {
            "filename": file.filename,
            "original_text_length": len(raw_text),
            "anonymized_text": anonymized_text
        }
