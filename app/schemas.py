from typing import List, Optional
from pydantic import BaseModel, EmailStr

# User Schemas (already there)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Notes Schemas
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True


# Sharing Schema
class ShareNoteRequest(BaseModel):
    note_id: int
    shared_with_email: EmailStr
