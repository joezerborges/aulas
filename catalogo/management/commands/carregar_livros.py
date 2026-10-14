from django.core.management.base import BaseCommand

from catalogo.models import Livro


class Command(BaseCommand):
    help = "Carrega livros de exemplo para a loja."

    def handle(self, *args, **options):
        livros = [
            {
                "titulo": "Python para Curiosos",
                "autor": "Marina Costa",
                "slug": "python-para-curiosos",
                "descricao": (
                    "Uma introdução acolhedora à programação com Python, "
                    "com exemplos práticos e projetos para iniciantes."
                ),
                "preco": "59.90",
                "estilo_capa": Livro.EstiloCapa.TERRACOTA,
            },
            {
                "titulo": "Django na Prática",
                "autor": "Rafael Lima",
                "slug": "django-na-pratica",
                "descricao": (
                    "Aprenda a organizar aplicações web, criar modelos e "
                    "construir páginas dinâmicas usando Django."
                ),
                "preco": "74.50",
                "estilo_capa": Livro.EstiloCapa.AZUL,
            },
            {
                "titulo": "Algoritmos Descomplicados",
                "autor": "Beatriz Nunes",
                "slug": "algoritmos-descomplicados",
                "descricao": (
                    "Conceitos fundamentais de lógica e algoritmos explicados "
                    "por meio de desafios e exemplos em Python."
                ),
                "preco": "64.00",
                "estilo_capa": Livro.EstiloCapa.VERDE,
            },
            {
                "titulo": "Interfaces com Bootstrap",
                "autor": "Lucas Mendes",
                "slug": "interfaces-com-bootstrap",
                "descricao": (
                    "Um guia de componentes responsivos para criar interfaces "
                    "web organizadas e acessíveis."
                ),
                "preco": "52.90",
                "estilo_capa": Livro.EstiloCapa.ROXO,
            },
        ]

        for dados in livros:
            livro, criado = Livro.objects.update_or_create(
                slug=dados["slug"],
                defaults=dados,
            )
            acao = "Criado" if criado else "Atualizado"
            self.stdout.write(f"{acao}: {livro.titulo}")

        self.stdout.write(self.style.SUCCESS("Catálogo de exemplo carregado."))
