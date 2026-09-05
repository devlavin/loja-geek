````markdown
# 🛒 Geek Store API — FastAPI + PostgreSQL

API REST desenvolvida com **Python, FastAPI e PostgreSQL**, simulando o backend de uma loja geek fictícia.

O projeto começou como um CRUD simples de produtos utilizando uma lista em memória e foi evoluindo gradualmente para uma aplicação backend completa, com banco de dados, autenticação, autorização, categorias, carrinho de compras, pedidos, pagamento simulado, área administrativa, testes automatizados e migrations.

O principal objetivo é praticar conceitos de desenvolvimento backend e construir uma API estruturada e próxima de um projeto real.

---

## 🚀 Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Psycopg
- PostgreSQL
- JWT
- bcrypt
- Alembic
- Pytest
- Git e GitHub

---

## 📦 Sobre o projeto

A **Geek Store API** representa o backend de uma loja virtual fictícia voltada para produtos geek.

A aplicação permite que usuários:

- Criem uma conta
- Façam login
- Consultem seus dados
- Atualizem seus dados
- Excluam sua conta
- Visualizem produtos e categorias
- Adicionem produtos ao carrinho
- Alterem a quantidade de produtos no carrinho
- Removam produtos do carrinho
- Criem pedidos
- Consultem seus pedidos
- Realizem um pagamento simulado
- Cancelem pedidos permitidos

Administradores possuem permissões adicionais para gerenciar produtos, categorias, usuários e pedidos.

---

## 🏗️ Arquitetura

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
````

Autenticação:

```text
Cliente
   ↓
Login
   ↓
JWT
   ↓
FastAPI
   ↓
get_current_user
   ↓
Autorização
```

---

## 📂 Estrutura do projeto

```text
python/
│
├── alembic/
│   ├── versions/
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
├── .env.example
├── .gitignore
├── alembic.ini
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

Permite atualizar dados do próprio usuário.

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

Permite que administradores cadastrem um ou vários produtos.

### Listar produtos

```http
GET /products
```

Retorna os produtos cadastrados.

Também possui filtros e paginação.

Exemplos de filtros:

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

Essas operações de gerenciamento são restritas a administradores.

---

# 🗂️ Categorias

### Criar categoria

```http
POST /categories
```

### Listar categorias

```http
GET /categories
```

### Buscar categoria

```http
GET /categories/{category_id}
```

Retorna a categoria juntamente com seus produtos.

### Atualizar categoria

```http
PATCH /categories/{category_id}
```

### Excluir categoria

```http
DELETE /categories/{category_id}
```

Uma categoria que possui produtos não pode ser excluída.

---

# 🛒 Carrinho

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

---

# 📋 Pedidos

### Criar pedido

```http
POST /orders
```

Cria um pedido utilizando os produtos presentes no carrinho.

Durante a criação:

* O estoque é verificado.
* O estoque dos produtos é atualizado.
* Os itens do carrinho são transferidos para o pedido.
* O carrinho é esvaziado.
* O preço utilizado no pedido é registrado no `OrderItem`.

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

Não existe integração com gateway de pagamento real.

### Cancelamento

```http
PATCH /orders/{order_id}/cancel
```

Permite cancelar pedidos que ainda podem ser cancelados.

Quando um pedido é cancelado, os produtos retornam ao estoque.

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

Os status dos pedidos possuem transições controladas:

```text
PENDENTE
   ↓
PAGO
   ↓
ENVIADO
   ↓
ENTREGUE
```

Também existem fluxos de cancelamento permitidos conforme o status do pedido.

---

# 🗄️ Banco de dados

O projeto utiliza **PostgreSQL** como banco de dados e **SQLAlchemy** como ORM.

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

---

# 🔄 Migrations

O projeto utiliza **Alembic** para controle de alterações no banco de dados.

Criar uma migration:

```powershell
alembic revision --autogenerate -m "description"
```

Aplicar migrations:

```powershell
alembic upgrade head
```

Verificar a migration atual:

```powershell
alembic current
```

As migrations permitem versionar a estrutura do banco de dados junto com o código da aplicação.

---

# 🧪 Testes

O projeto utiliza **Pytest** para testes automatizados.

Executar todos os testes:

```powershell
pytest
```

Os testes cobrem diferentes partes da API, incluindo:

* Produtos
* Categorias
* Usuários
* Autenticação
* Carrinho
* Pedidos
* Pagamentos
* Cancelamentos
* Área administrativa
* Controle de permissões
* Validações
* Estoque

---

# ⚙️ Como executar o projeto

## 1. Clonar o repositório

```bash
git clone https://github.com/devlavin/crud-produtos.git
cd crud-produtos
```

## 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ativar:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Instalar as dependências

```powershell
pip install -r requirements.txt
```

## 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql+psycopg://postgres:SUA_PASSWORD@localhost:5432/fastapi_products
JWT_SECRET_KEY=SUA_CHAVE_SECRETA
```

O arquivo `.env` não deve ser enviado para o GitHub.

Utilize o `.env.example` como referência.

## 5. Configurar o banco

Crie o banco PostgreSQL e execute as migrations:

```powershell
alembic upgrade head
```

## 6. Executar a API

```powershell
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

---

# 📚 Documentação da API

O FastAPI gera automaticamente uma documentação interativa.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# 🔒 Segurança

O projeto utiliza algumas práticas básicas de segurança:

* Senhas armazenadas com `bcrypt`
* Autenticação utilizando JWT
* Controle de acesso baseado em roles
* Variáveis de ambiente para informações sensíveis
* `.env` protegido pelo `.gitignore`
* Validação de dados utilizando Pydantic

O projeto não utiliza dados reais de clientes e o pagamento é apenas simulado para fins de estudo.

---

# 🎯 Objetivos de aprendizado

O projeto tem como objetivo consolidar conhecimentos em:

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
* Fluxo de pedidos
* Controle de estoque
* Migrations com Alembic
* Testes automatizados com Pytest
* Git e GitHub
* Estruturação de aplicações backend

---

# 🚧 Próximos passos

O projeto continuará evoluindo com foco em aproximá-lo de uma aplicação real.

* [x] CRUD de produtos
* [x] PostgreSQL
* [x] SQLAlchemy
* [x] Autenticação
* [x] Autorização por role
* [x] Categorias
* [x] Carrinho
* [x] Pedidos
* [x] Pagamento simulado
* [x] Área administrativa
* [x] Testes automatizados
* [x] Alembic
* [x] Padronização dos nomes do projeto
* [ ] Refatoração do código
* [ ] Melhorar tratamento de erros
* [ ] Docker
* [ ] Deploy
* [ ] Desenvolvimento do frontend
* [ ] Integração entre frontend e API

---

## 💻 Projeto

Projeto desenvolvido como parte dos estudos de **desenvolvimento backend com Python**, com foco em construir uma API REST completa e evoluir gradualmente de um CRUD simples para uma aplicação de e-commerce fictícia.

**Backend:** Python + FastAPI + PostgreSQL

**Objetivo:** aprendizado, prática e construção de portfólio.

```

Eu também **corrigi uma coisa importante conceitualmente**: não faz mais sentido o README ensinar `python database.py` para criar tabela, porque agora entramos no **Alembic**. O fluxo correto do projeto daqui pra frente é `alembic upgrade head`.

E deixei os itens já concluídos como `[x]`, porque agora o README conta a **história atual do projeto**, não mais a história do CRUD inicial. ❤️
```
