from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.github import router as github_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(github_router)

# Add analysis router with error handling
analysis_available = False
try:
    from app.routes.analysis import router as analysis_router
    app.include_router(analysis_router)
    analysis_available = True
except ImportError as e:
    print(f"Warning: Analysis routes unavailable: {e}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "auth": "available",
            "github": "available", 
            "analysis": "available" if analysis_available else "unavailable"
        }
    }


@app.get("/")
def root():
    return {"message": "hello world"}