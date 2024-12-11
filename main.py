from fastapi import FastAPI
from routes.appointments import router as appointments_router

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir las rutas de las citas
app.include_router(appointments_router)

# Mensaje de bienvenida en la raíz del servidor
@app.get("/")
async def root():
    return {"mensaje": "¡Bienvenido al backend de Dany, asistente virtual del Dr. Wilfrido Alarcón!"}
