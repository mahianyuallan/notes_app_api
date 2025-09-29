from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, database, auth, models

router = APIRouter(prefix="/notes", tags=["Notes"])

# Create a note
@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, 
                db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_note(db, note, current_user.id)

# Get notes (own + shared)
@router.get("/", response_model=List[schemas.NoteResponse])
def get_notes(db: Session = Depends(database.get_db), 
              current_user: models.User = Depends(auth.get_current_user)):
    own_notes = crud.get_user_notes(db, current_user.id)
    shared_notes = crud.get_shared_notes(db, current_user.id)
    return own_notes + shared_notes

# Update note
@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note: schemas.NoteCreate, 
                db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(auth.get_current_user)):
    updated = crud.update_note(db, note_id, note, current_user.id)
    if not updated:
        raise HTTPException(status_code=403, detail="Not authorized or note not found")
    return updated

# Delete note
@router.delete("/{note_id}")
def delete_note(note_id: int, 
                db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(auth.get_current_user)):
    success = crud.delete_note(db, note_id, current_user.id)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized or note not found")
    return {"detail": "Note deleted successfully"}

# Share note
@router.post("/share")
def share_note(request: schemas.ShareNoteRequest, 
               db: Session = Depends(database.get_db), 
               current_user: models.User = Depends(auth.get_current_user)):
    shared_with_user = crud.get_user_by_email(db, request.shared_with_email)
    if not shared_with_user:
        raise HTTPException(status_code=404, detail="User to share with not found")
    shared_entry = crud.share_note(db, request.note_id, shared_with_user, current_user.id)
    if not shared_entry:
        raise HTTPException(status_code=403, detail="Not authorized to share this note")
    return {"detail": f"Note shared with {request.shared_with_email}"}
