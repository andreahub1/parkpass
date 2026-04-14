from django.urls import path
from . import views

urlpatterns = [
    path('buscar-boleto/<uuid:uuid>/', views.buscar_boleto, name='buscar_boleto'),
    path('procesar-pago/<int:id>/', views.procesar_pago, name='procesar_pago'),
    path('confirmar-pago/', views.confirmar_pago, name='confirmar_pago'),
    path('pago-paypal/<uuid:boleto_id>/', views.pago_paypal, name='pago_paypal'),
    path('pago-mercado/<str:boleto_id>/', views.crear_pago_mp, name='pago_mp'),
    path('pago-exitoso/<str:boleto_id>/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-error/', views.pago_error, name='pago_error'),
    path('pago-pendiente/', views.pago_pendiente, name='pago_pendiente'),]
