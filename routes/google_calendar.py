from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os

# Cargar las credenciales desde el archivo .env
GOOGLE_CALENDAR_CREDENTIALS_PATH = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_PATH")
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")
TIMEZONE = os.getenv("TIMEZONE", "America/Cancun")

def obtener_servicio_google_calendar():
    """
    Autentica y devuelve un servicio de Google Calendar listo para usar.
    """
    try:
        # Autenticar usando las credenciales JSON
        credentials = Credentials.from_service_account_file(
            GOOGLE_CALENDAR_CREDENTIALS_PATH,
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        service = build("calendar", "v3", credentials=credentials)
        return service
    except Exception as e:
        print(f"Error al autenticar con Google Calendar: {e}")
        raise
