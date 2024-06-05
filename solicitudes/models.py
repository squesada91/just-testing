# Create your models here.
from django.db import models

class Solicitud(models.Model):
    TIPO_CHOICES = [
        ('Compra', 'Compra'),
        ('Vacaciones', 'Vacaciones'),
        ('Presupuesto', 'Presupuesto'),
    ]
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.tipo} - {self.estado}"
