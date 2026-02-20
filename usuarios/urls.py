from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Público
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # 🔵 Área privada
    path('inicio/', views.inicio, name='inicio'),          # Home azul
    path('escanear/', views.escanear_qr, name='escanear'), # Lector QR
]
