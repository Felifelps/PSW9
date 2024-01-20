from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth

# Create your views here.
def cadastro(request):
    if request.method == 'POST':
        # Pega os dados do formulário
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not (senha == confirmar_senha):
            messages.add_message(
                request,
                constants.ERROR,
                'Senhas não coincidem!'
            )
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(
                request, 
                constants.ERROR,
                'Usuário já cadastrado!'
            )
            return redirect('/usuarios/cadastro')
        
        try:
            User.objects.create_user(
                username=username,
                password=senha
            )
            return redirect('/usuarios/login')
        except:
            messages.add_message(
                request, 
                constants.ERROR,
                'Erro interno no servidor!'
            )
            return redirect('/usuarios/cadastro')
        
    return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(
            request,
            username=username,
            password=senha
        )

        if user:
            auth.login(request, user)
            messages.add_message(
                request,
                constants.SUCCESS,
                'Usuário logado!'
            )
            return redirect('/flashcards/novo_flashcard')
        
        messages.add_message(
            request,
            constants.ERROR,
            'Usuário ou senha incorretos!'
        )
        return redirect('/usuarios/login')

        

    return render(
        request,
        'login.html'
    )

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')