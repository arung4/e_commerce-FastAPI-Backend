from sqlalchemy.orm import Session
from .models import User, UserRole , PasswordResetToken
from .schemas import UserCreate , UserLogin , ResetPasswordRequest
from .utils import hash_password , verfiy_password, create_jwt_token
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from middlewares.utils import send_email
from datetime import datetime, timedelta
import secrets
import hashlib



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
    

    
def forgot_password(email:str, db: Session):
    
    user = db.query(User).filter(User.email == email).first()

    if not user: 
        raise HTTPException(status_code=404, detail="User not found")

    # generate token 
    token = secrets.token_urlsafe(32)    
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    expiration = datetime.now() + timedelta(minutes=15)

    # store token securely in DB
    reset_entry = PasswordResetToken(
        user_id = user.id,
        token = hashed_token, 
        expiration_time = expiration,
        used = False
    )
    db.add(reset_entry)
    db.commit()
    db.refresh(reset_entry)

    reset_link = f"http://localhost:3000/reset-password?token={token}"

    send_email(
        to_email = user.email,
        subject = "Reset your password",
        body = f"Click the following link to reset your password:\n\n{reset_link}\n\nThis link will expire in 15 minutes."
    )

    return {
        "message" : "Reset password email sent successfully"
    }


def reset_password(request: ResetPasswordRequest, db: Session):

    token = request.token 
    new_password = request.new_password

    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    # Extract the token data from DB
    token_data = db.query(PasswordResetToken).filter(
        PasswordResetToken.token ==hashed_token,
        PasswordResetToken.used == False
    ).first()

    if not token_data: 
        raise HTTPException(status_code = 400, detail = "Invalid or expired token")
    
    if token_data.expiration_time < datetime.now() : 
        raise HTTPException(status_code = 400, detail = "Token expired")
    
    user = db.query(User).filter(User.id == token_data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password = hash_password(new_password)
    # Mark token field used as True
    token_data.used = True
    db.commit()


    return {
        "message" : "Password reset successfully"
    }



