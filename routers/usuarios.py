from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Usuario
from schemas import Usuario as UsuarioSchema, UsuarioCreate
from security import get_password_hash
from .deps import get_current_user

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[UsuarioSchema])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Usuario).offset(skip).limit(limit).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Este endpoint podría no requerir current_user si es para registro inicial, 
    # pero normalmente solo un admin crea usuarios. Lo dejaremos abierto para compatibilidad inicial.
    db_user = db.query(Usuario).filter(Usuario.alias == usuario.alias).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El alias ya está registrado")
    
    hashed_password = get_password_hash(usuario.contrasenia)
    nuevo_usuario = Usuario(
        id_persona=usuario.id_persona,
        id_rol=usuario.id_rol,
        alias=usuario.alias,
        contrasenia=hashed_password
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario creado exitosamente", "id_usuario": nuevo_usuario.id_usuario}

@router.patch("/{id_usuario}/baja")
def dar_baja_usuario(id_usuario: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.activo = False
    db.commit()
    return {"mensaje": "Usuario dado de baja"}
