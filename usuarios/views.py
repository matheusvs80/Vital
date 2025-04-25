from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def home(request):
    # Se o usuário estiver autenticado, passamos o nome dele para o template
    if request.user.is_authenticated:
        nome = request.user.first_name
        return render(request, 'home.html', {'nome': nome})
    
    return render(request, 'home.html')


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha: 
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')  # noqa: F821   
            return redirect('cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'Asenha deve ter no mininmo 6 caracteres')  # noqa: F821
            return redirect('cadastro')
        
        try:
            # Username deve ser único!
            User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except:  # noqa: E722
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('cadastro')

        messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso')
        return redirect('login')
    
def logar(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
						# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('login')
        
def sair(request):
    logout(request)
    return redirect('/')