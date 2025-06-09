from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse, UserWithMessage, UserLoginResponse, UserLogin
from fastapi import APIRouter , Depends
from fastapi.security import OAuth2PasswordRequestForm
from config.database import  get_db
from .crud import create_user , get_users ,get_user, login

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup",response_model=UserWithMessage)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db = db, user=user)

@router.post("/login", response_model=UserLoginResponse)
async def create_login_endpoint(login_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)): 
    return login(db=db,login_data = login_data)

@router.post("/forgot-password", response_model=UserLoginResponse)
async def create_login_endpoint(login_data: UserLogin, db : Session = Depends(get_db)): 
    pass   # Deal at the end

@router.post("/reset-password", response_model=UserLoginResponse)
async def create_login_endpoint(login_data: UserLogin, db : Session = Depends(get_db)): 
   pass # Deal at the end 


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id,db: Session = Depends(get_db)): 
    return get_user(db,user_id)

@router.get("/users/", response_model=list[UserResponse])
async def read_users(db: Session = Depends(get_db),skip: int = 0, limit: int = 100 ):
    return get_users(db, skip=skip, limit=limit)


    