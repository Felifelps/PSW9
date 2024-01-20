from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')
    
    if request.method == 'GET':
        categoria = request.GET.get('categoria')
        dificuldade = request.GET.get('dificuldade')

        flashcards = Flashcard.objects.filter(user=request.user)

        if categoria:
            flashcards = flashcards.filter(categoria_id=categoria)
        
        if dificuldade:
            flashcards = flashcards.filter(dificuldade=dificuldade)

        return render(
            request,
            'novo_flashcard.html', 
            {
                'categorias': Categoria.objects.all(),
                'dificuldades': Flashcard.DIFICULDADE_CHOICES,
                'flashcards': flashcards
            }
        )

    pergunta = request.POST.get('pergunta')
    resposta = request.POST.get('resposta')
    categoria = request.POST.get('categoria')
    dificuldade = request.POST.get('dificuldade')

    if pergunta.strip() == '' or resposta.strip() == '':
        messages.add_message(
            request,
            constants.ERROR,
            'Prrencha os campos de pergunta e resposta!'
        )
        return redirect('/flashcards/novo_flashcard/')
    
    Flashcard(
        user=request.user,
        pergunta=pergunta,
        resposta=resposta,
        categoria_id=categoria,
        dificuldade=dificuldade
    ).save()

    messages.add_message(
        request,
        constants.SUCCESS,
        'Flashcard criado!'
    )

    return redirect('/flashcards/novo_flashcard/')


def del_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    if not (request.user.id == flashcard.user_id):
        messages.add_message(
            request,
            constants.WARNING,
            'O flashcard não é seu!'
        )
        return redirect('/flashcards/novo_flashcard/')
    flashcard.delete()
    messages.add_message(
        request,
        constants.SUCCESS,
        'Flashcard deletado!'
    )
    return redirect('/flashcards/novo_flashcard/')

def iniciar_desafio(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')
    if request.method == 'GET':
        return render(
            request, 
            'iniciar_desafio.html',
            {
                'categorias': Categoria.objects.all(),
                'dificuldades': Flashcard.DIFICULDADE_CHOICES,
            }
        )
    
    titulo = request.POST.get('titulo')
    categorias = request.POST.getlist('categoria')
    dificuldade = request.POST.get('dificuldade')
    qtd_perguntas = request.POST.get('qtd_perguntas')

    # categoria e flashcards são manytomany
    # só depois de salvar uma vez
    desafio = Desafio(
        user=request.user,
        titulo=titulo,
        quantidade_perguntas=qtd_perguntas,
        dificuldade=dificuldade
    )

    desafio.save()

    desafio.categoria.add(*categorias)

    flashcards = Flashcard.objects.filter(
        user=request.user
    ).filter(
        dificuldade=dificuldade
    ).filter(
        categoria_id__in=categorias
    ).order_by('?')

    if len(flashcards) < int(qtd_perguntas):
        flashcards = flashcards[:int(qtd_perguntas)]

    for f in flashcards:
        f = FlashcardDesafio(flashcard=f)
        f.save()
        desafio.flashcards.add(f)

    desafio.save()

    return redirect('/flashcards/listar_desafio')


def listar_desafio(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')
    desafios = Desafio.objects.filter(user=request.user)

    categoria = request.GET.get('categoria')
    dificuldade = request.GET.get('dificuldade')

    if categoria:
        desafios = desafios.filter(categoria__in=categoria)
    
    if dificuldade:
        desafios = desafios.filter(dificuldade=dificuldade)

    return render(
        request,
        'listar_desafio.html',
        {
            'categorias': Categoria.objects.all(),
            'dificuldades': Flashcard.DIFICULDADE_CHOICES,
            'desafios': desafios
        }
    )


def desafio(request, id):
    des = Desafio.objects.get(id=id)
    if not (request.user.id == des.user_id):
        messages.add_message(
            request,
            constants.WARNING,
            'O desafio não é seu!'
        )
        return redirect('/flashcards/listar_desafio/')
    
    respondidos = des.flashcards.filter(respondido=True)

    data = (
        respondidos.filter(acertou=True).count(),
        respondidos.filter(acertou=False).count(),
        des.flashcards.filter(respondido=False).count(),
    )
    
    return render(
        request,
        'desafio.html',
        {
            'desafio': des,
            'data': data
        }
    )

def responder_flashcard(request, id):
    f = FlashcardDesafio.objects.get(id=id)
    if not (request.user.id == f.flashcard.user_id):
        messages.add_message(
            request,
            constants.WARNING,
            'O flashcard não é seu!'
        )
        return redirect('/flashcards/desafio/')
    
    acertou = request.GET.get('acertou')
    
    f.respondido = True
    f.acertou = acertou == '1'
    f.save()

    return redirect(f'/flashcards/desafio/{request.GET.get("desafio")}')

def relatorio(request, id):
    des = Desafio.objects.get(id=id)
    if not (request.user.id == des.user_id):
        messages.add_message(
            request,
            constants.WARNING,
            'O desafio não é seu!'
        )
        return redirect('/flashcards/iniciar_desafio/')
    
    respondidos = des.flashcards.filter(respondido=True)
    acertados = respondidos.filter(acertou=True)

    grafico1 = [
        acertados.count(),
        respondidos.filter(acertou=False).count()
    ]

    grafico2 = []
    categorias = []

    for categoria in des.categoria.all():
        categorias.append(categoria.nome)
        grafico2.append(
            acertados.filter(flashcard__categoria=categoria).count()
        )



    return render(
        request, 
        'relatorio.html',
        {
            'desafio': des,
            'grafico1': grafico1,
            'grafico2': grafico2,
            'categorias': categorias
        }
    )