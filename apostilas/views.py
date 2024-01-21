from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Apostila, ViewApostila, Tag, Avaliacao

# Create your views here.
def adicionar_apostila(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')
    if request.method == 'GET':
        views_totais = ViewApostila.objects.filter(
            apostila__user=request.user
        ).count()
        return render(
            request, 
            'adicionar_apostila.html',
            {
                'apostilas': Apostila.objects.filter(user=request.user),
                'views_totais': views_totais
            }
        )
    
    titulo = request.POST.get('titulo')
    arquivo = request.FILES['arquivo']

    Apostila(
        user=request.user,
        titulo=titulo,
        arquivo=arquivo
    ).save()

    messages.add_message(
        request,
        messages.constants.SUCCESS,
        'Salvo com sucesso!'
    )

    return redirect('/apostilas/adicionar_apostila/')


def ver_apostila(request, id):
    for ap in Apostila.objects.all():
        ap.delete()
    apostila = Apostila.objects.get(id=id)
    if not (request.user.id == apostila.user_id):
        messages.add_message(
            request,
            messages.constants.WARNING,
            'A apostila não é sua!'
        )
        return redirect('/apostilas/adicionar_apostila/')
    
    ViewApostila(
        apostila=apostila,
        ip=request.META['REMOTE_ADDR']
    ).save()

    views_apostila = ViewApostila.objects.filter(apostila=apostila)

    return render(
        request, 
        'ver_apostila.html',
        {
            'apostila': apostila,
            'views_unicas': len({view.ip for view in views_apostila}),
            'views_totais': views_apostila.count()
        }
    )