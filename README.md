# 🛒 Geek Store

E-commerce fictício desenvolvido para praticar **desenvolvimento full stack**, com foco principalmente em backend.

O projeto começou como um CRUD simples de produtos e evoluiu para uma aplicação completa com autenticação, autorização, banco de dados, carrinho, pedidos, controle de estoque, testes automatizados e Docker.

---

## 🚀 Tecnologias

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* Psycopg
* JWT
* bcrypt
* Alembic
* Pytest

### Frontend

* React
* TypeScript
* Vite
* React Router

### Infraestrutura

* Docker
* Docker Compose
* Git
* GitHub

---

## ✨ Funcionalidades

### 👤 Usuários

* Cadastro
* Login com JWT
* Consulta e atualização de perfil
* Exclusão de conta
* Hash de senhas com bcrypt
* Autorização por roles (`user` / `admin`)

### 📦 Produtos e categorias

* CRUD de produtos
* CRUD de categorias
* Pesquisa e filtros
* Paginação
* Controle de estoque
* Proteção das operações administrativas

### 🛒 Carrinho

* Adicionar produtos
* Alterar quantidade
* Remover produtos
* Validação de estoque
* Controle do preço no momento da adição

### 📋 Pedidos

* Criação de pedidos a partir do carrinho
* Histórico de pedidos
* Detalhes do pedido
* Pagamento simulado
* Cancelamento
* Atualização automática do estoque

### 👑 Administração

* Gerenciamento de usuários
* Alteração de roles
* Gerenciamento de produtos e categorias
* Gerenciamento de pedidos
* Atualização de status

---

## 🏗️ Arquitetura

```text
                 ┌─────────────────┐
                 │     React       │
                 │   TypeScript    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │    FastAPI      │
                 │      JWT        │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   SQLAlchemy    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   PostgreSQL    │
                 └─────────────────┘
```

---

## 🗄️ Banco de dados

Principais entidades:

```text
User
 ├── Cart
 │    └── CartItem
 │         └── Product
 │
 └── Order
      └── OrderItem
           └── Product

Product
 └── Category
```

O projeto utiliza **SQLAlchemy** como ORM e **Alembic** para migrations.

Valores monetários são tratados com `Decimal` na aplicação e `NUMERIC(10,2)` no PostgreSQL.

---

## 🔐 Autenticação

A autenticação utiliza **JWT com Bearer Token**.

```text
Login
  ↓
JWT
  ↓
Authorization: Bearer <token>
  ↓
Usuário autenticado
  ↓
Verificação de permissões
```

Existem dois níveis de acesso:

```text
user
admin
```

---

## 🧪 Testes

O projeto utiliza **Pytest** para testes automatizados.

Atualmente:

```text
66 passed
```

Os testes cobrem autenticação, usuários, produtos, categorias, carrinho, pedidos, estoque, pagamentos e permissões administrativas.

---

## 🐳 Docker

O projeto possui ambiente containerizado utilizando Docker Compose.

```text
┌─────────────────────┐
│   React + Vite      │
│   :5173             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   FastAPI           │
│   :8000             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   PostgreSQL        │
│   :5432             │
└─────────────────────┘
```

### Iniciar o projeto

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Para executar as migrations:

```bash
docker compose exec api python -m alembic upgrade head
```

---

## 📂 Estrutura

```text
loja-geek/
│
├── backend/
│   ├── alembic/
│   ├── routers/
│   ├── tests/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schema.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── processo.md
└── README.md
```

---

## 📌 Status

**Em desenvolvimento / projeto de estudo e portfólio.**

### Concluído

* [x] API REST
* [x] PostgreSQL
* [x] SQLAlchemy
* [x] Autenticação JWT
* [x] Autorização por roles
* [x] Produtos
* [x] Categorias
* [x] Carrinho
* [x] Pedidos
* [x] Controle de estoque
* [x] Pagamento simulado
* [x] Área administrativa
* [x] Testes automatizados
* [x] Alembic
* [x] Docker
* [x] Docker Compose
* [x] Frontend React + TypeScript
* [x] Integração frontend/API

### Próximos passos

* [ ] Refinar interface
* [ ] Melhorar tratamento de erros
* [ ] Revisão de segurança
* [ ] Deploy

---

## 🎯 Objetivo

Projeto desenvolvido para consolidar conhecimentos em **Python, FastAPI, PostgreSQL, React e desenvolvimento de APIs REST**, evoluindo gradualmente de um CRUD simples para uma aplicação full stack estruturada.

**Backend:** Python + FastAPI + PostgreSQL
**Frontend:** React + TypeScript + Vite
**ORM:** SQLAlchemy
**Autenticação:** JWT + bcrypt
**Testes:** Pytest
**Migrations:** Alembic
**Containerização:** Docker + Docker Compose
