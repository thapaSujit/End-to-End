from fastapi import FastAPI
from src.api import router as api_router

# Initialize FastAPI
app = FastAPI()

# Include routes from the API router
app.include_router(api_router)

# Root endpoint to handle the "/" route
@app.get("/")
async def root():
    return {"message": "Welcome to the NEPSE Data Scraper API"}

# Run using: uvicorn src.main:app --reload