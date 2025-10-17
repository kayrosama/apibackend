from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from services.database import get_db
from utils.security import verify_token
from models.user import User, UserRole
from services import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def token_required(request: Request):
    # Extraer el token del encabezado Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = auth_header.split("Bearer ")[-1].strip()
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")

    return token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
def require_roles(*allowed_roles: UserRole):
    def role_checker(user: User = Depends(get_current_user)):
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Inactive user")
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
    