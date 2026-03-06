from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# 🏠 HOME PÚBLICO (login / registro)
def home(request):
    return render(request, 'usuarios/home.html')


# 🔐 LOGIN
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('inicio')  # Home azul
        else:
            return render(request, 'usuarios/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'usuarios/login.html')


# 📝 REGISTRO
def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 🔹 Validar que las contraseñas coincidan
        if password != confirm_password:
            return render(request, 'usuarios/registro.html', {
                'error': 'Las contraseñas no coinciden'
            })

        # 🔹 Validar que el usuario no exista
        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/registro.html', {
                'error': 'El usuario ya existe'
            })

        # 🔹 Crear usuario
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        messages.success(request, "Usuario registrado correctamente ✅")
        return redirect('login')

    return render(request, 'usuarios/registro.html')


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# 🔵 INICIO (después de iniciar sesión)
@login_required
def inicio(request):
    return render(request, 'usuarios/inicio.html')


# 📷 ESCANEAR QR
@login_required
def escanear_qr(request):
    return render(request, 'usuarios/escanear.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from boletos.models import Boleto

def procesar_pago(request, codigo):
    boleto = get_object_or_404(Boleto, codigo=codigo)

    if request.method == "POST":
        boleto.pagado = True
        boleto.save()

        messages.success(request,  "Pago realizado con éxito. Tienes 15 minutos para salir del estacionamiento.")
        return redirect("inicio")

    metodo = request.GET.get("metodo")

    return render(request, "usuarios/procesar_pago.html", {
        "boleto": boleto,
        "metodo": metodo
    })
    
    
from .models import Contacto
from django.contrib import messages

def inicio(request):

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        mensaje = request.POST.get("mensaje")

        if nombre and correo and mensaje:
            Contacto.objects.create(
                nombre=nombre,
                correo=correo,
                mensaje=mensaje
            )

            # 📧 Enviar correo
            asunto = "Nuevo mensaje de contacto - ParkPass"
            cuerpo = f"""
            Nombre: {nombre}
            Correo: {correo}

            Mensaje:
            {mensaje}
            """

            send_mail(
                asunto,
                cuerpo,
                settings.EMAIL_HOST_USER,
                ['andrea.ledesmalopez@cesunbc.edu.mx'],  # AQUI VA EL CORREO QUE RECIBE
                fail_silently=False,
            )

            messages.success(request, "Mensaje enviado correctamente ✅")
            return redirect("inicio")

    return render(request, "usuarios/inicio.html")