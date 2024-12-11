from fastapi import APIRouter, HTTPException, requests
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

router = APIRouter()

# Modelos de datos
class CrearCitaRequest(BaseModel):
    fecha_inicio: str = Field(..., pattern=r"\d{4}-\d{2}-\d{2}")
    hora_inicio: str = Field(..., pattern=r"\d{2}:\d{2}")
    nombre_paciente: str
    celular_contacto: str
    motivo_consulta: str

class EditarCitaRequest(BaseModel):
    id_cita: str
    nueva_fecha: str
    nuevo_horario: str

class BuscarCitaRequest(BaseModel):
    nombre_paciente: str
    celular_contacto: str

class BorrarCitaRequest(BaseModel):
    id_cita: str

# Endpoints
@router.post("/crear_cita")
async def crear_cita(data: CrearCitaRequest):
    try:
        # Cálculo de fecha y hora final
        fecha_inicio = data.fecha_inicio
        hora_inicio = datetime.strptime(data.hora_inicio, "%H:%M")
        hora_fin = (hora_inicio + timedelta(minutes=45)).strftime("%H:%M")
        fecha_fin = fecha_inicio

        # Crear la respuesta para Make
        response = {
            "fecha_inicio": fecha_inicio,
            "hora_inicio": data.hora_inicio,
            "fecha_fin": fecha_fin,
            "hora_fin": hora_fin,  # Agregamos este campo
            "nombre_paciente": data.nombre_paciente,
            "celular_contacto": data.celular_contacto,
            "motivo_consulta": data.motivo_consulta,
        }

        return {"mensaje": "Datos calculados correctamente", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la cita: {e}")


@router.post("/buscar_cita")
async def buscar_cita(data: BuscarCitaRequest):
    try:
        # Simulación de respuesta desde Make (reemplazar con conexión real)
        response = {
            "mensaje": "Cita encontrada",
            "id": "cita123456",  # Ejemplo de ID
            "fecha_inicio": "2024-01-01",
            "hora_inicio": "10:00",
            "hora_fin": "10:45",
            "nombre_paciente": data.nombre_paciente,
            "celular_contacto": data.celular_contacto,
            "motivo_consulta": "Consulta de rutina"
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar la cita: {e}")

@router.put("/editar_cita")
async def editar_cita(data: EditarCitaRequest):
    try:
        # Simular consulta de la cita original (esto debería venir de una base de datos en un entorno real)
        cita_original = {
            "id_cita": data.id_cita,
            "nombre_paciente": "Juan Pérez",
            "celular_contacto": "1234567890",
            "motivo_consulta": "Consulta general"
        }

        # Cálculo de la nueva hora final
        nuevo_horario_inicio = datetime.strptime(data.nuevo_horario, "%H:%M")
        nuevo_horario_final = (nuevo_horario_inicio + timedelta(minutes=45)).strftime("%H:%M")

        # Combinar datos originales con los nuevos
        response = {
            "id_cita": cita_original["id_cita"],
            "nombre_paciente": cita_original["nombre_paciente"],
            "celular_contacto": cita_original["celular_contacto"],
            "motivo_consulta": cita_original["motivo_consulta"],
            "nueva_fecha_inicio": data.nueva_fecha,
            "nuevo_horario_inicio": data.nuevo_horario,
            "nuevo_horario_final": nuevo_horario_final,
            "event_id": "test-event-id-123"  # Este debería ser el ID real del evento en Google Calendar
        }

        return {"mensaje": "Datos de edición calculados correctamente", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al editar la cita: {e}")


@router.delete("/borrar_cita")
async def borrar_cita(data: BorrarCitaRequest):
    try:
        # Crear la respuesta para Make
        response = {
            "id_cita": data.id_cita,
        }

        return {"mensaje": "Cita eliminada correctamente", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al borrar la cita: {e}")
    


import requests  # Este es el módulo correcto para enviar solicitudes HTTP
from fastapi import HTTPException
from pydantic import BaseModel

# Define un modelo de datos para el Body
class ProbarWebhookRequest(BaseModel):
    accion: str

@router.post("/probar_webhook")
@router.put("/probar_webhook")
async def probar_webhook(data: ProbarWebhookRequest):
    # URLs de los webhooks en Make.com
    urls = {
        "crear_cita": "https://hook.us2.make.com/2cxrev8vuf72q5w439xv84s8trud47wc",
        "editar_cita": "https://hook.us2.make.com/gpt3tjk19o0azhk9h76r73czya2oekup",
        "buscar_cita": "https://hook.us2.make.com/63d3azdu80g1c543gyc70w4itxq98x9d",
        "borrar_cita": "https://hook.us2.make.com/rwviuvuh64guw13v3brhly6c2rgncn47"
    }

    # Verifica si la acción es válida
    accion = data.accion
    if accion not in urls:
        raise HTTPException(status_code=400, detail="Acción no válida")

    # Datos de prueba para cada acción
    payload = {}
    if accion == "crear_cita":
        payload = {
            "fecha_inicio": "2024-12-20",
            "hora_inicio": "10:00",
            "hora_fin": "10:45",
            "nombre_paciente": "Juan Pérez",
            "celular_contacto": "1234567890",
            "motivo_consulta": "Consulta general"
        }
    elif accion == "editar_cita":
        payload = {
                "id_cita": "test-id-123",
                "nombre_paciente": "Juan Pérez",
                "celular_contacto": "1234567890",
                "motivo_consulta": "Consulta general",
                "nueva_fecha_inicio": "2024-12-22",
                "nuevo_horario_inicio": "11:30",
                "nuevo_horario_final": "12:15",
                "event_id": "test-event-id-123"
            }
    elif accion == "buscar_cita":
        payload = {
            "nombre_paciente": "Juan Pérez",
            "celular_contacto": "1234567890"
        }
    elif accion == "borrar_cita":
        payload = {
            "id_cita": "test-id-123"
        }

    try:
        # Obtener la URL según la acción
        webhook_url = urls[accion]

        # Enviar los datos al webhook
        response = requests.post(webhook_url, json=payload)

        # Manejar la respuesta
        if response.status_code == 200:
            return {"mensaje": "Datos enviados correctamente al webhook", "respuesta": response.json()}
        else:
            return {
                "mensaje": "Error al enviar datos al webhook",
                "status_code": response.status_code,
                "response": response.text
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar datos al webhook: {e}")
