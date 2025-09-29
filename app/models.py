from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    notes = relationship("Note", back_populates="owner")
    shared_notes = relationship("NoteSharing", back_populates="shared_with_user")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")
    shared_with = relationship("NoteSharing", back_populates="note")


class NoteSharing(Base):
    __tablename__ = "note_sharing"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"))
    shared_with_id = Column(Integer, ForeignKey("users.id"))

    note = relationship("Note", back_populates="shared_with")
    shared_with_user = relationship("User", back_populates="shared_notes")
