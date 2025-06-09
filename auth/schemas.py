from pydantic import BaseModel, EmailStr, field_validator
import re
from enum import Enum

class UserRole(str,Enum): 
    user = 'user'
    admin = 'admin'

class UserBase(BaseModel):
    email: EmailStr
    name: str
    mobile: str
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        if len(v) > 50:
            raise ValueError("Name must be less than 50 characters")
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError("Name can only contain letters and spaces")
        return v.title()  # Auto-capitalize names

    @field_validator('mobile')
    def validate_mobile(cls, v):
        if not v.isdigit():
            raise ValueError("Mobile must contain only digits")
        if len(v) != 10:
            raise ValueError("Mobile must be 10 digits")
        if v.startswith('0'):
            raise ValueError("Mobile cannot start with 0")
        # Indian number prefixes validation
        valid_prefixes = ['6', '7', '8', '9']
        if v[0] not in valid_prefixes:
            raise ValueError("Invalid Indian mobile number")
        return v

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.user
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError("Password must contain at least one special character")
        return v

class User(UserBase):
    id: int
    role: UserRole = UserRole.user

    class Config:
        from_attributes = True


# 2. Login reques schema 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 3. User response schema (excluding password)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: str
    role: UserRole

    class Config: 
        orm_mode = True  # for compatibility with SQLAlchemy models


class UserWithMessage(BaseModel): 
    message: str
    user: UserResponse
    

class UserLoginResponse(BaseModel): 
    message: str
    access_token: str