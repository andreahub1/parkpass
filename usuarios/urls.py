from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Público
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # 🔵 Área privada
    path('inicio/', views.inicio, name='inicio'),
    path('escanear/', views.escanear_qr, name='escanear'),

    # 💳 Pago
    path('procesar-pago/<str:codigo>/', views.procesar_pago, name='procesar_pago'),

    # 🔐 ADMIN QR
    path('generar-qr/', views.generar_qr, name='generar_qr'),
]