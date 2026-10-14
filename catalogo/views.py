from django.shortcuts import get_object_or_404, render

from .models import Livro


def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, "catalogo/lista_livros.html", {"livros": livros})


def comprar_livro(request, slug):
    livro = get_object_or_404(Livro, slug=slug)
    return render(request, "catalogo/comprar_livro.html", {"livro": livro})


def quem_somos(request):
    return render(request, "catalogo/quem_somos.html")


def politica_trocas(request):
    return render(request, "catalogo/politica_trocas.html")
