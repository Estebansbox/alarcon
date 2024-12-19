from fastapi import FastAPI
from routes.appointments import router as appointments_router

# Crear la aplicación FastAP
app = FastAPI()

# Incluir las rutas de las citas
app.include_router(appointments_router)

# Mensaje de bienvenida en la raíz del servidor
@app.get("/")
async def root():
    return {"mensaje": "¡Bienvenido al backend de Dani, asistente virtual del Dr. Wilfrido Alarcón!"} 

# Cambio de prueba.
# Este es un cambio de prueba para Rende