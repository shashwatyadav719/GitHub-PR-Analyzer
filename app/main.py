from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.github import router as github_router
from app.routes.analysis import router as analysis_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(github_router)
app.include_router(analysis_router)


@app.get("/")
def root():
    return {"message": "hello world"}