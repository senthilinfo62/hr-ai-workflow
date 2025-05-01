from fastapi import UploadFile, HTTPException
import magic
import os

# Maximum file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Allowed MIME types
ALLOWED_MIME_TYPES = [
    'application/pdf'
]

async def validate_file(file: UploadFile):
    """
    Validate the uploaded file:
    - Check if file exists
    - Check file size
    - Check file type
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Read the file content
    content = await file.read()
    
    # Reset file position after reading
    await file.seek(0)
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)}MB")
    
    # Check file type using python-magic
    mime_type = magic.from_buffer(content, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415, 
            detail=f"Unsupported file type: {mime_type}. Only PDF files are allowed."
        )
    
    return content
