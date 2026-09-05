# CRUD products — FastAPI + PostgreSQL

API REST desenvolvida para praticar desenvolvimento backend com Python, FastAPI e PostgreSQL.

O projeto começou como um CRUD utilizando uma lista em memória e, posteriormente, foi evoluído para utilizar um banco de dados PostgreSQL através do SQLAlchemy.

## Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Psycopg
- PostgreSQL
- Git e GitHub

## Sobre o projeto

O objetivo principal foi praticar os fundamentos de desenvolvimento de APIs REST e entender como funciona a comunicação entre uma aplicação backend e um banco de dados.

Durante o desenvolvimento, o projeto passou por algumas etapas:

1. Criação da API utilizando FastAPI.
2. Criação dos modelos de dados com Pydantic.
3. Implementação de um CRUD utilizando uma lista em memória.
4. Implementação de cadastro de múltiplos products.
5. Adição de busca de product por ID.
6. Implementação de tratamento de erros com HTTP 404.
7. Criação de um banco de dados PostgreSQL.
8. Integração do PostgreSQL com SQLAlchemy.
9. Criação do modelo `product` utilizando SQLAlchemy.
10. Criação da tabela `products` no banco de dados.
11. Implementação de sessões de banco de dados.
12. Migração do CRUD da memória para o PostgreSQL.
13. Configuração das credenciais através de variáveis de ambiente.
14. Versionamento do projeto utilizando Git e GitHub.

## Arquitetura atual

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

## Endpoints

### create products

```http
POST /products
```

Permite create um ou vários products.

Exemplo:

```json
[
  {
    "id": 1,
    "name": "Jogos Vorazes",
    "price": 39.9
  },
  {
    "id": 2,
    "name": "Em Chamas",
    "price": 42.9
  }
]
```

### list products

```http
GET /products
```

Retorna todos os products cadastrados.

### Buscar product por ID

```http
GET /products/{id}
```

Retorna um product específico.

Caso o product não exista, a API retorna:

```http
404 Not Found
```

### update preço

```http
PATCH /products/{id}
```

Atualiza o preço de um product.

Exemplo:

```json
{
  "price": 49.9
}
```

### Excluir product

```http
DELETE /products/{id}
```

Remove um product do banco de dados.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/devlavin/crud-products.git
cd crud-products
```

### 2. create e ativar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
pip install fastapi sqlalchemy psycopg python-dotenv
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql+psycopg://postgres:SUA_password@localhost:5432/fastapi_products
```

O arquivo `.env` não deve ser enviado para o GitHub.

Utilize o `.env.example` como referência.

### 5. create a tabela no banco

Com o PostgreSQL configurado e o banco `fastapi_products` criado:

```powershell
python database.py
```

### 6. Executar a API

```powershell
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação da API

O FastAPI gera automaticamente uma documentação interativa.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Também é possível acessar a documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados.

Tabela principal:

```text
products
├── id
├── name
└── price
```

O SQLAlchemy é responsável pela comunicação entre a aplicação Python e o PostgreSQL.

## Segurança

As credenciais do banco de dados são armazenadas em variáveis de ambiente através do arquivo `.env`.

O `.env` está incluído no `.gitignore` e não faz parte do repositório.

O arquivo `.env.example` é disponibilizado apenas como modelo de configuração.

## Objetivo de aprendizado

Este projeto faz parte dos estudos de desenvolvimento backend e tem como objetivo consolidar conhecimentos em:

- APIs REST
- FastAPI
- Python
- CRUD
- PostgreSQL
- SQLAlchemy
- ORM
- Pydantic
- Variáveis de ambiente
- Git e GitHub
- Estruturação de aplicações backend

## Próximos passos

Algumas melhorias planejadas para o projeto:

- [ ] Separar schemas, models e rotas
- [ ] create uma estrutura de routers
- [ ] Melhorar validações dos dados
- [ ] Adicionar migrations com Alembic
- [ ] create testes automatizados
- [ ] Melhorar tratamento de erros
- [ ] Adicionar autenticação
- [ ] create frontend para consumir a API
- [ ] Containerizar a aplicação com Docker

---

Projeto desenvolvido como parte dos estudos de desenvolvimento backend com Python.
