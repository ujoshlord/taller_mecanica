from fastapi import FastAPI
from routers import auth, personas, roles, usuarios, vehiculos, productos, consultas, ventas

app = FastAPI(title="API Taller Mecánico")

# Incluir routers
app.include_router(auth.router)
app.include_router(personas.router)
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(vehiculos.router)
app.include_router(productos.router)
app.include_router(consultas.router)
app.include_router(ventas.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Taller Mecánico"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)