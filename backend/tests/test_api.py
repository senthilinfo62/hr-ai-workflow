"""Tests for API endpoints."""
import io
import json
import pytest
from unittest.mock import patch, MagicMock

from fastapi import UploadFile


def test_get_candidates(client):
    """Test getting all candidates."""
    # Mock the CVProcessor.get_all_candidates method
    with patch('src.infrastructure.ai.cv_processor.CVProcessor.get_all_candidates') as mock_get_all:
        # Set up the mock to return a list of candidates
        mock_get_all.return_value = [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "123456789",
                "city": "New York",
                "birthdate": "1990-01-01",
                "education": "Bachelor's in Computer Science",
                "job_history": "Software Engineer at XYZ Corp",
                "skills": ["Python", "JavaScript", "SQL"],
                "score": 8
            }
        ]
        
        # Make the request
        response = client.get("/api/cv/candidates")
        
        # Check the response
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "John Doe"


def test_create_candidate(client):
    """Test creating a candidate."""
    # Mock the validate_file function
    with patch('src.utils.file_validator.validate_file') as mock_validate:
        # Set up the mock to return some PDF content
        mock_validate.return_value = b"mock pdf content"
        
        # Mock the CVProcessor.process_cv method
        with patch('src.infrastructure.ai.cv_processor.CVProcessor.process_cv') as mock_process:
            # Set up the mock to return a candidate
            mock_process.return_value = {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "123456789",
                "city": "New York",
                "birthdate": "1990-01-01",
                "education": "Bachelor's in Computer Science",
                "job_history": "Software Engineer at XYZ Corp",
                "skills": ["Python", "JavaScript", "SQL"],
                "score": 8
            }
            
            # Create a test PDF file
            pdf_content = b"%PDF-1.5\nsome mock pdf content"
            
            # Make the request
            response = client.post(
                "/api/cv/candidates",
                files={"cv": ("test.pdf", pdf_content, "application/pdf")},
                data={"name": "John Doe", "email": "john@example.com"}
            )
            
            # Check the response
            assert response.status_code == 201
            assert response.json()["name"] == "John Doe"
            assert response.json()["email"] == "john@example.com"
