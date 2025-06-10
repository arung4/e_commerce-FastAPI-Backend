from sqlalchemy.orm import Session
from .models import User, UserRole
from .schemas import UserCreate , UserLogin
from .utils import hash_password , verfiy_password, create_jwt_token
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm


def get_user(db: Session, user_id: int,current_user:User):

    if not current_user: 
        raise HTTPException(status_code=401, detail = "User not authenticated")
    
    if not current_user.role == "admin": 
        raise HTTPException(status_code =403, detail = "user not authorized")
    
    return db.query(User).filter(User.id == user_id).first()

# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()

def get_users(db: Session, current_user:User,skip: int = 0, limit: int = 10):

    if not current_user: 
        raise HTTPException(status_code=401, detail = "User not authenticated")
    if not current_user.role == "admin": 
        raise HTTPException(status_code =403, detail = "user not authorized")
    
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):

    # 1. Check if user alreadyexists 
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user: 
        raise HTTPException(status_code=400, detail = "User alredy exists with this email")
   
    # 2. Hash the password
    hashed_password = hash_password(user.password)
    
    # Handle role assignment
    try:
      role = user.role 
    except ValueError: 
        role = UserRole.user
   
   # Create user instance 
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        mobile=user.mobile,
        role= role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "user": new_user
    }

def login(db: Session, login_data: OAuth2PasswordRequestForm ): 
    user = db.query(User).filter(User.email == login_data.username).first()

    if not user: 
        raise HTTPException(status_code=400, detail="User not exists with this email and password")
    
    if not verfiy_password(login_data.password, user.password): 
        raise HTTPException(status_code=400,detail="Wrong password")
    
    token = create_jwt_token(data = {
                    "user_id": user.id,
                    "email":user.email,
                    "role":user.role.value

    })

    return {
        "message": "Login successful", 
        "access_token":token,
    }
    

    
