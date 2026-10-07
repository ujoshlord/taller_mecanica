from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Rol
from schemas import Rol as RolSchema, RolCreate
from .deps import get_current_user

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=List[RolSchema])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Rol).offset(skip).limit(limit).all()

@router.post("/", response_model=RolSchema, status_code=status.HTTP_201_CREATED)
def create_rol(rol: RolCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_rol = Rol(**rol.model_dump())
    db.add(db_rol)
    try:
        db.commit()
        db.refresh(db_rol)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="El rol ya existe u ocurrió un error")
    return db_rol
