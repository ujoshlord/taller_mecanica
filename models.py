from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, DateTime, Date, ForeignKey, CheckConstraint, text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Persona(Base):
    __tablename__ = "personas"
    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100))

class Rol(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey("personas.id_persona", ondelete="CASCADE"), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False) 
    alias = Column(String(50), unique=True, nullable=False)
    contrasenia = Column(String(255), nullable=False)
    token = Column(String(255), unique=True)
    activo = Column(Boolean, default=True)

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id_vehiculo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("personas.id_persona", ondelete="RESTRICT"), nullable=False)
    vin = Column(String(50), unique=True)
    placa = Column(String(20), unique=True, nullable=False)
    marca = Column(String(50))
    modelo = Column(String(50))

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_compra = Column(Date, default=datetime.utcnow)
    costo_compra = Column(Numeric(10, 2), nullable=False)
    # costo_venta es GENERATED ALWAYS, SQLAlchemy no necesita insertarlo, pero se define para mapeo
    costo_venta = Column(Numeric(10, 2), server_default=text("(costo_compra * 1.3)"))
    stock = Column(Integer, default=0, nullable=False)
    disponible = Column(Boolean, server_default=text("(stock > 0)"))

class Consulta(Base):
    __tablename__ = "consultas"
    id_consulta = Column(Integer, primary_key=True, index=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo", ondelete="CASCADE"), nullable=False)
    id_mecanico = Column(Integer, ForeignKey("usuarios.id_usuario"))
    sintoma = Column(Text, nullable=False)
    problema = Column(Text)
    fecha_hora_entrada = Column(DateTime, default=datetime.utcnow)
    fecha_hora_salida = Column(DateTime)
    estado = Column(String(20), default='En proceso')

class Venta(Base):
    __tablename__ = "ventas"
    id_venta = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consultas.id_consulta", ondelete="CASCADE"), nullable=False)
    id_repuesto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Integer, CheckConstraint('cantidad > 0'), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), server_default=text("(cantidad * precio_unitario)"))
