from django.http import JsonResponse
from django.utils import timezone
from .models import Boleto
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import mercadopago


# 🔍 BUSCAR BOLETO
def buscar_boleto(request, uuid):
    try:
        boleto = Boleto.objects.get(codigo=uuid)

        # 🔥 SI YA ESTÁ PAGADO
        if boleto.pagado:
            return JsonResponse({
                "id": str(boleto.codigo),
                "monto": float(boleto.monto),
                "pagado": True
            })

        # Calcular tiempo
        ahora = timezone.now()
        tiempo = ahora - boleto.fecha_entrada

        minutos = tiempo.total_seconds() / 60
        horas = minutos / 60

        tarifa_por_hora = 15
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


# 💳 PROCESAR PAGO NORMAL
def procesar_pago(request, id):
    boleto = get_object_or_404(Boleto, id=id)
    metodo = request.GET.get("metodo")

    return render(request, "procesar_pago.html", {
        "boleto": boleto,
        "metodo": metodo
    })


# 🟡 PAYPAL
def pago_paypal(request, boleto_id):
    boleto = get_object_or_404(Boleto, codigo=boleto_id)

    monto = "{:.2f}".format(float(boleto.monto))

    return render(request, "usuarios/pago_paypal.html", {
        "monto": monto,
        "boleto_id": boleto.codigo
    })


# ✅ CONFIRMAR PAGO PAYPAL
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


# 🟢 MERCADO PAGO
def crear_pago_mp(request, boleto_id):
    boleto = get_object_or_404(Boleto, codigo=boleto_id)

    import mercadopago

    sdk = mercadopago.SDK("APP_USR-3120184419890522-041020-ef64319f474db8a50a38b8bfc7ef7de4-3329068576")

    # 🔴 Validar monto
    if float(boleto.monto) <= 0:
        return JsonResponse({"error": "Monto inválido"})

    preference_data = {
        "items": [
            {
                "title": "Pago de estacionamiento",
                "quantity": 1,
                "unit_price": float(boleto.monto),
                "currency_id": "MXN"
            }
        ],
        "back_urls": {
           "success": "http://localhost:8000/pago-exitoso/" + str(boleto.codigo) + "/",
           "failure": "http://localhost:8000/pago-error/",
           "pending": "http://localhost:8000/pago-pendiente/",
        },
        #"auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)

    print("RESPUESTA MP:", preference)

    if preference["status"] == 201:
        return redirect(preference["response"]["sandbox_init_point"])
    else:
        return JsonResponse({
            "error": "Mercado Pago falló",
            "detalle": preference
        })
        
# ✅ CUANDO EL PAGO FUE EXITOSO
def pago_exitoso(request, boleto_id):
    boleto = get_object_or_404(Boleto, codigo=boleto_id)
    boleto.pagado = True
    boleto.save()
    return redirect("/inicio/")


# ❌ ERROR
def pago_error(request):
    return JsonResponse({"status": "error"})


# ⏳ PENDIENTE
def pago_pendiente(request):
    return JsonResponse({"status": "pendiente"})