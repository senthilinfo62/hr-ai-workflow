import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.cv_router import router as cv_router

app = FastAPI(title="HR AI Workflow API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cv_router, prefix="/api/cv", tags=["CV Processing"])

@app.get("/")
async def root():
    return {"message": "Welcome to HR AI Workflow API"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)