import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token

def verify_access_token(token: str):
    try:
        decoded_payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        return decoded_payload

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token"
        )
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)