# backend/src/domain/entities/candidate.py
from typing import List, Optional

from pydantic import BaseModel


class CandidateBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    birthdate: Optional[str] = None


class CandidateCreate(CandidateBase):
    cv_content: str


class CandidateResponse(CandidateBase):
    id: int
    education: Optional[str]
    job_history: Optional[str]
    skills: List[str]
    score: Optional[int]

    class Config:
        orm_mode = True
