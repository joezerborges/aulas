from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Livro


class CatalogoViewsTests(TestCase):
    def setUp(self):
        self.livro = Livro.objects.create(
            titulo="Python em sala",
            autor="Ana Exemplo",
            slug="python-em-sala",
            descricao="Um livro de exemplo para a turma.",
            preco="49.90",
        )

    def test_lista_exibe_livro_e_link_de_compra(self):
        resposta = self.client.get(reverse("catalogo:lista"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.livro.titulo)
        self.assertContains(resposta, self.livro.get_absolute_url())

    def test_pagina_de_compra_exibe_livro_e_carrossel(self):
        resposta = self.client.get(self.livro.get_absolute_url())

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.livro.titulo)
        self.assertContains(resposta, 'data-bs-ride="carousel"')
        self.assertContains(resposta, 'data-bs-interval="4500"')
        self.assertNotContains(resposta, 'data-bs-slide="prev"')
        self.assertNotContains(resposta, 'data-bs-slide="next"')

    def test_livro_inexistente_retorna_404(self):
        resposta = self.client.get("/comprar/livro-que-nao-existe/")

        self.assertEqual(resposta.status_code, 404)

    def test_pagina_inicial_exibe_navegacao_e_links_institucionais(self):
        resposta = self.client.get(reverse("catalogo:lista"))

        self.assertContains(resposta, 'href="/quem-somos/"')
        self.assertContains(resposta, 'href="/politica-de-trocas/"')
        self.assertContains(resposta, "Explorar livros")

    def test_paginas_quem_somos_e_politica_de_trocas_abrem(self):
        quem_somos = self.client.get(reverse("catalogo:quem_somos"))
        politica = self.client.get(reverse("catalogo:politica_trocas"))

        self.assertEqual(quem_somos.status_code, 200)
        self.assertContains(quem_somos, "livraria fictícia")
        self.assertEqual(politica.status_code, 200)
        self.assertContains(politica, "demonstração educacional")

    def test_comando_de_exemplo_pode_ser_executado_mais_de_uma_vez(self):
        saida = StringIO()
        call_command("carregar_livros", stdout=saida)
        call_command("carregar_livros", stdout=saida)

        self.assertEqual(Livro.objects.count(), 5)
        self.assertIn("Catálogo de exemplo carregado.", saida.getvalue())
