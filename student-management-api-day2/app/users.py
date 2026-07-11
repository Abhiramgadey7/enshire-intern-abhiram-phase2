from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
import app.schemas as schemas
import app.auth as auth
from app.exceptions import DuplicateRegistrationException, InvalidCredentialsException

router = APIRouter(tags=["Users & Authentication"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise DuplicateRegistrationException()
    
    new_user = User(
        email=user_in.email,
        hashed_password=auth.hash_password(user_in.password),
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsException()
    
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: User = Depends(auth.get_current_user)):
    return current_user

@router.post("/admin-only-route", response_model=dict)
def admin_route(admin_user: User = Depends(auth.RoleChecker(["admin"]))):
    return {"status": "success", "message": f"Welcome Admin {admin_user.email}. System control authorized."}