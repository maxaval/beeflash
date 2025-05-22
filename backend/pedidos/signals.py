from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido
from .utils import enviar_notificacion, enviar_notificacion_fcm

@receiver(post_save, sender=Pedido)
def notificar_cambio_estado(sender, instance, **kwargs):
    if instance.estado == "en_camino":
        mensaje = f"🚀 Tu pedido #{instance.id} está en camino con el Ryder {instance.ryder.nombre}."
    elif instance.estado == "entregado":
        mensaje = f"✅ Tu pedido #{instance.id} ha sido entregado. ¡Gracias por confiar en Bee Flash!"
    
    if instance.cliente:
        enviar_notificacion(instance.cliente.telefono, mensaje)
    if instance.comercio:
        enviar_notificacion(instance.comercio.telefono, f"📦 Actualización del pedido #{instance.id}: {mensaje}")

@receiver(post_save, sender=Pedido)
def notificar_pedido_fcm(sender, instance, **kwargs):
    if instance.estado == "en_camino":
        titulo = "Pedido en camino 🚀"
        cuerpo = f"Tu pedido #{instance.id} está en camino con {instance.ryder.nombre}."
    elif instance.estado == "entregado":
        titulo = "Pedido entregado ✅"
        cuerpo = f"Tu pedido #{instance.id} ha sido entregado."

    if instance.cliente and instance.cliente.fcm_token:
        enviar_notificacion_fcm(instance.cliente.fcm_token, titulo, cuerpo)
    if instance.comercio and instance.comercio.fcm_token:
        enviar_notificacion_fcm(instance.comercio.fcm_token, f"📦 Actualización del pedido", cuerpo)
        