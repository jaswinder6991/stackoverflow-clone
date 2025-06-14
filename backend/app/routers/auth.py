from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from ..models import UserAuth, UserLogin, Token, User as PydanticUser
from ..db.db import get_db
from ..db.models import User as DBUser
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..data_service import DataService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

# Security configuration
SECRET_KEY = "your-secret-key-here"  # In production, use a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    data_service = DataService(db)
    user = data_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=PydanticUser)
async def register(user_data: UserAuth, db: Session = Depends(get_db)):
    data_service = DataService(db)
    
    try:
        # Check if username already exists
        if data_service.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Username already registered",
                    "field": "username",
                    "message": f"The username '{user_data.username}' is already taken"
                }
            )
        
        # Check if email already exists
        if data_service.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Email already registered",
                    "field": "email",
                    "message": f"The email '{user_data.email}' is already registered"
                }
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = data_service.create_user(
            name=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        return user
    except HTTPException:
        # Re-raise HTTP exceptions as they already have proper error details
        raise
    except Exception as e:
        # Log the unexpected error
        print(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Registration failed",
                "message": "An unexpected error occurred during registration. Please try again."
            }
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    data_service = DataService(db)
    print(f"Attempting login for username: {form_data.username}")
    
    user = data_service.get_user_by_username(form_data.username)
    print(f"User found: {user is not None}")
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "User not found",
                "message": f"No account found with username '{form_data.username}'. Please register first."
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    password_valid = verify_password(form_data.password, user.hashed_password)
    print(f"Password valid: {password_valid}")
    
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid password",
                "message": "The password you entered is incorrect. Please try again."
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me", response_model=PydanticUser)
async def get_current_user_info(current_user: DBUser = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user 