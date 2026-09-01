🐍 Projeto CRUD de Produtos — Processo de Desenvolvimento

## 1. Criação da API

Comecei criando uma API utilizando FastAPI.

A primeira rota criada foi:

@app.get("/exemplo")
def Exemplo_1():
return "Hello World"

O objetivo inicial foi entender como criar endpoints e fazer o FastAPI responder às requisições HTTP.

## 2. Criação do modelo de dados

Utilizei Pydantic para definir e validar os dados dos produtos:

class Item(BaseModel):
id: int
name: str
price: float

Cada produto possui:

id
name
price 

## 3. Criação do CRUD inicialmente em memória

Antes de utilizar um banco de dados, criei uma lista para armazenar os produtos:

produtos = []

Isso permitiu desenvolver e testar a lógica do CRUD sem depender inicialmente de um banco.

Foram criadas as operações:

POST → cadastrar produtos
GET → listar produtos
GET /{id} → buscar produto específico
PATCH /{id} → atualizar preço
DELETE /{id} → excluir produto 

## 4. Cadastro de vários produtos

Inicialmente o endpoint recebia apenas um produto.

Depois alterei para aceitar vários produtos de uma vez:

@app.post("/produtos")
def cadastrarProd(itens: list[Item]):

Utilizei um for para percorrer os produtos e adicioná-los à lista:

for item in itens:
produtos.append(item)

Isso permitiu enviar vários produtos em uma única requisição.

## 5. Criação do endpoint de busca por ID

Criei:

GET /produtos/{id}

A rota percorre os produtos e procura pelo ID informado.

Também implementei tratamento de erro com HTTPException:

raise HTTPException(
status_code=404,
detail="Produto não encontrado."
)

Assim, quando um produto não existe, a API retorna HTTP 404.

## 🗄️ 6. Introdução do PostgreSQL

Depois que o CRUD em memória estava funcionando, decidi substituir a lista pelo PostgreSQL.

Criei um banco chamado:

fastapi_produtos

Também configurei o ambiente virtual (.venv) e instalei:

FastAPI
SQLAlchemy
psycopg

O psycopg foi utilizado como driver para a comunicação entre Python/SQLAlchemy e PostgreSQL.

## 🔌 7. Configuração do SQLAlchemy

Criei o arquivo:

database.py

Nele configurei o engine:

engine = create_engine(DATABASE_URL)

A URL utiliza:

PostgreSQL + Psycopg
↓
localhost:5432
↓
fastapi_produtos

Também criei o SessionLocal para trabalhar com sessões do banco.

## 🏗️ 8. Criação do Model

Criei:

models.py

E defini uma Base utilizando SQLAlchemy:

class Base(DeclarativeBase):
pass

Depois criei o model Produto:

class Produto(Base):
**tablename** = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)

Esse model representa a tabela produtos no PostgreSQL.

## 🏗️ 9. Criação automática da tabela

Utilizei:

Base.metadata.create_all(bind=engine)

Com isso, o SQLAlchemy criou a tabela produtos no PostgreSQL com base no model definido em Python.

Depois confirmei a criação da tabela pelo pgAdmin.

## 🔄 10. Criação da Session

Criei a função:

def get_db():
db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

Ela permite que o FastAPI forneça uma sessão do banco para cada requisição e depois feche essa sessão.

Utilizei Depends(get_db) nas rotas:

db: Session = Depends(get_db)

## 📥 11. Migração do POST para PostgreSQL

O cadastro deixou de utilizar:

produtos.append(item)

e passou a criar objetos SQLAlchemy:

produto = Produto(
id=item.id,
name=item.name,
price=item.price
)

Depois:

db.add(produto)
db.commit()

Assim, os produtos passaram a ser realmente armazenados no PostgreSQL.

Também testei cadastrando livros da saga Jogos Vorazes 😂📚.

## 📤 12. Migração do GET

O endpoint:

GET /produtos

passou a consultar o banco utilizando:

resultado = db.execute(select(Produto))

E os resultados foram convertidos para uma lista:

produtos = resultado.scalars().all()

## 🔎 13. Migração do GET por ID

Para buscar um produto específico, utilizei:

resultado = db.execute(
select(Produto).where(Produto.id == id)
)

Depois:

produto = resultado.scalar_one_or_none()

Caso o produto não exista:

HTTPException(status_code=404)

## ✏️ 14. Migração do PATCH

Criei um schema separado para atualizar somente o preço:

class AtualizarPreco(BaseModel):
price: float

A API busca o produto pelo ID, altera:

produto.price = item.price

e confirma a alteração:

db.commit()

Assim, o PATCH altera somente o preço do produto.

## 🗑️ 15. Migração do DELETE

O DELETE segue praticamente o mesmo processo:

resultado = db.execute(
select(Produto).where(Produto.id == id)
)

produto = resultado.scalar_one_or_none()

Depois verifica se o produto existe e utiliza:

db.delete(produto)
db.commit()

O registro é então removido definitivamente do PostgreSQL.

## ✅ Resultado final

Ao final do processo, foi desenvolvido um CRUD completo de produtos, utilizando:

Python
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
Endpoints implementados
Método Endpoint Função
POST /produtos Cadastrar produtos
GET /produtos Listar produtos
GET /produtos/{id} Buscar produto por ID
PATCH /produtos/{id} Atualizar preço
DELETE /produtos/{id} Excluir produto

**Meu estudo**

- O projeto foi desenvolvido inicialmente utilizando armazenamento em memória para compreender a lógica do CRUD. Após validar o funcionamento das operações, o armazenamento foi migrado para PostgreSQL utilizando SQLAlchemy, tornando a aplicação persistente e aproximando o projeto de uma arquitetura utilizada em aplicações reais.
