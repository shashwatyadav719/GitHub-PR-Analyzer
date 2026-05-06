import httpx
from fastapi import HTTPException 

async def get_repo(github_token:str):
    request_url = "https://api.github.com/user/repos"

    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                request_url,
                headers=request_headers
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to GitHub"
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch repos from GitHub"
        )
    

    return response.json()   

async def get_pr(github_token:str,owner:str,repo:str):
    request_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }

    try: 
        async with httpx.AsyncClient() as client:
            response = await client.get(
                request_url,
                headers=request_headers
            )
        
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to GitHub"
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch PR files from GitHub"
        )
    
    return response.json()

async def get_pr_files(github_token:str,owner:str,repo:str,pr_number:int):
    request_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                request_url,
                headers=request_headers
            )
        
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to GitHub"
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch PR files from GitHub"
        )
    
    return response.json()

