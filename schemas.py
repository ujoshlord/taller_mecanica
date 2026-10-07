from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Persona
class PersonaBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[str] = None

class PersonaCreate(PersonaBase):
    pass

class Persona(PersonaBase):
    id_persona: int
    class Config:
        from_attributes = True

# Rol
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id_rol: int
    class Config:
        from_attributes = True

# Usuario
class UsuarioBase(BaseModel):
    id_persona: int
    id_rol: int
    alias: str

class UsuarioCreate(UsuarioBase):
    contrasenia: str

class Usuario(UsuarioBase):
    id_usuario: int
    activo: bool
    class Config:
        from_attributes = True

# Vehiculo
class VehiculoBase(BaseModel):
    id_cliente: int
    vin: Optional[str] = None
    placa: str
    marca: Optional[str] = None
    modelo: Optional[str] = None

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id_vehiculo: int
    class Config:
        from_attributes = True

# Producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    costo_compra: Decimal
    stock: int = 0

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id_producto: int
    fecha_compra: Optional[date]
    costo_venta: Optional[Decimal]
    disponible: Optional[bool]
    class Config:
        from_attributes = True

# Consulta
class ConsultaBase(BaseModel):
    id_vehiculo: int
    id_mecanico: Optional[int] = None
    sintoma: str
    problema: Optional[str] = None
    estado: str = 'En proceso'

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id_consulta: int
    fecha_hora_entrada: Optional[datetime]
    fecha_hora_salida: Optional[datetime]
    class Config:
        from_attributes = True

# Venta
class VentaBase(BaseModel):
    id_consulta: int
    id_repuesto: int
    cantidad: int
    precio_unitario: Decimal

class VentaCreate(VentaBase):
    pass

class Venta(VentaBase):
    id_venta: int
    subtotal: Optional[Decimal]
    class Config:
        from_attributes = True
