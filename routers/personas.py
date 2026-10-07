from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Persona
from schemas import Persona as PersonaSchema, PersonaCreate
from .deps import get_current_user

router = APIRouter(prefix="/personas", tags=["personas"])

@router.get("/", response_model=List[PersonaSchema])
def read_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Persona).offset(skip).limit(limit).all()

@router.post("/", response_model=PersonaSchema, status_code=status.HTTP_201_CREATED)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_persona = Persona(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@router.get("/{id_persona}", response_model=PersonaSchema)
def read_persona(id_persona: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_persona
