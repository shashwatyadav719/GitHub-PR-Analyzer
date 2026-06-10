import httpx
from fastapi import HTTPException
import asyncio
from app.services.cache_service import repo_context_cache



def build_cache_key(owner: str, repo: str):
    return f"{owner}/{repo}"



async def get_repo_readme(github_token: str, owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to GitHub"
        )

    if response.status_code == 404:
        return None

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch README"
        )

    return response.text

async def get_repo_structure(github_token: str, owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"

    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    try:
        async with httpx.AsyncClient() as client:

            response = await client.get(url, headers=headers)
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to GitHub"
        )

    if response.status_code != 200:
        return None

    data = response.json()
    tree = data.get("tree", [])

    structure = []

    for item in tree:
        path = item.get("path")

        if not path:
            continue

        
        if any(skip in path for skip in [".git", "node_modules", "__pycache__"]):
            continue

        structure.append(path)

    return structure


async def get_repo_context(github_token: str, owner: str, repo: str):

    key = build_cache_key(owner, repo)

    if key in repo_context_cache:
        return repo_context_cache[key]
    
    readme,structure = await asyncio.gather(
        get_repo_readme(github_token, owner, repo),
        get_repo_structure(github_token, owner, repo)
    )
    

    context_parts = []

    if readme:
        context_parts.append(f"README:\n{readme}")

    if structure:
        structure_text = "\n".join(structure[:200])  
        context_parts.append(f"Project Structure:\n{structure_text}")

    if not context_parts:
        return None
    
    final_context = "\n\n".join(context_parts)

    
    repo_context_cache[key] = final_context

    return final_context 


