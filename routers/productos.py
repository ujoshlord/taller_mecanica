from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Producto
from schemas import Producto as ProductoSchema, ProductoCreate
from .deps import get_current_user

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/", response_model=List[ProductoSchema])
def obtener_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Producto).offset(skip).limit(limit).all()

@router.post("/", response_model=ProductoSchema, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    nuevo_producto = Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto
