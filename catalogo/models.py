from django.db import models
from django.urls import reverse


class Livro(models.Model):
    class EstiloCapa(models.TextChoices):
        TERRACOTA = "terracota", "Terracota"
        AZUL = "azul", "Azul"
        VERDE = "verde", "Verde"
        ROXO = "roxo", "Roxo"

    titulo = models.CharField("título", max_length=160)
    autor = models.CharField("autor", max_length=120)
    slug = models.SlugField(unique=True)
    descricao = models.TextField("descrição")
    preco = models.DecimalField("preço", max_digits=8, decimal_places=2)
    imagem_capa_url = models.URLField(
        "URL da imagem da capa",
        max_length=500,
        blank=True,
        help_text=(
            "Informe o endereço direto de uma imagem que você tem autorização "
            "para exibir. Deixe em branco para usar a capa ilustrada."
        ),
    )
    estilo_capa = models.CharField(
        "estilo da capa",
        max_length=12,
        choices=EstiloCapa.choices,
        default=EstiloCapa.TERRACOTA,
    )

    class Meta:
        ordering = ["titulo"]
        verbose_name = "livro"
        verbose_name_plural = "livros"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("catalogo:comprar", args=[self.slug])
