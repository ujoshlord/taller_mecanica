from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Vehiculo
from schemas import Vehiculo as VehiculoSchema, VehiculoCreate
from .deps import get_current_user

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])

@router.get("/", response_model=List[VehiculoSchema])
def obtener_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Vehiculo).offset(skip).limit(limit).all()

@router.post("/", response_model=VehiculoSchema, status_code=status.HTTP_201_CREATED)
def crear_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_vehiculo = db.query(Vehiculo).filter((Vehiculo.placa == vehiculo.placa) | (Vehiculo.vin == vehiculo.vin)).first()
    if db_vehiculo:
        raise HTTPException(status_code=400, detail="El vehículo (placa o vin) ya existe")
    
    nuevo_vehiculo = Vehiculo(**vehiculo.model_dump())
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo
