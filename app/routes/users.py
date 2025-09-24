from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, crud, database, auth

router = APIRouter(prefix="/users", tags=["Users"])

# ==========================
# Register a new user
# ==========================
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


# ==========================
# Login (JWT token)
# ==========================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = auth.create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


# ==========================
# Get current logged-in user
# ==========================
@router.get("/me", response_model=schemas.UserResponse)
def read_current_user(current_user = Depends(auth.get_current_user)):
    return current_user
