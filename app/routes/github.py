from fastapi import APIRouter,Depends,HTTPException
from app.utils.jwt_handler import get_current_user
from app.services.github_service import get_repo,get_pr,get_pr_files
from app.schemas.github import RepoResponse, PullRequestResponse

router = APIRouter(prefix="/github", tags=["GitHub"])

@router.get("/repos",response_model=list[RepoResponse])
async def get_repositories(current_user: dict = Depends(get_current_user)):
    github_token = current_user["github_token"]

    if not github_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    repositories = await get_repo(github_token)

    if not repositories:
        raise HTTPException(
            status_code=404,
            detail="No repositories found" 
        )
    

    return repositories

@router.get("/repos/{owner}/{repo}",response_model=list[PullRequestResponse])
async def get_pull_request(owner:str,repo:str,current_user: dict = Depends(get_current_user)):
    github_token = current_user["github_token"]

    pull_requests = await get_pr(github_token,owner,repo)  

    if not pull_requests:
        raise HTTPException(
            status_code=404,
            detail="No pull requests found"
        )

    prs = [
        {
            "number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "created_at": pr["created_at"],
            "author": pr["user"]["login"],
            "url": pr["html_url"]
        }
        for pr in pull_requests
    ]

    return prs

@router.get("/repos/{owner}/{repo}/{pr_number}")
async def fetch_pr_files(owner:str,repo:str,pr_number:int,current_user: dict = Depends(get_current_user)):
    github_token = current_user["github_token"]

    pr_files = await get_pr_files(github_token,owner,repo,pr_number)

    if not pr_files:
        raise HTTPException(
            status_code=404,
            detail="No files found in this PR"
        )

    return pr_files