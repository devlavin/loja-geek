# 🛒 Geek World — E-commerce Full Stack

E-commerce fictício voltado para produtos geek, desenvolvido como projeto de estudo full stack, com **backend em Python/FastAPI** e **frontend em React/Vite**, ambos em produção.

O projeto começou como um CRUD simples de produtos com dados em memória e evoluiu para uma aplicação completa: banco de dados relacional, autenticação JWT, autorização por roles, categorias, carrinho de compras, pedidos, controle de estoque, pagamento simulado, área administrativa, testes automatizados, migrations com Alembic, containerização com Docker — e agora também com uma interface de usuário completa consumindo essa API.

**🔗 Projeto em produção:** [loja-geek-phi.vercel.app](https://loja-geek-phi.vercel.app/)
**🔗 API em produção:** [loja-geek.onrender.com](https://loja-geek.onrender.com/)

---

## 🚀 Tecnologias

**Backend**
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Psycopg
- PostgreSQL
- JWT + bcrypt
- Alembic (migrations)
- Pytest (66 testes passando)

**Frontend**
- React
- Vite

**Infraestrutura**
- Docker + Docker Compose
- Deploy: Render (API) + Vercel (frontend)
- Git e GitHub

---

## 📦 Sobre o projeto

O **Geek World** simula uma loja virtual completa de produtos geek, cobrindo tanto a experiência do cliente quanto a área administrativa.

A aplicação permite que usuários:

- Criem uma conta e façam login
- Consultem e atualizem seus dados
- Visualizem, pesquisem e filtrem produtos por categoria e preço
- Adicionem, atualizem e removam produtos do carrinho
- Criem pedidos a partir do carrinho
- Realizem um pagamento simulado
- Consultem e cancelem pedidos (quando permitido)

Administradores possuem permissões adicionais para gerenciar produtos, categorias, usuários e pedidos.

---

## 🏗️ Arquitetura

```
Cliente (React + Vite)
   ↓
FastAPI
   ↓
Pydantic (validação)
   ↓
SQLAlchemy (ORM)
   ↓
Psycopg
   ↓
PostgreSQL
```

### Fluxo de autenticação

```
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
Autenticação → Autorização / Role
```

Frontend e backend são hospedados separadamente (Vercel e Render), integrados via variável de ambiente apontando para a URL da API, com CORS configurado entre os dois serviços.

---

## 🗄️ Banco de dados

PostgreSQL como banco relacional, com SQLAlchemy como ORM.

Principais entidades:

```
User → Cart → CartItem → Product → Category
User → Order → OrderItem → Product
```

Valores monetários usam `Decimal` na aplicação e `NUMERIC(10,2)` no PostgreSQL, evitando problemas de precisão de `float`.

---

## 🔐 Autenticação e autorização

Autenticação via **JWT**. Dois níveis de acesso: `user` e `admin`. Administradores têm permissões adicionais de gerenciamento da loja, com regras que impedem ações administrativas indevidas (como alterar a própria role).

---

## 🧪 Testes

```
pytest
```

66 testes cobrindo produtos, categorias, usuários, autenticação, autorização, carrinho, pedidos, pagamentos, cancelamentos, controle de estoque, área administrativa e regras de negócio.

---

## 🐳 Docker

```
docker compose up -d --build
docker compose exec api python -m alembic upgrade head
```

Dois serviços principais: a API FastAPI e o PostgreSQL, com volume Docker para persistência dos dados.

---

## ⚙️ Como executar o backend localmente

```bash
git clone https://github.com/devlavin/loja-geek.git
cd loja-geek
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

API disponível em `http://127.0.0.1:8000` — documentação automática em `/docs` (Swagger) e `/redoc`.

---

## 🚧 Status do projeto

O projeto evoluiu de um CRUD simples para uma aplicação full stack completa, com frontend próprio consumindo a API em produção.

**Concluído**
- [x] Backend completo (CRUD, autenticação, autorização, carrinho, pedidos, pagamento simulado, área administrativa)
- [x] Frontend em React/Vite integrado à API
- [x] Testes automatizados (66 passando)
- [x] Migrations com Alembic
- [x] Docker e Docker Compose
- [x] Deploy em produção (API no Render, frontend na Vercel)

**Próximos passos**
- [ ] Refatoração e melhorias de tratamento de erros
- [ ] Revisão de segurança
- [ ] Ajustes finais de integração frontend/backend

---

## 🎯 Objetivo

Projeto desenvolvido para consolidar conhecimentos em desenvolvimento full stack: API REST em Python/FastAPI, ORM e banco relacional, autenticação e autorização, testes automatizados, containerização e integração entre frontend e backend hospedados separadamente — construção de portfólio real.
