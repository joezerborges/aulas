from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Livro",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=160, verbose_name="título")),
                ("autor", models.CharField(max_length=120, verbose_name="autor")),
                ("slug", models.SlugField(unique=True)),
                ("descricao", models.TextField(verbose_name="descrição")),
                (
                    "preco",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, verbose_name="preço"
                    ),
                ),
                (
                    "estilo_capa",
                    models.CharField(
                        choices=[
                            ("terracota", "Terracota"),
                            ("azul", "Azul"),
                            ("verde", "Verde"),
                            ("roxo", "Roxo"),
                        ],
                        default="terracota",
                        max_length=12,
                        verbose_name="estilo da capa",
                    ),
                ),
            ],
            options={
                "verbose_name": "livro",
                "verbose_name_plural": "livros",
                "ordering": ["titulo"],
            },
        ),
    ]
