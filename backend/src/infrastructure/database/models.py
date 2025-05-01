# backend/src/infrastructure/database/models.py
from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50))
    city = Column(String(100))
    birthdate = Column(String(50))
    education = Column(Text)
    job_history = Column(Text)
    skills = Column(JSON)
    score = Column(Integer)
