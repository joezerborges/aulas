# Página de Papel — projeto didático de livraria com Django

Este material acompanha uma pequena vitrine de livros feita com **Python,
Django, SQLite, templates HTML e Bootstrap**. O visual utiliza os componentes
e as classes prontas do Bootstrap, sem exigir que a turma escreva CSS próprio.
Ele foi escrito para ser usado em
aula: apresenta primeiro o que o projeto faz, depois explica como executar e,
por fim, guia a turma pela construção de cada parte.

O site tem duas páginas principais:

1. **Catálogo:** apresenta os livros em cartões responsivos.
2. **Detalhe do livro:** abre quando o visitante clica em **Comprar**; mostra
   a descrição e o preço e apresenta um carrossel automático, sem setas nem
   indicadores de navegação.

Os livros ficam no banco de dados SQLite. É possível editá-los pelo painel
administrativo do Django.

> **Importante — demonstração didática:** o botão leva à página informativa do
> livro. O site não tem carrinho, não registra pedidos e não processa
> pagamentos. Portanto, essa demonstração **não realiza uma compra**.
>
> **Importante — ambiente local:** o projeto está configurado para
> desenvolvimento (`DEBUG = True`) e contém uma chave secreta ilustrativa.
> Não o publique na internet nessa configuração. Um projeto real precisa de
> configuração segura e revisão antes de ser colocado em produção.

## Objetivos de aprendizagem

Ao percorrer o material e fazer as atividades, a turma poderá:

- reconhecer a diferença entre um **projeto Django** e uma **aplicação Django**;
- criar e ativar um ambiente virtual e instalar dependências;
- modelar dados com o Django ORM e relacionar o modelo com uma tabela;
- entender por que as mudanças de modelo são registradas em migrações;
- percorrer o caminho entre URL, view, banco de dados e template;
- exibir dados do banco em HTML usando o sistema de templates do Django;
- usar Bootstrap para montar uma grade responsiva e um carrossel automático;
- cadastrar e consultar dados pelo Django Admin;
- escrever testes para páginas e respostas HTTP;
- identificar quais partes ainda seriam necessárias para transformar a
  demonstração em uma loja real.

## Roteiro de construção do zero com a turma

Esta seção é o roteiro principal para a aula. A proposta é começar em uma
pasta vazia e criar o site em pequenas etapas. Ao final de cada etapa, pare,
execute o projeto e confira o resultado antes de avançar. Assim, quando surgir
um erro, a turma sabe qual foi a última mudança feita.

O projeto que acompanha este README já contém os arquivos prontos. Para
praticar desde o início, **não execute estes comandos dentro da pasta que já
contém este README**: crie uma pasta nova para a turma e siga a sequência
abaixo. Outra opção é pedir aos alunos que criem os arquivos numa cópia
separada do projeto.

### Antes de digitar código: desenhar o que vamos construir

Apresente primeiro o resultado e pergunte quais informações um livro precisa
ter na loja. Para este exercício, cada registro terá título, autor, endereço
curto, descrição, preço, estilo visual da capa e, opcionalmente, a URL de uma
imagem autorizada para a capa. Depois desenhe o caminho de
uma visita:

```text
Navegador -> URL -> view -> banco de dados -> template -> HTML no navegador
```

Explique o propósito de cada peça antes de criá-la:

- **URL:** responde “qual endereço o visitante pediu?”;
- **view:** decide o que fazer com aquela requisição;
- **modelo:** descreve os dados e permite consultá-los no banco;
- **template:** define como os dados viram HTML;
- **CSS/Bootstrap:** define a apresentação e o comportamento visual;
- **banco:** mantém os livros mesmo depois que o servidor é encerrado.

O botão da demonstração terá o texto **Comprar**, mas só navegará até a
página informativa do livro. Avise desde o início que não faremos carrinho,
pedido nem pagamento.

### Etapa 1 — criar uma pasta de trabalho isolada

No PowerShell, escolha um local para a aula e crie a pasta:

```powershell
New-Item -ItemType Directory pagina_de_papel
Set-Location pagina_de_papel
```

Confira que a pasta está vazia:

```powershell
Get-Location
Get-ChildItem
```

**O que fazer:** abrir essa pasta no editor e usar nela o terminal integrado.

**Por que fazer:** todos os comandos seguintes criam arquivos relativamente
à pasta atual. Começar com uma pasta vazia também evita misturar este
exercício com outro projeto Django.

### Etapa 2 — criar e ativar um ambiente virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**O que fazer:** conferir que `(.venv)` aparece no terminal. Se `py` não
estiver instalado, use `python -m venv .venv`.

**Por que fazer:** o ambiente virtual isola as bibliotecas deste curso das
bibliotecas instaladas para outros projetos. Isso torna mais previsível a
instalação e evita que uma atualização para outra disciplina quebre este
exercício.

Em seguida, instale Django e registre a dependência do projeto:

```powershell
python -m pip install "Django>=5.2,<7.0"
```

Crie o arquivo `requirements.txt` na pasta principal com:

```text
Django>=5.2,<7.0
django-browser-reload>=1.18,<2.0
```

Instale também o pacote de recarga automática agora registrado:

```powershell
python -m pip install -r requirements.txt
```

**Por que manter `requirements.txt`:** uma pessoa que receber o projeto
consegue recriar as dependências com
`python -m pip install -r requirements.txt`, em vez de adivinhar quais
bibliotecas são necessárias. A faixa admite versões compatíveis com o Python
instalado; em projetos de produção, a equipe pode fixar versões com uma
estratégia de dependências própria.

### Etapa 3 — criar o projeto e a aplicação Django

Com o ambiente virtual ativo, execute:

```powershell
django-admin startproject livraria .
python manage.py startapp catalogo
```

O ponto `.` em `startproject livraria .` é importante: diz ao Django para
criar o projeto na pasta atual, onde já está o ambiente virtual, em vez de
criar mais uma pasta externa.

**Explique a diferença:**

- `livraria` é o **projeto**, que contém configurações gerais e as rotas
  principais;
- `catalogo` é uma **aplicação**, que conterá a funcionalidade de livros.

Um projeto pode ter várias aplicações. Separar as responsabilidades agora
ajuda a turma a entender onde cada funcionalidade deve ficar.

Crie as pastas para os templates e arquivos CSS:

```powershell
New-Item -ItemType Directory -Force -Path catalogo\templates\catalogo
```

**Por que criar `templates/catalogo`:** o Django procura os templates dentro
de cada aplicação quando `APP_DIRS` está habilitado. O nome adicional
`catalogo` evita colisões, por exemplo, entre templates de aplicações
diferentes com o mesmo nome `base.html`.

Nesta versão, não é necessário criar uma pasta de CSS: vamos usar os
componentes e as classes prontos do Bootstrap.

### Etapa 4 — configurar a aplicação e o idioma

Abra `livraria/settings.py`, criado pelo comando do Django.

1. Na lista `INSTALLED_APPS`, acrescente `"catalogo",`.
2. Altere o idioma para `pt-br` e o fuso horário para `America/Sao_Paulo`.

O resultado das partes relevantes fica assim:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_browser_reload",
    "catalogo",
]

MIDDLEWARE = [
    # Preserve the middleware created by Django above this line.
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
```

**O que fazer:** salve e localize essas configurações no arquivo antes de
continuar.

**Por que registrar `"catalogo"`:** sem essa etapa, o Django não carrega a
aplicação como parte do projeto e não encontra corretamente modelos,
migrações e outras integrações dela.

O Django já cria `STATIC_URL`, usado para localizar arquivos estáticos.
Como esta versão usa o CSS do Bootstrap por CDN e não mantém uma folha CSS
própria, não precisamos configurar `STATICFILES_DIRS`.

Na lista real `MIDDLEWARE`, mantenha todos os itens que o Django criou e
adicione `"django_browser_reload.middleware.BrowserReloadMiddleware"` no
final. A linha isolada mostrada acima só destaca a adição: não substitua por
ela a lista completa gerada pelo Django.

O pacote `"django_browser_reload"` em `INSTALLED_APPS` e o middleware são
necessários para ativar a recarga automática no navegador. Essa integração é
explicada passo a passo na seção “Ver as alterações sem atualizar a página
manualmente”.

> O arquivo gerado pelo Django também contém `SECRET_KEY`, `DEBUG`, banco,
> templates e middleware. Preserve a configuração gerada nessa aula; não
> substitua o arquivo inteiro por um fragmento de exemplo. Explique que
> `DEBUG=True` e a chave de desenvolvimento só são adequados para a aula em
> ambiente local.

### Etapa 5 — modelar os livros antes de desenhar os cartões

Abra `catalogo/models.py` e defina o modelo. O modelo descreve os dados que
queremos guardar; ele ainda não é uma página HTML nem uma tabela criada no
banco.

```python
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
```

**Explique as decisões:**

- Herdar de `models.Model` permite ao Django tratar `Livro` como um modelo
  persistido.
- `CharField` guarda texto curto; por isso exige `max_length`.
- `TextField` guarda a descrição, que pode ser maior.
- `DecimalField` representa preços com casas decimais; para dinheiro é uma
  escolha mais apropriada do que `FloatField`.
- `URLField` armazena um endereço de imagem; `blank=True` torna o campo
  opcional para que os livros continuem usando uma capa ilustrada quando não
  houver imagem.
- `max_length=500` permite URLs maiores do que o limite padrão do campo.
- `help_text` mostra no formulário do admin como preencher o campo e lembra
  que a imagem precisa estar autorizada.
- `SlugField` guarda um texto apropriado para a URL, por exemplo
  `django-na-pratica`. `unique=True` impede que dois livros tenham o mesmo
  slug.
- `TextChoices` restringe o estilo da capa a valores conhecidos e dá rótulos
  legíveis no admin.
- `Meta.ordering` pede que as consultas sejam ordenadas pelo título.
- `__str__` faz objetos aparecerem com um nome útil, em vez de uma
  representação técnica.
- `get_absolute_url` centraliza o endereço canônico do livro. `reverse`
  encontra a rota pelo nome e monta a URL com o slug.

**Confira com a turma:** quais dados são obrigatórios para exibir um livro?
Qual campo precisa ser único para compor o endereço? O preço poderia ser
texto? Peça que justifiquem as escolhas antes de seguir.

### Etapa 6 — transformar o modelo em tabela

Execute:

```powershell
python manage.py makemigrations
```

Abra o arquivo que o Django criar dentro de `catalogo/migrations/`.
Ele registra, em código, como criar a tabela e as colunas do modelo.

Depois execute:

```powershell
python manage.py migrate
```

**Explique a diferença:**

- `makemigrations` compara os modelos com o histórico de migrações e
  **escreve uma instrução de mudança**;
- `migrate` **executa as instruções** no banco de dados.

As migrações permitem que toda a turma aplique a mesma alteração de esquema,
em ordem, mesmo que cada pessoa tenha seu próprio banco local.

O Django usa SQLite nesta atividade. Ele guarda os dados num arquivo local,
não exige instalação de um servidor de banco separado e é suficiente para
aprender os conceitos.

### Etapa 7 — disponibilizar os livros no painel administrativo

Abra `catalogo/admin.py`:

```python
from django.contrib import admin

from .models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "preco", "estilo_capa")
    list_filter = ("estilo_capa",)
    search_fields = ("titulo", "autor")
    prepopulated_fields = {"slug": ("titulo",)}
```

**O que fazer:** salve o arquivo. Depois crie uma conta administrativa:

```powershell
python manage.py createsuperuser
```

**Por que registrar o modelo:** o admin do Django já oferece telas para
cadastrar, alterar e excluir registros. O decorador `@admin.register(Livro)`
liga o modelo a essas telas. `list_display`, `list_filter` e `search_fields`
adaptam a listagem para ser útil à pessoa que administra o catálogo.

`prepopulated_fields` ajuda a preencher o slug a partir do título, mas a
restrição `unique=True` no modelo continua importante: a validação de
unicidade não deve depender somente da interface administrativa.

Execute `python manage.py runserver`, abra
<http://127.0.0.1:8000/admin/> e cadastre pelo menos dois livros. Nesse
momento, os dados existem no banco; as páginas públicas ainda serão criadas
nas etapas seguintes.

### Etapa 8 — criar a view que consulta os livros

Abra `catalogo/views.py`:

```python
from django.shortcuts import get_object_or_404, render

from .models import Livro


def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, "catalogo/lista_livros.html", {"livros": livros})


def comprar_livro(request, slug):
    livro = get_object_or_404(Livro, slug=slug)
    return render(request, "catalogo/comprar_livro.html", {"livro": livro})
```

**Explique cada função:**

- O Django chama a função de view quando uma URL associada a ela é
  requisitada. O primeiro argumento é a requisição HTTP (`request`).
- `Livro.objects.all()` usa o ORM para pedir todos os livros ao banco.
- `get_object_or_404` procura um livro pelo slug. Se não encontrar, responde
  com HTTP 404 — “não encontrado” — em vez de mostrar uma página sem dados.
- `render` combina um template com um dicionário de contexto. A chave
  `"livros"` ou `"livro"` será o nome disponível no HTML.

**Por que não escrever SQL nesta etapa:** o ORM permite consultar objetos
usando Python e traduz as operações para o banco configurado pelo projeto.
Isso facilita o exemplo, sem esconder que os dados vêm do banco.

### Etapa 9 — declarar os endereços das páginas

Crie `catalogo/urls.py`:

```python
from django.urls import path

from . import views


app_name = "catalogo"

urlpatterns = [
    path("", views.lista_livros, name="lista"),
    path("comprar/<slug:slug>/", views.comprar_livro, name="comprar"),
]
```

Depois edite `livraria/urls.py` para encaminhar a raiz do site à aplicação:

```python
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("catalogo.urls")),
]
```

Essa rota adicional é o canal de eventos usado pelo django-browser-reload.
Ela não é uma página do catálogo que o visitante precise abrir.

**Por que dividir as URLs:** o projeto escolhe qual aplicação atende à
requisição; a aplicação conhece suas próprias rotas. Essa divisão facilita
adicionar outras áreas no futuro.

**Leia os padrões com a turma:**

- `path("", ...)` associa a raiz `/` à lista de livros;
- `comprar/` é um prefixo fixo para detalhes;
- `<slug:slug>` captura uma parte da URL e a entrega à view como argumento
  chamado `slug`;
- `name="comprar"` dá um nome estável à rota para gerar links sem codificar
  manualmente o endereço.

O projeto final também possui as rotas `quem_somos` e `politica_trocas`.
Essas páginas são informativas: por isso, suas views apenas selecionam o
template apropriado; não precisam consultar o modelo de livros.

### Etapa 10 — criar a estrutura comum dos templates

Crie `catalogo/templates/catalogo/base.html`. Este arquivo será a moldura
compartilhada pelas páginas e carrega o Bootstrap:

```html
<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Página de Papel{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'catalogo:lista' %}">
                Página de Papel
            </a>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer class="container py-4">
        Projeto didático: nenhum pagamento é processado.
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

O template-base deste repositório também inclui atributos `integrity` e
`crossorigin` nos recursos do CDN; ao usar os recursos diretamente no
projeto, prefira manter essas proteções do arquivo final.

#### Criar navegação e rodapé compartilhados

No arquivo completo `base.html`, a barra superior é uma **navbar do
Bootstrap**. Ela contém um nome de marca que volta ao início, links para o
catálogo e para “Quem somos”, além de um botão destacado para explorar os
livros. Em telas pequenas, o botão hambúrguer expande e recolhe o menu.

**O que fazer na aula:** adicione os links dentro de uma lista
`navbar-nav`. Para que um link funcione, crie primeiro sua rota em
`catalogo/urls.py`; só então use `{% url 'catalogo:quem_somos' %}` no
template.

**Por que usar `{% url %}`:** o template pergunta ao Django qual caminho
corresponde ao nome da rota. Se o endereço mudar no arquivo de URLs, o link
continua funcionando sem precisar atualizar manualmente todas as páginas.

O botão expansível usa `data-bs-toggle="collapse"` e
`data-bs-target="#siteNavigation"`. O `id` indicado pelo alvo precisa ser
igual ao `id` do elemento expansível. O JavaScript do Bootstrap, já carregado
ao final da base, implementa abrir e fechar; os atributos ARIA informam aos
leitores de tela que o botão controla aquele menu.

O rodapé também fica na base, então aparece de modo consistente em todas as
páginas. Ele agrupa os links para catálogo, “Quem somos” e “Política de
trocas”, e exibe o aviso de que esta demonstração não processa pedidos.
Classes prontas do Bootstrap dão cor, contraste e espaçamento aos links. No
celular, as colunas do rodapé se reorganizam com a grade responsiva.

As páginas informativas usam o mesmo `base.html`, mas cada uma tem um
template próprio. `quem_somos.html` explica o propósito fictício e
educacional da livraria. `politica_trocas.html` deixa explícito que o site
não vende nem aceita solicitações; seu texto é ilustrativo e não deve ser
tratado como uma política jurídica de uma loja real.

**Explique as tags:**

- `{% block title %}` e `{% block content %}` são espaços que os templates
  filhos preencherão;
- `{% url 'catalogo:lista' %}` resolve a rota nomeada e cria o link inicial;
- classes como `bg-dark`, `text-light`, `py-5` e `btn` aplicam os estilos que
  o Bootstrap já fornece;
- `bootstrap.bundle.min.js` habilita componentes interativos, como o
  carrossel;

Bootstrap virá de um CDN. Portanto, o navegador precisa de internet para
baixar esses arquivos. O Django serve os templates; o navegador aplica
o CSS do Bootstrap depois de receber o HTML.

**Bootstrap evita escrever CSS, mas não elimina HTML:** ainda precisamos
declarar no template se algo é um título, link, imagem ou cartão. As classes
do Bootstrap dizem como esses elementos devem aparecer e se adaptar às telas.

O pacote de recarga automática acrescenta o próprio script à resposta HTML
em ambiente de desenvolvimento, por meio do middleware. Não precisamos
adicionar código JavaScript nosso nem uma tag extra aos templates.

### Etapa 11 — renderizar cada livro em um cartão

Crie `catalogo/templates/catalogo/lista_livros.html`:

```html
{% extends "catalogo/base.html" %}

{% block title %}Livros | Página de Papel{% endblock %}

{% block content %}
<section class="container py-5">
    <h1 class="mb-4">Encontre sua próxima leitura</h1>

    <div class="row g-4">
        {% for livro in livros %}
        <div class="col-sm-6 col-lg-4 col-xl-3">
            <article class="card h-100 shadow-sm">
                <div class="ratio ratio-1x1 bg-body-secondary">
                    {% if livro.imagem_capa_url %}
                    <img class="w-100 h-100 object-fit-contain"
                         src="{{ livro.imagem_capa_url }}"
                         alt="Capa de {{ livro.titulo }}"
                         loading="lazy">
                    {% else %}
                    <div class="d-flex flex-column justify-content-center align-items-center text-center text-white bg-primary p-4">
                        <span class="small text-uppercase mb-3">Página de Papel</span>
                        <span class="h3">{{ livro.titulo }}</span>
                        <span>{{ livro.autor }}</span>
                    </div>
                    {% endif %}
                </div>
                <div class="card-body d-flex flex-column">
                    <h2 class="h5">{{ livro.titulo }}</h2>
                    <p>{{ livro.descricao }}</p>
                    <p class="fw-bold mt-auto">R$ {{ livro.preco }}</p>
                    <a class="btn btn-primary"
                       href="{{ livro.get_absolute_url }}">Comprar</a>
                </div>
            </article>
        </div>
        {% empty %}
        <div class="col-12">
            <p>O catálogo ainda está vazio. Cadastre livros pelo admin.</p>
        </div>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

**O que fazer:** com pelo menos dois livros cadastrados, atualize `/` no
navegador e confira se aparecem cartões diferentes.

**Por que usar o loop:** a view envia uma coleção, e o template produz um
cartão para cada objeto. Ao cadastrar um terceiro livro, não é necessário
copiar e colar outro cartão em HTML.

**Explique a grade Bootstrap:** `row` organiza a linha; `col-sm-6`,
`col-lg-4` e `col-xl-3` alteram o número de colunas conforme a largura da
tela. `g-4` define espaço entre cartões. `empty` trata explicitamente a lista
sem resultados.

`get_absolute_url()` foi implementado no modelo e devolve a rota daquele
livro. O botão é um link de navegação, não um formulário de compra.

### Etapa 12 — criar a página individual do livro

Crie `catalogo/templates/catalogo/comprar_livro.html`:

```html
{% extends "catalogo/base.html" %}

{% block title %}{{ livro.titulo }} | Página de Papel{% endblock %}

{% block content %}
<section class="container py-5">
    <a href="{% url 'catalogo:lista' %}">&larr; Voltar ao catálogo</a>
    <div class="row align-items-center g-4 mt-2">
        <div class="col-md-5">
            <div class="ratio ratio-1x1 bg-body-secondary rounded overflow-hidden">
                {% if livro.imagem_capa_url %}
                <img class="w-100 h-100 object-fit-contain"
                     src="{{ livro.imagem_capa_url }}"
                     alt="Capa de {{ livro.titulo }}">
                {% else %}
                <div class="d-flex flex-column justify-content-center align-items-center text-center text-white bg-primary p-4">
                    <span class="h3">{{ livro.titulo }}</span>
                    <span>{{ livro.autor }}</span>
                </div>
                {% endif %}
            </div>
        </div>
        <div class="col-md-7">
            <h1>{{ livro.titulo }}</h1>
            <p>por {{ livro.autor }}</p>
            <p>{{ livro.descricao }}</p>
            <p class="fs-3">R$ {{ livro.preco }}</p>
            <p class="alert alert-info">
                Demonstração didática. Nenhum pedido ou pagamento será realizado.
            </p>
        </div>
    </div>

    <section class="mt-5" aria-label="Apresentação do livro">
        <div id="livroCarousel"
             class="carousel slide"
             data-bs-ride="carousel"
             data-bs-interval="4500"
             data-bs-pause="false"
             data-bs-touch="false">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <div class="bg-primary text-white rounded p-5">
                        <h2>Aprenda no seu ritmo</h2>
                        <p>Conheça os detalhes e descubra se esta leitura combina com você.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="bg-success text-white rounded p-5">
                        <h2>Ideias que viram projetos</h2>
                        <p>Use a leitura para inspirar seus próximos passos de aprendizagem.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="bg-dark text-white rounded p-5">
                        <h2>Feito para aprender web</h2>
                        <p>Esta vitrine é um exemplo de integração entre Django e Bootstrap.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</section>
{% endblock %}
```

**Por que há `active`:** o Bootstrap precisa saber qual slide mostrar
primeiro. Sem um slide ativo, o carrossel pode iniciar sem conteúdo visível.

**Por que não há setas:** o HTML inclui apenas `carousel-inner` e seus itens;
não há controles de anterior/próximo nem indicadores. `data-bs-ride` inicia
a rotação, `data-bs-interval` define o tempo em milissegundos e os outros
atributos desativam pausa por mouse e gesto de toque.

O JavaScript do Bootstrap foi carregado na base. Sem ele, os atributos HTML
não bastam para avançar os slides.

### Etapa 13 — compor a aparência com classes do Bootstrap

Neste projeto não criamos um arquivo CSS. A aparência vem de classes e
componentes prontos do Bootstrap, que já incluímos em `base.html`.

**O que fazer:** leia as classes usadas nos templates e experimente trocar
uma de cada vez. Por exemplo, mude `bg-primary` para `bg-success`, ou
`btn-primary` para `btn-outline-primary`, atualize o navegador e observe o
resultado.

**Por que funciona sem CSS próprio:** o Bootstrap já contém as regras de
apresentação para essas classes. Por exemplo:

- `container`, `row` e `col-*` organizam a grade responsiva;
- `card`, `card-body` e `shadow-sm` formam o cartão do livro;
- `btn`, `btn-primary` e `btn-warning` formatam os botões;
- `bg-dark`, `bg-primary`, `text-white` e `text-secondary` aplicam cores;
- `p-*`, `py-*`, `mb-*` e `gap-*` aplicam espaçamento;
- `ratio ratio-1x1` reserva uma área quadrada para a imagem;
- `w-100 h-100 object-fit-contain` encaixa a imagem nessa área sem deformá-la;
- `alert alert-info` destaca uma mensagem;
- `navbar` e `collapse` implementam a barra de navegação adaptável;
- `carousel` e `carousel-item` montam o carrossel.

Bootstrap não elimina o HTML: o template ainda precisa declarar que um
elemento é um link, imagem, título ou cartão. O que ele evita nesta aula é
escrever as regras CSS que determinariam cores, espaçamentos, colunas e
comportamento responsivo.

**Atenção aos limites da grade:** `ratio-1x1` faz uma área quadrada. Foi
escolhida para evitar CSS adicional; as imagens de capa mantêm sua proporção
dentro dela por meio de `object-fit-contain`. Caso se queira uma capa com
proporção personalizada, isso já exigiria CSS ou uma extensão/tema do
Bootstrap.

### Usar uma imagem de capa por URL

O modelo do projeto também tem o campo opcional `imagem_capa_url`. Para
habilitá-lo numa implementação feita pela turma:

1. Adicione o `URLField` ao modelo, com `blank=True`, para que o livro possa
   continuar sem uma imagem.
2. Crie e aplique a migração:

   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

3. No template do cartão e no template de detalhe, teste se
   `livro.imagem_capa_url` tem conteúdo. Se tiver, gere uma tag `<img>`; se
   estiver vazia, mostre a capa ilustrada original:

   ```django
   {% if livro.imagem_capa_url %}
   <img class="w-100 h-100 object-fit-contain"
        src="{{ livro.imagem_capa_url }}"
        alt="Capa de {{ livro.titulo }}"
        loading="lazy">
   {% else %}
   <div class="d-flex flex-column justify-content-center align-items-center text-center text-white bg-primary p-4">
       <span class="h3">{{ livro.titulo }}</span>
       <span>{{ livro.autor }}</span>
   </div>
   {% endif %}
   ```

4. No admin, edite um livro, cole a URL no campo **URL da imagem da capa**,
   salve e confira o cartão e a página de detalhe.

**A URL precisa apontar para o arquivo da imagem**, não para a página de
produto. “Copiar endereço da imagem” no navegador pode fornecer esse link,
mas só use a imagem se você tiver autorização para exibi-la. Uma URL pública
não significa que a imagem esteja liberada para uso comercial. Sites de
livros também podem bloquear a exibição em outros domínios, mudar o endereço
ou remover a imagem; nesse caso, o navegador pode deixar de carregá-la.
Para um site de produção, prefira imagens próprias/licenciadas hospedadas
num serviço que permita essa utilização e mantenha uma alternativa caso a
imagem não carregue. Neste exercício, deixar o campo vazio mantém as capas
ilustradas como fallback.

### Etapa 14 — verificar o percurso completo antes de aprimorar

Pare e teste o fluxo antes de adicionar detalhes visuais:

1. Reinicie `runserver`, se o terminal tiver sido encerrado.
2. Abra `/` e confirme que a lista mostra os livros cadastrados no admin.
3. Clique em **Comprar** em um cartão.
4. Confira que o título, preço e descrição correspondem àquele livro.
5. Aguarde e confirme que o carrossel muda de slide automaticamente.
6. Tente abrir `/comprar/slug-que-nao-existe/` e observe a resposta 404.
7. Volte ao admin, altere o título de um livro e atualize o site.

**Por que testar assim:** cada verificação cobre uma parte do caminho:
roteamento, consulta, contexto, template, JavaScript, tratamento de erro e
leitura atualizada do banco. Se algo falhar, investigue a camada específica
em vez de reescrever o projeto inteiro.

### Etapa 15 — adicionar dados de exemplo e testes

Para uma aula curta, cadastrar dois ou três livros pelo admin é suficiente.
Para repetir rapidamente a demonstração em vários computadores, o projeto
final também inclui o comando `carregar_livros`:

```powershell
python manage.py carregar_livros
```

Ele fica em
`catalogo/management/commands/carregar_livros.py`. O nome do arquivo
(`carregar_livros.py`) vira o nome do comando. `handle` contém a lógica
executada; `update_or_create` cria cada livro na primeira execução e
atualiza os mesmos livros nas execuções seguintes. Esse comando é um passo
opcional para estudar depois que a turma já compreendeu os modelos, views e
templates.

Para verificar o comportamento da aplicação:

```powershell
python manage.py test catalogo
```

Em `catalogo/tests.py`, `TestCase` prepara um banco de teste isolado;
`setUp` cria um livro antes de cada teste; `self.client.get` simula uma
requisição HTTP sem abrir um navegador. As asserções verificam tanto a
resposta quanto o conteúdo relevante. Por exemplo, um teste garante que o
carrossel está configurado para avançar sozinho e que não existem controles
de anterior/próximo.

**Por que testar:** um teste registra o comportamento esperado e avisa se
uma mudança posterior, como renomear uma URL, quebrar o fluxo de compra
demonstrativo.

### Encerramento da construção

Com a turma, percorra o caminho de uma página e peça que cada aluno explique
uma camada usando o projeto:

```text
/comprar/django-na-pratica/
    -> livraria/urls.py
    -> catalogo/urls.py
    -> comprar_livro(request, slug)
    -> Livro.objects / SQLite
    -> comprar_livro.html
    -> HTML + CSS do Bootstrap no navegador
```

Finalize separando claramente o que foi implementado do que não foi:
a vitrine lê e apresenta livros; o botão navega para uma página demonstrativa;
nenhuma venda, reserva, cobrança ou transação ocorre.

## 1. O que é necessário

- **Python 3.10 ou superior.** O instalador do Python para Windows precisa
  disponibilizar o comando `py` (Python Launcher) ou o comando `python`.
- Acesso à internet para baixar o Bootstrap pelo CDN quando as páginas forem
  abertas no navegador.
- Um editor de código e um terminal, como o terminal integrado do VS Code.

Para conferir o Python no PowerShell:

```powershell
py --version
```

Se `py` não estiver disponível, tente:

```powershell
python --version
```

O arquivo `requirements.txt` especifica a faixa de versões de Django
compatível com o projeto. O `pip` escolhe uma versão que também seja
compatível com a versão de Python instalada.

## 2. Preparar o ambiente no Windows

Abra o PowerShell na pasta do projeto, isto é, na pasta que contém
`manage.py`. Para verificar a pasta atual e listar os arquivos:

```powershell
Get-Location
Get-ChildItem
```

Crie um ambiente virtual:

```powershell
py -m venv .venv
```

Um **ambiente virtual** é uma instalação isolada de pacotes Python para este
projeto. Assim, instalar Django aqui não altera os pacotes dos outros
projetos do computador.

Ative-o no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativo, normalmente o nome `(.venv)` aparecerá no começo da
linha do terminal. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

`python -m pip` executa o instalador de pacotes usando o mesmo Python que está
ativo no terminal. A opção `-r` pede que ele leia a lista de dependências do
arquivo. Neste projeto, essa lista contém o Django.

> **Se o PowerShell bloquear a ativação:** isso pode acontecer por causa da
> política de execução de scripts da máquina. Não é necessário mudar uma
> configuração global só para acompanhar a aula. Use outro terminal
> autorizado pelo laboratório, como o Prompt de Comando, e ative com
> `.venv\Scripts\activate.bat`. Se a máquina pertence à escola, siga a
> orientação de quem administra esse equipamento.

## 3. Inicializar e abrir o site

Com o ambiente virtual ativo, execute na pasta do projeto:

```powershell
python manage.py migrate
python manage.py carregar_livros
python manage.py runserver
```

O que cada comando faz:

1. `migrate` cria no SQLite as tabelas necessárias às aplicações instaladas,
   incluindo a tabela de livros e as tabelas usadas pelo Django Admin.
2. `carregar_livros` insere ou atualiza os quatro livros de exemplo.
3. `runserver` inicia o servidor de desenvolvimento para que o navegador
   possa acessar o site.

Abra <http://127.0.0.1:8000/>. Deixe o terminal com `runserver` aberto
enquanto usa o site; o servidor para quando o processo é encerrado. Para
finalizá-lo, volte ao terminal e pressione `Ctrl+C`.

### Ver as alterações sem atualizar a página manualmente

Este projeto usa o pacote **django-browser-reload**. Ele mantém o navegador
conectado ao servidor de desenvolvimento; quando detecta uma alteração
relevante no código Python, nos templates ou nos arquivos estáticos, recarrega
a página aberta automaticamente.

O Django puro reinicia o servidor quando alguns arquivos Python mudam, mas
isso não significa que uma aba já aberta no navegador sempre será atualizada.
O pacote completa essa experiência para o desenvolvimento. Você só precisa
deixar `runserver` rodando e a página do site aberta; depois de salvar uma
alteração, aguarde a recarga automática. Não é necessário clicar no botão de
atualizar do navegador.

#### Como o pacote foi conectado ao projeto

1. A dependência `django-browser-reload` está registrada em
   `requirements.txt`. Num novo ambiente, ela é instalada junto com o Django:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Em `livraria/settings.py`, `"django_browser_reload"` está em
   `INSTALLED_APPS`, e
   `"django_browser_reload.middleware.BrowserReloadMiddleware"` aparece no
   fim de `MIDDLEWARE`. O middleware acrescenta o script de monitoramento às
   respostas HTML quando `DEBUG=True`.

3. Em `livraria/urls.py`, a rota
   `path("__reload__/", include("django_browser_reload.urls"))` cria o canal
   pelo qual o navegador recebe os avisos de alteração.

4. Execute `python manage.py runserver` sem a opção `--nothreading`, abra o
   site e deixe a aba ativa enquanto desenvolve.

Não criamos um arquivo `.json` para ativar esse recurso: é a integração de
Django e `django-browser-reload` que faz o monitoramento. Algumas ferramentas
do editor e extensões de servidor estático usam configurações JSON, mas um
servidor estático não executa as views nem os templates do Django. Para este
projeto, a abordagem integrada ao Django também monitora os templates e
reinícios do servidor.

**Experimento para a turma:** abra `catalogo/templates/catalogo/lista_livros.html`,
altere o texto do título, salve e observe a aba do navegador. Depois faça
uma alteração simples numa view ou em outro template. O navegador deve
recarregar automaticamente. Para uma mudança em Python, o Django também
pode reiniciar o servidor; aguarde o terminal indicar que está pronto.

Esse recurso é de desenvolvimento e só injeta o script quando `DEBUG=True`.
Não o use como solução de produção.

### Criar um usuário do painel administrativo

Em outro terminal, também na pasta do projeto e com o ambiente virtual ativo:

```powershell
python manage.py createsuperuser
```

Siga as perguntas do terminal para definir nome de usuário, e-mail opcional e
senha. Depois abra <http://127.0.0.1:8000/admin/>, entre com essa conta e
cadastre, edite ou remova livros.

**Admin e servidor são conceitos diferentes:** `createsuperuser` cria uma
conta no banco; `runserver` inicia o servidor. É possível executar comandos
administrativos em um terminal e manter o servidor rodando em outro.

## 4. Tour pela estrutura de arquivos

```text
manage.py
requirements.txt
livraria/
    settings.py
    urls.py
    wsgi.py
catalogo/
    admin.py
    apps.py
    models.py
    tests.py
    urls.py
    views.py
    migrations/
    management/commands/carregar_livros.py
    templates/
        400.html
        403.html
        404.html
        500.html
    templates/catalogo/
        base.html
        lista_livros.html
        comprar_livro.html
        quem_somos.html
        politica_trocas.html
```

### Projeto e aplicação

- **`livraria/` é o projeto Django:** reúne configurações e o ponto de entrada
  central das URLs do site.
- **`catalogo/` é uma aplicação Django:** reúne uma funcionalidade do site —
  neste caso, os livros e as páginas do catálogo.
- **`manage.py`** recebe comandos como `runserver`, `migrate`, `test` e o
  comando próprio `carregar_livros`.
- **`requirements.txt`** registra a dependência de Django para que outras
  pessoas possam instalar as mesmas dependências do projeto.

A separação entre projeto e aplicações permite que um mesmo projeto Django
tenha várias áreas, como catálogo, clientes e pedidos.

### Arquivos que vale localizar durante a aula

- `livraria/settings.py`: configura aplicações, banco de dados, idioma e
  templates.
- `livraria/urls.py`: conecta as URLs gerais do projeto às URLs do catálogo
  e do admin.
- `catalogo/models.py`: define os dados que serão guardados para cada livro.
- `catalogo/migrations/0001_initial.py`: registra a migração que cria a
  tabela do modelo `Livro`.
- `catalogo/views.py`: busca os dados e seleciona o template da resposta.
- `catalogo/urls.py`: associa endereços web às funções de view, incluindo
  as páginas informativas “Quem somos” e “Política de trocas”.
- `catalogo/templates/catalogo/`: contém os HTML renderizados pelo Django.
- `catalogo/templates/400.html`, `403.html`, `404.html` e `500.html`:
  personalizam as páginas de erro HTTP.
- `catalogo/admin.py`: configura como o modelo aparece no painel
  administrativo.
- `catalogo/tests.py`: verifica comportamentos importantes das páginas.
- `catalogo/management/commands/carregar_livros.py`: implementa o comando
  que prepara dados de exemplo.

## 5. Como uma página chega ao navegador

Use a página do detalhe como exemplo. Ao visitar
`/comprar/django-na-pratica/`, o Django faz, simplificadamente, este percurso:

1. **URL do navegador:** o visitante faz uma requisição para o servidor.
2. **Roteamento do projeto:** `livraria/urls.py` encaminha a URL raiz para
   `catalogo/urls.py`.
3. **Roteamento da aplicação:** `catalogo/urls.py` reconhece
   `comprar/<slug:slug>/` e captura o texto `django-na-pratica`.
4. **View:** `comprar_livro` recebe esse valor como argumento e procura o
   livro no banco.
5. **ORM:** `Livro.objects` traduz a consulta Python para uma consulta ao
   SQLite.
6. **Template:** se o livro existir, o Django renderiza
   `comprar_livro.html` com o objeto livro disponível no contexto.
7. **Resposta HTTP:** o navegador recebe o HTML renderizado e solicita
   também os estilos e scripts necessários.

Se não houver livro com o slug solicitado, `get_object_or_404` gera uma
resposta HTTP 404. Isso é preferível a mostrar uma página de compra sem
informações ou a esconder silenciosamente o erro.

O caminho do catálogo usa as mesmas etapas, mas a view consulta a lista de
livros e envia vários objetos ao template da listagem.

## 6. Construir o modelo e entender as migrações

Abra `catalogo/models.py`. A classe `Livro` herda de `models.Model`, portanto
o Django a trata como um modelo do ORM. Cada atributo declarado com
`models.CharField`, `models.TextField` ou `models.DecimalField` representa um
campo salvo no banco de dados:

- `titulo` e `autor` são textos de tamanho limitado;
- `slug` é uma versão adequada para compor uma URL e tem valor único;
- `descricao` é um texto mais longo;
- `preco` usa um campo decimal, mais adequado para representar valores
  monetários do que um número de ponto flutuante;
- `estilo_capa` usa opções fixas para selecionar as cores da capa.

`__str__` define uma representação legível do livro, por exemplo no admin.
`Meta` configura detalhes de apresentação e ordenação. `get_absolute_url()`
devolve a rota associada a um livro, usando o nome da URL em vez de repetir
uma string de endereço em diferentes partes do projeto.

### Do modelo para a tabela

Uma **migração** é um arquivo Python que descreve uma mudança da estrutura
do banco. Para praticar a criação de uma migração após mudar o modelo:

```powershell
python manage.py makemigrations
```

Esse comando compara os modelos atuais com as migrações existentes e gera o
arquivo de mudança necessário. Ele **não aplica** a mudança ao banco. Para
aplicar as migrações pendentes:

```powershell
python manage.py migrate
```

O projeto já vem com a migração inicial. Por isso, ao executar
`makemigrations` sem alterar os modelos, é esperado que o Django informe que
não há mudanças detectadas. Depois de modificar um modelo em um exercício,
execute os dois comandos e examine o novo arquivo dentro de
`catalogo/migrations/`.

## 7. Popular e administrar os livros

O arquivo
`catalogo/management/commands/carregar_livros.py` mostra como criar um
comando próprio do Django. O comando percorre uma lista de dados e usa
`update_or_create`:

- se já existe um livro com o mesmo `slug`, atualiza os dados;
- se ainda não existe, cria o livro.

Isso permite executar `python manage.py carregar_livros` várias vezes sem
criar cópias dos mesmos exemplos. Para observar o cadastro pelo admin:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Em outro terminal, visite <http://127.0.0.1:8000/admin/> e entre. O arquivo
`catalogo/admin.py` registra `Livro` no admin e define colunas, filtros,
campos de busca e o preenchimento do `slug` a partir do título.

**Pergunta para a turma:** quando o admin preenche o `slug`, isso substitui
a necessidade de verificar que o valor é único no banco? Não: a interface
ajuda a pessoa que cadastra, e a restrição `unique=True` no modelo também
impõe unicidade no banco.

## 8. Ligar URLs, views e templates

### URLs do projeto e da aplicação

No arquivo `livraria/urls.py`, a rota `/admin/` aponta para o admin do Django;
a rota vazia inclui as URLs de `catalogo`. Em `catalogo/urls.py`, há duas
rotas nomeadas:

- `lista`: página inicial do catálogo, em `/`;
- `comprar`: página de detalhe, em `/comprar/<slug>/`.

O nome da rota pode ser usado com `{% url 'catalogo:comprar' livro.slug %}`
ou, como no projeto, `{{ livro.get_absolute_url }}`. Usar nomes ajuda a
manter links corretos se o formato dos endereços mudar.

### Views e consultas

Em `catalogo/views.py`:

- `lista_livros` consulta `Livro.objects.all()` e envia o resultado ao
  template como `livros`;
- `comprar_livro` consulta um livro por `slug` e envia o resultado como
  `livro`;
- `render` combina o template e os dados do contexto para construir a
  resposta HTML;
- `get_object_or_404` responde com 404 quando a consulta não encontra o
  livro solicitado.

Uma view conecta a requisição HTTP à lógica da aplicação. Ela não desenha a
página: os templates são responsáveis pela apresentação.

## 9. Montar o catálogo em HTML com Bootstrap

Abra `catalogo/templates/catalogo/base.html` e
`catalogo/templates/catalogo/lista_livros.html`.

### Herança de templates

`base.html` define a estrutura comum: documento HTML, idioma, área de
navegação, conteúdo principal, rodapé e inclusão do Bootstrap e do CSS da
aplicação. O template do catálogo usa:

- `{% extends "catalogo/base.html" %}` para reutilizar essa estrutura;
- `{% block title %}` para personalizar o título da aba do navegador;
- `{% block content %}` para fornecer o conteúdo específico da página.

Quando a página de detalhe herda a mesma base, as duas telas mantêm o mesmo
estilo geral sem duplicar todo o HTML.

O mesmo princípio vale para as páginas `quem_somos.html` e
`politica_trocas.html`: links de navegação e rodapé ficam num único arquivo,
e o conteúdo específico fica em cada template. Assim, uma alteração no menu
é feita uma vez e aparece em todo o site.

### Tags e variáveis do Django Template Language

Na página do catálogo, o Django Template Language usa:

- `{% for livro in livros %}` para criar um cartão para cada objeto;
- `{{ livro.titulo }}` e outras expressões para imprimir dados do livro;
- `{% empty %}` para mostrar uma mensagem quando a lista não tem resultados;
- `{% url ... %}` para construir links a partir de uma rota nomeada.

O Django escapa valores de texto automaticamente em templates comuns.
Assim, um título digitado no admin é tratado como texto, em vez de ser
interpretado diretamente como HTML.

### Responsividade

Cada cartão ocupa colunas com classes Bootstrap como `col-sm-6`,
`col-lg-4` e `col-xl-3`. A quantidade de colunas varia com a largura da
tela, então os livros podem aparecer em uma ou mais colunas sem criar uma
folha de estilos separada para cada tamanho de dispositivo.

O Bootstrap é carregado do CDN em `base.html`. Isso mantém os arquivos do
framework fora deste repositório e requer acesso à internet no navegador.
Classes prontas do Bootstrap controlam a grade, os cartões, a navegação,
o rodapé, os avisos e as capas, sem uma folha CSS própria.

### Capas de livros

Quando `imagem_capa_url` está preenchido, o navegador carrega a imagem do
endereço informado. Quando está vazio, o template monta uma capa simples com
classes Bootstrap de alinhamento, cor e espaçamento. O projeto guarda a URL,
não baixa nem hospeda o arquivo.

## 10. Página de detalhe e carrossel automático

O botão **Comprar** não é um formulário nem uma transação: é um link para a
página de detalhe do livro. Em `comprar_livro.html`, o template apresenta
título, autor, descrição, preço e uma mensagem que avisa que não há pedido
nem pagamento.

O componente de carrossel usa os atributos do Bootstrap:

- `data-bs-ride="carousel"` inicia a rotação automática;
- `data-bs-interval="4500"` indica 4.500 milissegundos — 4,5 segundos —
  entre os slides;
- `data-bs-pause="false"` mantém a rotação se o visitante passar o mouse
  sobre o carrossel;
- `data-bs-touch="false"` desativa a navegação por gesto de toque;
- `carousel-item active` identifica o slide que aparece primeiro.

Não existem botões de anterior/próximo nem indicadores no template. Por
isso, o visitante vê os slides avançarem automaticamente, mas não recebe
controles para escolher um slide. O JavaScript do Bootstrap é carregado em
`base.html` para que o componente funcione.

**Discussão de acessibilidade:** movimento automático pode distrair algumas
pessoas. Em um site de produção, avalie se deve existir um controle de pausa,
uma preferência por movimento reduzido e conteúdo equivalente que não dependa
de acompanhar a animação. Neste exercício, a ausência de controles atende ao
requisito da demonstração; a conversa sobre acessibilidade ajuda a turma a
entender que decisões de interface também têm impactos.

## 11. Testar o comportamento

Execute:

```powershell
python manage.py test catalogo
```

O Django cria um banco temporário para os testes e o remove ao terminar.
`catalogo/tests.py` verifica que:

1. a listagem responde com sucesso e mostra o livro cadastrado;
2. o link de compra leva ao endereço associado ao livro;
3. a página de detalhe contém o livro e os atributos do carrossel automático;
4. os controles de navegação não aparecem;
5. uma página para livro inexistente responde com HTTP 404;
6. o comando de exemplo pode ser executado novamente sem duplicar livros.
7. os handlers do Django exibem as páginas personalizadas para os erros 400,
   403, 404 e 500.

Os testes automatizados não verificam se o CDN está acessível nem fazem uma
inspeção visual no navegador. Para isso, abra as duas páginas e confira a
grade, os estilos, a navegação e a troca automática dos slides.

### Páginas personalizadas para erros

O Django procura automaticamente os templates com estes nomes quando
precisa exibir uma página de erro:

- `400.html`: solicitação inválida;
- `403.html`: acesso negado;
- `404.html`: endereço ou conteúdo não encontrado;
- `500.html`: erro inesperado no servidor.

Neste projeto eles ficam diretamente em `catalogo/templates/`, na raiz de
templates da aplicação. Não ficam dentro de `catalogo/templates/catalogo/`:
os nomes `400.html`, `403.html`, `404.html` e `500.html` são convenções
usadas pelos handlers padrão do Django. Como `APP_DIRS=True`, o carregador de
templates encontra os arquivos da aplicação. Não é preciso criar rotas
manuais para cada erro nem escrever handlers próprios para personalizar
somente o HTML.

Cada página usa classes prontas do Bootstrap e um link de volta para `/`.
Os templates de erro são independentes da base geral para que um problema no
layout principal ou nas URLs do site não impeça a exibição da página 500.

**A diferença entre desenvolvimento e produção importa:** com `DEBUG=True`,
o Django mostra páginas técnicas detalhadas para ajudar quem desenvolve;
ele não usa as páginas 400/403/404/500 personalizadas. Em produção,
`DEBUG` deve ser `False`, e o Django então usa os templates personalizados.
Não mantenha `DEBUG=False` com `ALLOWED_HOSTS=[]`: durante a aula, para
visualizar as páginas no navegador local, ajuste temporariamente em
`livraria/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

Reinicie `runserver` e acesse um endereço que não exista, por exemplo
<http://127.0.0.1:8000/pagina-que-nao-existe/>. Você deverá ver a página 404
da livraria, não a tela técnica do Django. Depois do experimento, restaure
`DEBUG = True` para continuar desenvolvendo. A configuração de produção
precisa de hosts reais e outras medidas de segurança; esses valores locais
não são uma configuração pronta para publicar.

Não provoque um erro 500 num site público para testar a página. Os testes
automatizados chamam os handlers de erro do Django em condições controladas
e verificam o código HTTP e o conteúdo correspondente.

## 12. Sequência sugerida para uma aula

Uma sequência que deixa espaço para demonstração e perguntas:

1. **Apresentação do resultado:** mostre o catálogo, redimensione a janela,
   clique em **Comprar** e observe a troca de slides.
2. **Mapa dos arquivos:** diferencie projeto e aplicação; localize
   configurações, URLs, modelo, views e templates.
3. **Dados:** examine `Livro`, explique campos e slug; aplique a migração e
   carregue os exemplos.
4. **Percurso de uma requisição:** acompanhe a URL desde
   `livraria/urls.py` até a view, a consulta ao banco e o template.
5. **Apresentação:** analise a herança de templates, o loop do catálogo, as
   classes Bootstrap e as regras do CSS.
6. **Admin:** crie ou atualize um livro e confira a mudança no site.
7. **Qualidade:** execute os testes e discuta o motivo de cada verificação.
8. **Limites e próximo passo:** compare a demonstração com requisitos reais
   de uma loja, sem recolher dados de pagamento.

### Perguntas para verificar compreensão

- Qual a diferença entre o projeto `livraria` e a aplicação `catalogo`?
- Onde a URL da página de detalhe captura o slug do livro?
- Qual arquivo procura o livro no banco? Qual arquivo gera o HTML?
- O que `makemigrations` faz que `migrate` não faz?
- Qual a diferença entre um campo `DecimalField` e um `FloatField` para
  representar um preço?
- Como o template resolve o que deve mostrar quando não há livros?
- Por que `get_object_or_404` é preferível a retornar uma página de detalhe
  sem um livro?
- Quais evidências no HTML confirmam que o carrossel é automático e não tem
  controles?
- O que ainda falta antes de chamar esse site de loja com compras reais?

## 13. Exercícios práticos

Faça uma mudança por vez. Quando alterar `models.py`, lembre-se de gerar e
aplicar as migrações antes de testar.

### Exercício A — criar uma categoria

1. Adicione ao modelo um campo `categoria`.
2. Crie e aplique a migração.
3. Atualize um ou mais livros pelo admin.
4. Mostre a categoria no cartão e na página de detalhe.

**Conceitos praticados:** campos, migrações, admin e apresentação de dados.

### Exercício B — adicionar uma busca

1. Crie um formulário HTML com um campo de pesquisa.
2. Leia o texto enviado pela view.
3. Use o ORM para filtrar por título ou autor.
4. Renderize os resultados no catálogo e mantenha o caso sem resultados
   compreensível.

**Conceitos praticados:** requisições GET, parâmetros de URL, consultas e
estado vazio.

### Exercício C — mostrar disponibilidade

1. Adicione ao modelo um campo para a quantidade em estoque.
2. Atualize o admin para exibir esse dado.
3. Mostre “Disponível” ou “Indisponível” no cartão.
4. Escreva um teste para cada situação.

**Conceitos praticados:** valores numéricos, lógica de template e testes.
Esse exercício ainda não deve diminuir o estoque nem registrar compras.

### Exercício D — investigar o 404

1. Abra uma URL de detalhe com um slug que não existe.
2. Observe a resposta no navegador.
3. Localize `get_object_or_404` na view.
4. Modifique o teste para verificar também que o texto do livro inexistente
   não aparece na página.

**Conceitos praticados:** códigos HTTP, consulta ao banco e testes de
comportamento.

## 14. Solução de problemas comuns

### `py` ou `python` não foi encontrado

Confira se o Python está instalado e se foi adicionado ao PATH. No Windows,
feche e abra novamente o terminal depois de instalar. Use
`py --version` ou `python --version` para descobrir qual comando está
disponível.

### `No module named django`

Ative o ambiente virtual e instale as dependências:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Verifique também que o terminal está na mesma pasta que contém
`requirements.txt` e `manage.py`.

### Erro sobre tabela inexistente ou migrações pendentes

Execute:

```powershell
python manage.py migrate
```

Se você acabou de adicionar ou alterar um campo em `models.py`, execute
primeiro `python manage.py makemigrations` e depois `python manage.py migrate`.

### O catálogo aparece vazio

Carregue os dados de exemplo:

```powershell
python manage.py carregar_livros
```

Ou cadastre um livro em <http://127.0.0.1:8000/admin/>. Se o admin ainda não
tiver uma conta, crie uma com `python manage.py createsuperuser`.

### A página abre, mas o Bootstrap não tem estilo

O Bootstrap deste projeto vem de um CDN. Confira a conexão à internet e o
painel de rede do navegador. Sem o CDN, o HTML continua existindo, mas as
classes visuais do Bootstrap não serão carregadas.

### A ativação do ambiente virtual não funciona

Confirme que criou a pasta `.venv` na pasta atual. No PowerShell use
`.\.venv\Scripts\Activate.ps1`; no Prompt de Comando use
`.venv\Scripts\activate.bat`. A política de execução de scripts pode ser
gerenciada pela escola ou pela organização.

## 15. Limites e próximos passos

Este projeto é um exercício de catálogo e navegação. Ele **não** implementa
autenticação de clientes, carrinho, pedidos, cálculo de frete, controle de
estoque após uma venda, confirmação por e-mail, pagamentos nem proteção
operacional para deploy.

Para evoluí-lo como atividade avançada, a turma pode começar desenhando o
fluxo de negócio e os modelos de pedido antes de escrever código. Uma
integração real de pagamento exige uma solução apropriada, tratamento seguro
de dados e testes próprios. Não use números reais de cartão, senhas reais ou
dados pessoais de estudantes neste exercício.