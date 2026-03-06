from django.http import JsonResponse
from django.utils import timezone
from .models import Boleto
from django.shortcuts import render, get_object_or_404


def buscar_boleto(request, uuid):
    try:
        boleto = Boleto.objects.get(codigo=uuid)

        # Calcular tiempo transcurrido
        ahora = timezone.now()
        tiempo = ahora - boleto.fecha_entrada

        minutos = tiempo.total_seconds() / 60
        horas = minutos / 60

        tarifa_por_hora = 20  # puedes cambiar esto

        monto_calculado = round(horas * tarifa_por_hora, 2)

        boleto.monto = monto_calculado
        boleto.save()

        return JsonResponse({
            "id": str(boleto.codigo),
            "monto": float(boleto.monto),
            "pagado": boleto.pagado
        })

    except Boleto.DoesNotExist:
        return JsonResponse({"error": "No existe"})


def procesar_pago(request, id):
    boleto = get_object_or_404(Boleto, id=id)
    metodo = request.GET.get("metodo")

    return render(request, "procesar_pago.html", {
        "boleto": boleto,
        "metodo": metodo
    })