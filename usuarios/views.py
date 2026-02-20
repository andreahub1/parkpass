from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
