"""Tests for file validator."""

import pytest
from fastapi import HTTPException

from src.utils.file_validator import validate_file


class MockUploadFile:
    """Mock UploadFile for testing."""

    def __init__(self, content, filename="test.pdf", content_type="application/pdf"):
        """Initialize with content."""
        self.filename = filename
        self._content_type = content_type
        self._content = content
        self._position = 0
        self.size = len(content)

    @property
    def content_type(self):
        """Get content type."""
        return self._content_type

    async def read(self):
        """Read content."""
        return self._content

    async def seek(self, position):
        """Seek to position."""
        self._position = position


@pytest.mark.asyncio
async def test_validate_file_valid():
    """Test validating a valid file."""
    # Create a mock PDF content
    content = b"%PDF-1.5\nsome mock pdf content"
    file = MockUploadFile(content)

    # This should not raise an exception
    result = await validate_file(file)
    assert result == content


@pytest.mark.asyncio
async def test_validate_file_too_large():
    """Test validating a file that's too large."""
    # Create a mock large file (6MB)
    content = b"x" * (6 * 1024 * 1024)
    file = MockUploadFile(content)

    # This should raise an HTTPException with status code 413
    with pytest.raises(HTTPException) as excinfo:
        await validate_file(file)

    assert excinfo.value.status_code == 413
    assert "File size exceeds the limit" in excinfo.value.detail


@pytest.mark.asyncio
async def test_validate_file_wrong_type():
    """Test validating a file with wrong type."""
    # Create a mock non-PDF file
    content = b"not a pdf file"
    file = MockUploadFile(content, filename="test.txt", content_type="text/plain")

    # This should raise an HTTPException with status code 415
    with pytest.raises(HTTPException) as excinfo:
        await validate_file(file)

    assert excinfo.value.status_code == 415
    assert "Unsupported file type" in excinfo.value.detail
