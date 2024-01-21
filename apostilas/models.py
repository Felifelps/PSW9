from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    nome = models.CharField(max_length=50)

class Apostila(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return f'<Apostila {self.titulo}>'


class ViewApostila(models.Model):
    ip = models.GenericIPAddressField()
    apostila =  models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'<ViewApostila {self.ip}>'
    
class Avaliacao(models.Model):
    AVALIACAO_CHOICES = (
        ('1', 'Muito Ruim'),
        ('2', 'Ruim'),
        ('3', 'Mediano'),
        ('4', 'Boa'),
        ('5', 'Muito Boa'),
    )
    avaliacao = models.CharField(max_length=1, choices=AVALIACAO_CHOICES)
    apostila =  models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'<Avaliacao {self.avaliacao}>'

