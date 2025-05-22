from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Ryder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el usuario de Django
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, unique=True)
    licencia_conducir = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=[
        ('disponible', 'Disponible'),
        ('en_ruta', 'En Ruta'),
        ('inactivo', 'Inactivo')
    ], default='disponible')

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.estado}"

class Comercio(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, unique=True)
    tipo_negocio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, unique=True)
    ubicacion = models.CharField(max_length=255)  # Puede mejorarse con coordenadas GPS

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Pedido(models.Model):
    comercio = models.ForeignKey(Comercio, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    ryder = models.ForeignKey(Ryder, on_delete=models.SET_NULL, null=True, blank=True)  # Puede estar sin asignar inicialmente
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado')
    ], default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignado_manual = models.BooleanField(default=False)  # Indica si fue asignado manualmente
    fecha_entrega = models.DateTimeField(null=True, blank=True)  # Nuevo campo

    def tiempo_entrega(self):
        if self.fecha_entrega:
            return (self.fecha_entrega - self.fecha_creacion).total_seconds() / 60  # Minutos
        return None

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"
    