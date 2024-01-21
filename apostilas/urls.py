from django.urls import path
from . import views

urlpatterns = [
    path('adicionar_apostila/', views.adicionar_apostila, name='adicionar_apostila'),
    path('ver_apostila/<int:id>', views.ver_apostila, name='ver_apostila'),
]
