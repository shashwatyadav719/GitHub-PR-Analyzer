from fastapi import APIRouter,HTTPException
from fastapi.responses import RedirectResponse
from app.config import GITHUB_CLIENT_ID
from app.services.auth_service import get_token,get_user
from app.utils.jwt_handler import create_access_token
from app.schemas.auth import AuthResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
                                                                                                                                                                                                                     
                                                      

@router.get("/login")
async def github_login():
    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
    )

    return RedirectResponse(url=github_url)



@router.get("/callback",response_model=AuthResponse)
async def github_callback(code: str):
    """Handle GitHub OAuth callback and return JWT token"""
    
    if not code:
        raise HTTPException(
            status_code=400,
            detail="Authorization code is missing"
        )

    try:
        token_data = await get_token(code)
        
        if "access_token" not in token_data:
            raise HTTPException(
                status_code=400,
                detail="Invalid token response from GitHub"
            )
            
        github_token = token_data["access_token"]
        
        user_data = await get_user(github_token)

        github_user_id = user_data.get("id")
        username = user_data.get("login")

        if not github_user_id or not username:
            raise HTTPException(
                status_code=400,
                detail="Invalid user data received from GitHub"
            )

        jwt_token = create_access_token({
            "github_user_id": github_user_id,
            "github_token": github_token
        })

        return {
            "access_token": jwt_token,
            "user": username
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions from service layer
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Authentication failed: {str(e)}"
        )
