from django.urls import path  
from . import views  
app_name = 'pago_qr'  
urlpatterns = [path('', views.index, name='index')] 
