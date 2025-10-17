from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from services.database import get_db
from utils.security import verify_token, get_current_user
from models.user import User, UserRole
from services import config
from utils.logger import get_logger

# Configurar logging
logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def token_required(request: Request):
    # Extraer el token del encabezado Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = auth_header.split("Bearer ")[-1].strip()
    if not verify_token(token):
        logger.warning("Token inválido: sin 'sub'")
        raise HTTPException(status_code=403, detail="Invalid token")

    return token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Token inválido: sin 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            logger.warning(f"Usuario no encontrado: {email}")
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError as e:
        logger.error(f"Error al decodificar token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

def require_roles(*allowed_roles):
    def role_checker(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                logger.error(f"Error al decodificar token: {str(e)}")
                raise HTTPException(status_code=401, detail="Invalid token")

            user = db.query(User).filter(User.email == email).first()
            if user is None:
                logger.warning(f"Usuario no encontrado: {email}")
                raise HTTPException(status_code=401, detail="User not found")

            logger.info(f"Autorización :: usuario={user.email}, activo={user.is_active}, rol={user.role}")
            if not user.is_active:
                logger.warning(f"Acceso denegado: usuario inactivo ({user.email})")
                raise HTTPException(status_code=403, detail="Inactive user")
            if user.role not in allowed_roles:
                logger.warning(f"Acceso denegado: rol no permitido ({user.role})")
                raise HTTPException(status_code=403, detail="Access forbidden")

            return user
        except JWTError as e:
            logger.error(f"Error al decodificar token: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
    return role_checker
