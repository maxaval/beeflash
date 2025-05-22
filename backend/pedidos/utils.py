import requests
from django.conf import settings
from firebase_admin import messaging

WHATSAPP_API_URL = "https://api.whatsapp.com/send"
WHATSAPP_TOKEN = settings.WHATSAPP_BUSINESS_TOKEN

def enviar_notificacion(numero, mensaje):
    payload = {
        "phone": numero,
        "message": mensaje,
        "token": WHATSAPP_TOKEN
    }
    requests.post(WHATSAPP_API_URL, json=payload)

def enviar_notificacion_fcm(token, titulo, cuerpo):
    mensaje = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=cuerpo
        ),
        token=token
    )
    response = messaging.send(mensaje)
    print(f"Notificación enviada: {response}")
    