# backend/src/presentation/api/cv_router.py
import logging
from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import EmailStr

from src.domain.schemas.candidate_schema import CandidateCreate, CandidateResponse
from src.infrastructure.ai.cv_processor import CVProcessor
from src.utils.file_validator import validate_file

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/candidates", response_model=CandidateResponse, status_code=201)
async def create_candidate(
    name: str = Form(...),
    email: EmailStr = Form(...),
    cv: UploadFile = File(...),
):
    try:
        # Validate candidate data
        candidate_data = CandidateCreate(name=name, email=email)

        # Validate file
        contents = await validate_file(cv)

        # Process CV
        processor = CVProcessor()
        result = await processor.process_cv(
            name=candidate_data.name, email=candidate_data.email, pdf_content=contents
        )

        return result
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        # Re-raise HTTP exceptions
        logger.error(f"HTTP error: {e.detail}")
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/candidates", response_model=List[CandidateResponse])
async def get_candidates():
    try:
        # Get all candidates
        processor = CVProcessor()
        candidates = await processor.get_all_candidates()
        return candidates
    except Exception as e:
        logger.error(f"Error fetching candidates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch candidates")
