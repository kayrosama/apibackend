from fastapi import Depends, HTTPException
from .utils.security import verify_token

def token_required(token: str = Depends(lambda: "fake-jwt-token")):
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
        