# 🛒 Geek Store API — FastAPI + PostgreSQL

API REST de e-commerce fictício desenvolvida com **Python, FastAPI e PostgreSQL**, com foco em desenvolvimento backend e na construção de uma aplicação estruturada e próxima de um projeto real.

O projeto começou como um CRUD simples de produtos utilizando uma lista em memória e evoluiu gradualmente para uma aplicação backend completa, incorporando banco de dados relacional, autenticação JWT, autorização por roles, categorias, carrinho de compras, pedidos, controle de estoque, pagamento simulado, área administrativa, testes automatizados, migrations com Alembic e ambiente containerizado com Docker.

O principal objetivo é consolidar conhecimentos de desenvolvimento backend e demonstrar a evolução de um projeto desde um CRUD básico até uma API REST completa.

---

## 🚀 Tecnologias

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Psycopg
* PostgreSQL
* JWT
* bcrypt
* Alembic
* Pytest
* Docker
* Docker Compose
* Git e GitHub

---

## 📦 Sobre o projeto

A **Geek Store API** simula o backend de uma loja virtual fictícia voltada para produtos geek.

A aplicação permite que usuários:

* Criem uma conta
* Façam login
* Consultem seus dados
* Atualizem seus dados
* Excluam sua conta
* Visualizem produtos e categorias
* Pesquisem e filtrem produtos
* Adicionem produtos ao carrinho
* Alterem a quantidade de produtos no carrinho
* Removam produtos do carrinho
* Criem pedidos
* Consultem seus pedidos
* Realizem um pagamento simulado
* Cancelem pedidos permitidos

Administradores possuem permissões adicionais para gerenciar produtos, categorias, usuários e pedidos.

---

# 🏗️ Arquitetura

A aplicação segue uma estrutura baseada na separação entre rotas, validação, regras de negócio, ORM e banco de dados.

```text
Cliente
   ↓
FastAPI
   ↓
Pydantic
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL
```

### Fluxo de autenticação

```text
Cliente
   ↓
Login
   ↓
JWT
   ↓
Authorization: Bearer <token>
   ↓
get_current_user
   ↓
Autenticação
   ↓
Autorização / Role
```

---

# 📂 Estrutura do projeto

```text
crud-produtos/
│
├── alembic/
│   ├── versions/
│   │   └── 6fdb58e707fc_initial_migration.py
│   ├── env.py
│   └── script.py.mako
│
├── routers/
│   ├── admin.py
│   ├── cart.py
│   ├── categories.py
│   ├── orders.py
│   ├── products.py
│   └── users.py
│
├── tests/
│   ├── conftest.py
│   ├── test_admin.py
│   ├── test_cart.py
│   ├── test_categories.py
│   ├── test_orders.py
│   ├── test_products.py
│   └── ...
│
├── auth.py
├── database.py
├── main.py
├── models.py
├── schema.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .env.example
├── .gitignore
├── processo.md
└── README.md
```

---

# 🛍️ Funcionalidades

## 👤 Usuários

### Criar usuário

```http
POST /users
```

Permite criar uma nova conta.

A senha possui validações de segurança e é armazenada utilizando hash com `bcrypt`.

### Login

```http
POST /users/login
```

Realiza a autenticação do usuário e retorna um token JWT.

### Usuário autenticado

```http
GET /users/me
```

Retorna os dados do usuário autenticado.

### Atualizar usuário

```http
PATCH /users/{user_id}
```

Permite atualizar os dados do próprio usuário.

### Excluir usuário

```http
DELETE /users/{user_id}
```

Permite que o usuário exclua sua própria conta.

---

# 📦 Produtos

### Criar produtos

```http
POST /products
```

Permite que administradores cadastrem produtos.

### Listar produtos

```http
GET /products
```

Retorna os produtos cadastrados.

A rota também possui recursos de pesquisa, filtros e paginação.

Exemplos:

```text
/products?name=batman
/products?category=livros
/products?min_price=20
/products?max_price=100
```

### Buscar produto

```http
GET /products/{product_id}
```

Retorna um produto específico.

### Atualizar preço

```http
PATCH /products/{product_id}
```

Atualiza o preço de um produto.

### Atualizar estoque

```http
PATCH /products/{product_id}/stock
```

Atualiza o estoque de um produto.

### Excluir produto

```http
DELETE /products/{product_id}
```

Remove um produto.

As operações de gerenciamento de produtos são restritas a administradores.

---

# 🗂️ Categorias

### Criar categoria

```http
POST /categories
```

Cria uma nova categoria.

### Listar categorias

```http
GET /categories
```

Retorna todas as categorias cadastradas.

### Buscar categoria

```http
GET /categories/{category_id}
```

Retorna uma categoria juntamente com seus produtos.

### Atualizar categoria

```http
PATCH /categories/{category_id}
```

Atualiza uma categoria.

### Excluir categoria

```http
DELETE /categories/{category_id}
```

Remove uma categoria.

Uma categoria que possui produtos não pode ser excluída.

As operações de gerenciamento de categorias são restritas a administradores.

---

# 🛒 Carrinho de compras

Cada usuário possui seu próprio carrinho.

### Visualizar carrinho

```http
GET /cart
```

### Adicionar produto

```http
POST /cart
```

### Alterar quantidade

```http
PATCH /cart/{product_id}
```

### Remover produto

```http
DELETE /cart/{product_id}
```

O sistema verifica a disponibilidade do produto no estoque antes de adicionar ou alterar sua quantidade.

Produtos não são duplicados no carrinho. Caso o produto já esteja presente, sua quantidade é atualizada.

O sistema também registra o preço do produto no momento em que ele foi adicionado ao carrinho por meio do campo `added_price`.

Caso o preço atual seja diferente do preço registrado, a API consegue identificar essa alteração.

---

# 📋 Pedidos

### Criar pedido

```http
POST /orders
```

Cria um pedido utilizando os produtos presentes no carrinho.

Durante a criação do pedido:

1. O estoque dos produtos é verificado.
2. O estoque é atualizado.
3. Os itens do carrinho são transferidos para o pedido.
4. O preço utilizado na compra é registrado no `OrderItem`.
5. O carrinho é esvaziado.

### Listar pedidos

```http
GET /orders
```

Retorna os pedidos do usuário autenticado.

### Visualizar pedido

```http
GET /orders/{order_id}
```

Retorna os detalhes de um pedido específico.

### Pagamento

```http
POST /orders/{order_id}/pay
```

Realiza um **pagamento simulado** e altera o status do pedido.

Não existe integração com um gateway de pagamento real.

### Cancelamento

```http
PATCH /orders/{order_id}/cancel
```

Permite cancelar pedidos que ainda podem ser cancelados de acordo com as regras de negócio.

Quando um pedido é cancelado, os produtos correspondentes retornam ao estoque.

---

# 🔐 Autenticação e autorização

A API utiliza **JWT (JSON Web Token)** para autenticação.

O fluxo é:

```text
Cadastro
   ↓
Login
   ↓
JWT
   ↓
Authorization: Bearer <token>
   ↓
Usuário autenticado
```

Existem dois níveis de acesso:

```text
user
admin
```

Usuários comuns possuem acesso às funcionalidades relacionadas à própria conta, carrinho e pedidos.

Administradores possuem permissões adicionais para gerenciamento da loja.

---

# 👑 Área administrativa

Administradores podem:

* Listar todos os pedidos
* Visualizar pedidos específicos
* Atualizar status dos pedidos
* Listar usuários
* Visualizar usuários
* Alterar a role de usuários
* Gerenciar produtos
* Gerenciar categorias

A alteração de permissões utiliza as roles:

```text
user
admin
```

O sistema também possui regras para impedir ações administrativas indevidas, como a alteração da própria role de administrador.

---

# 🔄 Status dos pedidos

Os pedidos possuem transições de status controladas pelas regras de negócio.

Fluxo principal:

```text
PENDENTE
   ↓
PAGO
   ↓
ENVIADO
   ↓
ENTREGUE
```

Também existem fluxos de cancelamento permitidos de acordo com o status atual do pedido.

---

# 🗄️ Banco de dados

O projeto utiliza **PostgreSQL** como banco de dados relacional e **SQLAlchemy** como ORM.

Principais entidades:

```text
User
 │
 └── Cart
      │
      └── CartItem
           │
           └── Product
                 │
                 └── Category

User
 │
 └── Order
      │
      └── OrderItem
           │
           └── Product
```

Principais tabelas:

```text
users
products
categories
carts
cart_items
orders
order_items
```

### Valores monetários

Os valores monetários utilizam `Decimal` na aplicação e `NUMERIC(10,2)` no PostgreSQL, evitando problemas de precisão comuns em operações financeiras com `float`.

---

# 🔄 Migrations

O projeto utiliza **Alembic** para versionamento e controle da estrutura do banco de dados.

Criar uma migration:

```powershell
alembic revision --autogenerate -m "description"
```

Aplicar as migrations:

```powershell
alembic upgrade head
```

Verificar a migration atual:

```powershell
alembic current
```

A migration inicial atual é:

```text
6fdb58e707fc_initial_migration.py
```

Ela é responsável pela criação da estrutura inicial do banco de dados.

---

# 🧪 Testes

O projeto utiliza **Pytest** para testes automatizados.

Executar todos os testes:

```powershell
pytest
```

### Resultado atual

```text
66 passed
```

Os testes cobrem diferentes partes da aplicação, incluindo:

* Produtos
* Categorias
* Usuários
* Autenticação
* Autorização
* Carrinho
* Pedidos
* Pagamentos
* Cancelamentos
* Controle de estoque
* Área administrativa
* Permissões
* Validações
* Regras de negócio

Os testes utilizam uma configuração de banco de dados separada para evitar alterações no banco utilizado pela aplicação.

---

# 🐳 Docker

O projeto possui suporte a **Docker e Docker Compose** para executar a API e o PostgreSQL em containers.

A aplicação utiliza dois serviços principais:

```text
┌─────────────────────┐
│     FastAPI API     │
│    loja-geek-api    │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│     PostgreSQL      │
│     postgres-dev    │
└─────────────────────┘
```

### Iniciar os containers

```powershell
docker compose up -d --build
```

### Verificar os containers

```powershell
docker compose ps
```

### Executar migrations

```powershell
docker compose exec api python -m alembic upgrade head
```

### Parar os containers

```powershell
docker compose down
```

O PostgreSQL utiliza um volume Docker para persistir os dados mesmo quando os containers são reiniciados.

---

# ⚙️ Como executar o projeto

## Opção 1 — Docker

Essa é a forma recomendada para reproduzir o ambiente da aplicação.

### 1. Clonar o repositório

```bash
git clone https://github.com/devlavin/crud-produtos.git
cd crud-produtos
```

### 2. Configurar o `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/loja
JWT_SECRET_KEY=SUA_CHAVE_SECRETA
```

> O arquivo `.env` não deve ser enviado para o GitHub.

Utilize o `.env.example` como referência.

### 3. Iniciar os containers

```powershell
docker compose up -d --build
```

### 4. Aplicar as migrations

```powershell
docker compose exec api python -m alembic upgrade head
```

A API estará disponível em:

```text
http://localhost:8000
```

---

## Opção 2 — Ambiente Python local

Também é possível executar a aplicação diretamente em um ambiente virtual Python.

### 1. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 2. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie o arquivo `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/loja
JWT_SECRET_KEY=SUA_CHAVE_SECRETA
```

### 5. Executar as migrations

```powershell
alembic upgrade head
```

### 6. Iniciar a API

```powershell
uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

---

# 📚 Documentação da API

O FastAPI gera automaticamente uma documentação interativa para os endpoints.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

# 🔒 Segurança

O projeto implementa algumas práticas básicas de segurança:

* Senhas armazenadas com hash utilizando `bcrypt`
* Autenticação utilizando JWT
* Autorização baseada em roles
* Variáveis de ambiente para informações sensíveis
* `.env` protegido pelo `.gitignore`
* Validação de dados utilizando Pydantic
* Banco de dados separado para testes
* Validação de estoque
* Controle das transições de status dos pedidos
* Restrições de acesso às operações administrativas

O projeto não utiliza dados reais de clientes e o pagamento é apenas simulado para fins de estudo.

---

# 🎯 Objetivos de aprendizado

O projeto foi desenvolvido para consolidar conhecimentos em:

* Python
* FastAPI
* APIs REST
* Pydantic
* SQLAlchemy
* ORM
* PostgreSQL
* Relacionamentos entre tabelas
* JWT
* Autenticação
* Autorização
* Hash de senhas
* Carrinho de compras
* Processamento de pedidos
* Controle de estoque
* Migrations com Alembic
* Testes automatizados com Pytest
* Docker
* Docker Compose
* Git e GitHub
* Estruturação de aplicações backend

---

# 🚧 Status do projeto

O projeto evoluiu de um CRUD simples utilizando dados em memória para uma aplicação backend estruturada, com banco de dados, autenticação, regras de negócio, testes e ambiente containerizado.

## Concluído

* [x] CRUD de produtos
* [x] PostgreSQL
* [x] SQLAlchemy
* [x] Pydantic
* [x] Autenticação de usuários
* [x] JWT
* [x] Autorização por role
* [x] Categorias
* [x] Carrinho de compras
* [x] Controle de quantidade no carrinho
* [x] Controle de estoque
* [x] Pedidos
* [x] Pagamento simulado
* [x] Cancelamento de pedidos
* [x] Área administrativa
* [x] Testes automatizados
* [x] 66 testes passando
* [x] Alembic
* [x] Migrations
* [x] Docker
* [x] Docker Compose
* [x] Configuração por variáveis de ambiente
* [x] Padronização dos nomes do projeto

## Próximos passos

* [ ] Refatoração do código
* [ ] Melhorar tratamento de erros
* [ ] Revisão de segurança
* [ ] Deploy em produção
* [ ] Desenvolvimento do frontend
* [ ] Integração entre frontend e API

---

# 💻 Projeto

Projeto desenvolvido como parte dos estudos de **desenvolvimento backend com Python**, com foco na construção de uma API REST e na evolução gradual de um CRUD simples para uma aplicação de e-commerce fictícia.

O projeto busca aplicar conceitos presentes no desenvolvimento backend real, incluindo autenticação, autorização, relacionamentos entre entidades, regras de negócio, controle de estoque, testes automatizados, migrations e containerização.

**Backend:** Python + FastAPI + PostgreSQL

**ORM:** SQLAlchemy

**Autenticação:** JWT + bcrypt

**Testes:** Pytest

**Migrations:** Alembic

**Containerização:** Docker + Docker Compose

**Objetivo:** aprendizado, prática e construção de portfólio.
