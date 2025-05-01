"""Tests for candidate schema."""
import pytest
from pydantic import ValidationError

from src.domain.schemas.candidate_schema import CandidateCreate, CandidateResponse


def test_candidate_create_valid():
    """Test creating a valid candidate."""
    candidate = CandidateCreate(name="John Doe", email="john@example.com")
    assert candidate.name == "John Doe"
    assert candidate.email == "john@example.com"


def test_candidate_create_invalid_name():
    """Test creating a candidate with an invalid name."""
    with pytest.raises(ValidationError):
        CandidateCreate(name="", email="john@example.com")
    
    with pytest.raises(ValidationError):
        CandidateCreate(name="J", email="john@example.com")  # Too short


def test_candidate_create_invalid_email():
    """Test creating a candidate with an invalid email."""
    with pytest.raises(ValidationError):
        CandidateCreate(name="John Doe", email="invalid-email")


def test_candidate_response():
    """Test candidate response model."""
    candidate = CandidateResponse(
        id=1,
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        city="New York",
        birthdate="1990-01-01",
        education="Bachelor's in Computer Science",
        job_history="Software Engineer at XYZ Corp",
        skills=["Python", "JavaScript", "SQL"],
        score=8
    )
    
    assert candidate.id == 1
    assert candidate.name == "John Doe"
    assert candidate.email == "john@example.com"
    assert candidate.phone == "123456789"
    assert candidate.city == "New York"
    assert candidate.birthdate == "1990-01-01"
    assert candidate.education == "Bachelor's in Computer Science"
    assert candidate.job_history == "Software Engineer at XYZ Corp"
    assert candidate.skills == ["Python", "JavaScript", "SQL"]
    assert candidate.score == 8
