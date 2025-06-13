from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse, UserWithMessage, UserLoginResponse, UserLogin
from fastapi import APIRouter , Depends
from fastapi.security import OAuth2PasswordRequestForm
from config.database import  get_db
from .crud import create_user , get_users ,get_user, login , forgot_password, reset_password
from .utils import get_current_user
from .schemas import User , ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup",response_model=UserWithMessage)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db = db, user=user)

@router.post("/login", response_model=UserLoginResponse)
async def create_login_endpoint(login_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)): 
    return login(db=db,login_data = login_data)

@router.post("/forgot-password", status_code = 200)
async def forgot_password_endpoint(request:ForgotPasswordRequest, db : Session = Depends(get_db)): 
    return forgot_password(request.email,db)

@router.post("/reset-password", status_code = 200)
async def reset_password_endpoint(request: ResetPasswordRequest, db : Session = Depends(get_db)): 
   return reset_password(request,db)


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id,db: Session = Depends(get_db), current_user:User = Depends(get_current_user)): 
    return get_user(db,user_id,current_user)

@router.get("/users/", response_model=list[UserResponse])
async def read_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 100 ):
    return get_users(db,current_user, skip=skip, limit=limit)


    