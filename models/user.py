from sqlalchemy import Column, Integer, String, Boolean, Enum
from services.database import Base
import enum

class UserRole(str, enum.Enum):
    admsys = "admsys"
    sysoper = "sysoper"
    opera = "opera"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.opera)
