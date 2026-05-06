import httpx
from app.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from fastapi import HTTPException



async def get_token(code:str):
    token_url = "https://github.com/login/oauth/access_token"

    request_data = {"client_id":GITHUB_CLIENT_ID,"client_secret":GITHUB_CLIENT_SECRET,"code":code}

    request_header = {
        "accept":"application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                token_url,
                data=request_data,
                headers=request_header
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Unable to connect to GitHub. "
        )

    token_data = response.json()

    if "access_token" not in token_data:
        raise HTTPException(
            status_code=400,
            detail="Failed to retrieve GitHub access token"
        )
    
    return token_data

async def get_user(access_token:str):
    user_url = "https://api.github.com/user"

    request_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                user_url,
                headers=request_headers
            )
        
    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail="Unable to connect to GitHub. b"
        )

    try:
        user_data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="Invalid response from GitHub user API"
        )

    
    
    return user_data


 
