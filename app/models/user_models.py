from app.db.db import Base
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    ADMIN= "ADMIN",
    USER= "USER"

class UserCreateModel(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole = UserRole.USER

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True,nullable=False, index=True)
    password = Column(String,nullable=False)
    email = Column(String, unique=True, nullable=False,index=True)
    role = Column(SAEnum(UserRole,name="user_role"), nullable=False, default= UserRole.USER)

class UserLoginModel(BaseModel):
    email:EmailStr
    password:str = Field(min_length=8)