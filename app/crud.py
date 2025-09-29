from sqlalchemy.orm import Session
from . import models, schemas, auth

# ===== USERS =====
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# ===== NOTES =====
def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_user_notes(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()

def get_note_by_id(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def update_note(db: Session, note_id: int, note: schemas.NoteCreate, user_id: int):
    db_note = get_note_by_id(db, note_id)
    if db_note and db_note.owner_id == user_id:
        db_note.title = note.title
        db_note.content = note.content
        db.commit()
        db.refresh(db_note)
        return db_note
    return None

def delete_note(db: Session, note_id: int, user_id: int):
    db_note = get_note_by_id(db, note_id)
    if db_note and db_note.owner_id == user_id:
        db.delete(db_note)
        db.commit()
        return True
    return False


# ===== SHARING =====
def share_note(db: Session, note_id: int, shared_with_user: models.User, current_user_id: int):
    note = get_note_by_id(db, note_id)
    if note and note.owner_id == current_user_id:
        shared_entry = models.NoteSharing(
            note_id=note_id,
            owner_id=current_user_id,
            shared_with_id=shared_with_user.id
        )
        db.add(shared_entry)
        db.commit()
        db.refresh(shared_entry)
        return shared_entry
    return None

def get_shared_notes(db: Session, user_id: int):
    """Fetch notes shared with a user."""
    return db.query(models.Note).join(
        models.NoteSharing, models.Note.id == models.NoteSharing.note_id
    ).filter(
        models.NoteSharing.shared_with_id == user_id
    ).all()
