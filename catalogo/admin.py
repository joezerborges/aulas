from django.contrib import admin
from .models import Livro
from django.contrib import admin
from django.contrib.auth.models import Group
import django.contrib.auth.admin  # Força o registro de Group antes de remover

admin.site.unregister(Group)




@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "preco", "estilo_capa")
    list_filter = ("estilo_capa",)
    search_fields = ("titulo", "autor")
    prepopulated_fields = {"slug": ("titulo",)}
