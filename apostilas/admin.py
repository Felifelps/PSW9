from django.contrib import admin

# Register your models here.
from .models import Apostila, ViewApostila, Tag, Avaliacao

admin.site.register(Apostila)
admin.site.register(ViewApostila)
admin.site.register(Tag)
admin.site.register(Avaliacao)