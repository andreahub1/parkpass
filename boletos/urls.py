from django.urls import path
from . import views

urlpatterns = [
    path('buscar-boleto/<uuid:uuid>/', views.buscar_boleto, name='buscar_boleto'),
     path('procesar-pago/<int:id>/', views.procesar_pago, name='procesar_pago'),
]
