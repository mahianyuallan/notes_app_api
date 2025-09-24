from pydantic import BaseModel, EmailStr

# For user registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# For showing user info (response)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
