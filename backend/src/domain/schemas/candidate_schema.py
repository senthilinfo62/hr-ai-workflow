import re
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator


class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        if re.search(r'[<>{}[\]\\]', v):
            raise ValueError('Name contains invalid characters')
        return v.strip()

class CandidateResponse(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    birthdate: Optional[str] = None
    education: Optional[str] = None
    job_history: Optional[str] = None
    skills: List[str] = []
    score: Optional[int] = None
    
    class Config:
        orm_mode = True
