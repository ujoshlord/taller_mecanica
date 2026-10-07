from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Venta, Producto, Consulta
from schemas import Venta as VentaSchema, VentaCreate
from .deps import get_current_user

router = APIRouter(prefix="/ventas", tags=["ventas"])

@router.get("/", response_model=List[VentaSchema])
def obtener_ventas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Venta).offset(skip).limit(limit).all()

@router.post("/", response_model=VentaSchema, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Verificar que exista la consulta
    consulta = db.query(Consulta).filter(Consulta.id_consulta == venta.id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    # Verificar stock
    producto = db.query(Producto).filter(Producto.id_producto == venta.id_repuesto).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if producto.stock < venta.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    # Restar stock
    producto.stock -= venta.cantidad

    nueva_venta = Venta(**venta.model_dump())
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta
