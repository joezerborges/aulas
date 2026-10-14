from django.urls import path

from . import views


app_name = "catalogo"

urlpatterns = [
    path("", views.lista_livros, name="lista"),
    path("comprar/<slug:slug>/", views.comprar_livro, name="comprar"),
    path("quem-somos/", views.quem_somos, name="quem_somos"),
    path("politica-de-trocas/", views.politica_trocas, name="politica_trocas"),
]
