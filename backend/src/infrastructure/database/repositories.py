# backend/src/infrastructure/database/repositories.py
from sqlalchemy.orm import Session
from src.domain.entities.candidate import CandidateCreate

class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, candidate: CandidateCreate):
        db_candidate = CandidateModel(**candidate.dict())
        self.db.add(db_candidate)
        self.db.commit()
        self.db.refresh(db_candidate)
        return db_candidate