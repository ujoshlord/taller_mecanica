from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import Consulta
from schemas import Consulta as ConsultaSchema, ConsultaCreate
from .deps import get_current_user

router = APIRouter(prefix="/consultas", tags=["consultas"])

@router.get("/", response_model=List[ConsultaSchema])
def obtener_consultas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Consulta).offset(skip).limit(limit).all()

@router.post("/", response_model=ConsultaSchema, status_code=status.HTTP_201_CREATED)
def crear_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    nueva_consulta = Consulta(**consulta.model_dump())
    db.add(nueva_consulta)
    db.commit()
    db.refresh(nueva_consulta)
    return nueva_consulta

@router.patch("/{id_consulta}/finalizar")
def finalizar_consulta(id_consulta: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    consulta = db.query(Consulta).filter(Consulta.id_consulta == id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    consulta.estado = 'Finalizado'
    consulta.fecha_hora_salida = datetime.utcnow()
    db.commit()
    db.refresh(consulta)
    return consulta
