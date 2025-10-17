from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.security import get_password_hash, verify_password, create_access_token, require_roles, get_current_user
from models.user import User, UserRole
from utils.logger import get_logger
from schemas.user import UserCreate, UserLogin, UserRead
from services.database import get_db

router = APIRouter()
logger = get_logger(__name__)

@router.post("/register", response_model=UserRead)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admsys))  # ← aquí se valida y se pasa el usuario
):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        logger.info(f"Existing User: {existing_user}")
        if existing_user:
            logger.info(f"Attempt to register existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            password=hashed_password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"User registered: {db_user.email}")
        return db_user

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user or not verify_password(credentials.password, user.password):
            logger.warning(f"Login failed for {credentials.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"User logged in: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

