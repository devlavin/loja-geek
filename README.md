# CRUD Produtos — FastAPI + PostgreSQL

API REST desenvolvida para praticar desenvolvimento backend com Python, FastAPI e PostgreSQL.

O projeto começou como um CRUD utilizando uma lista em memória e, posteriormente, foi evoluído para utilizar um banco de dados PostgreSQL através do SQLAlchemy.

## Tecnologias

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Psycopg
* PostgreSQL
* Git e GitHub

## Sobre o projeto

O objetivo principal foi praticar os fundamentos de desenvolvimento de APIs REST e entender como funciona a comunicação entre uma aplicação backend e um banco de dados.

Durante o desenvolvimento, o projeto passou por algumas etapas:

1. Criação da API utilizando FastAPI.
2. Criação dos modelos de dados com Pydantic.
3. Implementação de um CRUD utilizando uma lista em memória.
4. Implementação de cadastro de múltiplos produtos.
5. Adição de busca de produto por ID.
6. Implementação de tratamento de erros com HTTP 404.
7. Criação de um banco de dados PostgreSQL.
8. Integração do PostgreSQL com SQLAlchemy.
9. Criação do modelo `Produto` utilizando SQLAlchemy.
10. Criação da tabela `produtos` no banco de dados.
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

### Cadastrar produtos

```http
POST /produtos
```

Permite cadastrar um ou vários produtos.

Exemplo:

```json
[
  {
    "id": 1,
    "name": "Jogos Vorazes",
    "price": 39.90
  },
  {
    "id": 2,
    "name": "Em Chamas",
    "price": 42.90
  }
]
```

### Listar produtos

```http
GET /produtos
```

Retorna todos os produtos cadastrados.

### Buscar produto por ID

```http
GET /produtos/{id}
```

Retorna um produto específico.

Caso o produto não exista, a API retorna:

```http
404 Not Found
```

### Atualizar preço

```http
PATCH /produtos/{id}
```

Atualiza o preço de um produto.

Exemplo:

```json
{
  "price": 49.90
}
```

### Excluir produto

```http
DELETE /produtos/{id}
```

Remove um produto do banco de dados.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/devlavin/crud-produtos.git
cd crud-produtos
```

### 2. Criar e ativar o ambiente virtual

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
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/fastapi_produtos
```

O arquivo `.env` não deve ser enviado para o GitHub.

Utilize o `.env.example` como referência.

### 5. Criar a tabela no banco

Com o PostgreSQL configurado e o banco `fastapi_produtos` criado:

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
produtos
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

* APIs REST
* FastAPI
* Python
* CRUD
* PostgreSQL
* SQLAlchemy
* ORM
* Pydantic
* Variáveis de ambiente
* Git e GitHub
* Estruturação de aplicações backend

## Próximos passos

Algumas melhorias planejadas para o projeto:

* [ ] Separar schemas, models e rotas
* [ ] Criar uma estrutura de routers
* [ ] Melhorar validações dos dados
* [ ] Adicionar migrations com Alembic
* [ ] Criar testes automatizados
* [ ] Melhorar tratamento de erros
* [ ] Adicionar autenticação
* [ ] Criar frontend para consumir a API
* [ ] Containerizar a aplicação com Docker

---

Projeto desenvolvido como parte dos estudos de desenvolvimento backend com Python.
