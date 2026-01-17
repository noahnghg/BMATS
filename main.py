from fastapi import FastAPI
from app.resumes import router as resumes_router

app = FastAPI(
    title="HackTheBias API",
    description="API for parsing, anonymizing, and analyzing resumes to reduce hiring bias.",
    version="0.1.0"
)

# Include Routers
app.include_router(resumes_router)

@app.get("/")
async def root():
    return {"message": "Welcome to HackTheBias API. Visit /docs for documentation."}
