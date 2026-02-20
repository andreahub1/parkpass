from django.db import models
from django.utils import timezone
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class Boleto(models.Model):
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_entrada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    pagado = models.BooleanField(default=False)
    monto = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    qr_imagen = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_imagen:
            qr = qrcode.make(str(self.codigo))
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            self.qr_imagen.save(f'{self.codigo}.png', File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.codigo)
