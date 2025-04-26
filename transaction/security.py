from fastapi import Depends, HTTPException, Header, status

from .conf import API_KEY

def api_key_verification(Autorization: str = Header(...)) -> str:
    if Autorization != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return Autorization
