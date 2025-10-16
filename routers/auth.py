from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from utils.security import get_password_hash, verify_password, create_access_token
from models.user import User
from utils.logger import get_logger
from schemas.user import UserCreate, UserLogin, UserRead
from services.database import get_db
from datetime import timedelta

router = APIRouter()
logger = get_logger(__name__)

class LoginRequest(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: EmailStr

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.info(f"Attempt to register existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"User registered: {db_user.email}")
        return db_user

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user:
            logger.warning(f"Login failed: email not found - {credentials.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not verify_password(credentials.password, user.password):
            logger.warning(f"Login failed: incorrect password for {credentials.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"User logged in: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
