from django.http import JsonResponse
from django.utils import timezone
from .models import Boleto
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json 

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


# 🔥 PAYPAL (CORREGIDO)
def pago_paypal(request, boleto_id):
    boleto = get_object_or_404(Boleto, codigo=boleto_id)

    # ✅ FORZAR FORMATO CORRECTO PARA PAYPAL
    monto = "{:.2f}".format(float(boleto.monto))

    return render(request, "usuarios/pago_paypal.html", {
        "monto": monto,
        "boleto_id": boleto.codigo
    })
    
# ✅ CONFIRMAR PAGO DESDE PAYPAL
@csrf_exempt
def confirmar_pago(request):
    if request.method == "POST":
        data = json.loads(request.body)
        boleto_id = data.get("boleto_id")

        try:
            boleto = Boleto.objects.get(codigo=boleto_id)
            boleto.pagado = True
            boleto.save()

            return JsonResponse({"status": "ok"})

        except Boleto.DoesNotExist:
            return JsonResponse({"error": "No existe"})
    
    
