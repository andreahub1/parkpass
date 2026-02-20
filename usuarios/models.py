from django.db import models
from django.contrib.auth.models import User

class Pago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    codigo_qr = models.CharField(max_length=255)

    def __str__(self):
        return f"Pago de {self.usuario.username} - ${self.monto}"
