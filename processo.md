# 🛒 Loja Geek API — FastAPI + PostgreSQL

API REST de uma loja virtual desenvolvida com **Python, FastAPI, SQLAlchemy e PostgreSQL**.

O projeto começou como um CRUD simples de produtos armazenados em memória e evoluiu gradualmente para uma API de e-commerce com **autenticação JWT, autorização por roles, categorias, estoque, carrinho, pedidos, pagamento simulado, área administrativa, testes automatizados, Docker e Alembic**.

O principal objetivo do projeto foi aprender, na prática, como construir uma API backend estruturada e aplicar conceitos utilizados em aplicações reais.

---

# 📌 Sobre o projeto

O projeto começou com uma API simples para praticar os fundamentos de:

* Python;
* FastAPI;
* HTTP;
* REST;
* CRUD;
* Pydantic;
* validação de dados.

Inicialmente, os produtos eram armazenados em uma lista em memória.

Depois, a aplicação foi evoluída para utilizar **PostgreSQL através do SQLAlchemy**, permitindo persistência dos dados e introduzindo conceitos como:

* banco de dados relacional;
* Foreign Keys;
* relacionamentos ORM;
* sessões;
* transações;
* autenticação;
* autorização;
* regras de negócio.

Atualmente, a aplicação representa uma API de uma **loja virtual**, com fluxo de produtos, usuários, carrinho, pedidos e administração.

---

# 🚀 Tecnologias utilizadas

* **Python**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **PostgreSQL**
* **Psycopg**
* **Alembic**
* **JWT**
* **bcrypt**
* **pytest**
* **Docker**
* **Docker Compose**
* **Git**
* **GitHub**

O FastAPI também fornece documentação interativa baseada em OpenAPI, disponível através do Swagger UI e ReDoc.

---

# 🏗️ Evolução do projeto

A evolução aconteceu aproximadamente desta forma:

```text
CRUD em memória
      ↓
FastAPI + Pydantic
      ↓
PostgreSQL
      ↓
SQLAlchemy
      ↓
Categorias
      ↓
Estoque
      ↓
Usuários
      ↓
bcrypt
      ↓
JWT
      ↓
Autenticação e autorização
      ↓
Carrinho
      ↓
Pedidos
      ↓
Pagamento simulado
      ↓
Área administrativa
      ↓
Filtros e paginação
      ↓
Testes automatizados
      ↓
Alembic
      ↓
Docker
```

---

# 1. 🚀 Criação da API

O projeto começou com uma API utilizando FastAPI.

A primeira rota criada tinha como objetivo entender o funcionamento básico de uma API:

```python
@app.get("/exemplo")
def exemplo():
    return "Hello World"
```

Essa etapa permitiu compreender:

* como criar uma API;
* como criar endpoints;
* como utilizar métodos HTTP;
* como o FastAPI processa requisições;
* como retornar respostas.

O FastAPI utiliza type hints do Python para declaração de parâmetros, validação e geração automática da documentação OpenAPI.

---

# 2. 📦 Criação dos schemas

O Pydantic foi utilizado para definir e validar os dados recebidos pela API.

Um exemplo inicial era:

```python
class Item(BaseModel):
    name: str
    price: float
```

Com a evolução do projeto, os schemas passaram a representar diferentes entidades da aplicação:

* Product;
* Category;
* User;
* Cart;
* CartItem;
* Order;
* OrderItem.

Também foram adicionadas validações específicas para preços, estoque, quantidade, email e senha.

---

# 3. 💾 CRUD inicialmente em memória

Antes da utilização do PostgreSQL, os produtos eram armazenados em uma lista:

```python
products = []
```

Isso permitiu desenvolver a lógica do CRUD sem depender inicialmente de um banco de dados.

Foram implementadas operações como:

| Método | Endpoint         | Função          |
| ------ | ---------------- | --------------- |
| POST   | `/products`      | Criar produtos  |
| GET    | `/products`      | Listar produtos |
| GET    | `/products/{id}` | Buscar produto  |
| PATCH  | `/products/{id}` | Atualizar preço |
| DELETE | `/products/{id}` | Excluir produto |

Essa etapa foi importante para compreender primeiro a lógica da aplicação antes de adicionar persistência.

---

# 4. 📚 Cadastro de vários produtos

O endpoint de criação foi posteriormente alterado para permitir o cadastro de vários produtos em uma única requisição.

Exemplo:

```python
@app.post("/products")
def create_products(items: list[Item]):
    ...
```

A aplicação percorre os itens recebidos e realiza os respectivos cadastros.

---

# 5. 🔎 Busca de produto por ID

Foi criado o endpoint:

```text
GET /products/{id}
```

A rota procura o produto pelo ID informado.

Quando o produto não existe, a API retorna:

```text
HTTP 404
```

com uma resposta indicando que o produto não foi encontrado.

---

# 6. 🗄️ Introdução do PostgreSQL

Depois que o CRUD em memória estava funcionando, a aplicação foi migrada para PostgreSQL.

O banco passou a armazenar permanentemente os dados da aplicação.

O projeto utiliza:

```text
Python
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL
```

As informações de conexão são armazenadas através de variáveis de ambiente.

Exemplo:

```env
DATABASE_URL=...
JWT_SECRET_KEY=...
```

O arquivo `.env` não deve ser versionado.

---

# 7. 🔌 Configuração do SQLAlchemy

Foi criado o arquivo:

```text
database.py
```

Nele é configurado o engine:

```python
engine = create_engine(DATABASE_URL)
```

Também foi criada uma fábrica de sessões:

```python
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
```

A conexão com o banco passou a ser disponibilizada através de uma dependência do FastAPI.

---

# 8. 🏗️ Criação dos Models

Foi criado o arquivo:

```text
models.py
```

A Base do SQLAlchemy utiliza:

```python
class Base(DeclarativeBase):
    pass
```

Os principais models atuais são:

```text
Product
Category
User
Cart
CartItem
Order
OrderItem
```

---

# 9. 🗃️ Estrutura atual do banco

O PostgreSQL atualmente possui as seguintes entidades:

```text
categories
users
products
carts
cart_items
orders
order_items
```

Os relacionamentos principais são:

```text
Category
   │
   └── Products


User
   │
   ├── Cart
   │     └── CartItems
   │             └── Products
   │
   └── Orders
          └── OrderItems
                  └── Products
```

---

# 10. 🔄 Session do banco

Foi criada a dependência:

```python
def get_db():
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Nas rotas:

```python
db: Session = Depends(get_db)
```

O `Depends()` permite que o FastAPI injete automaticamente a sessão necessária para cada requisição.

---

# 11. 📥 Persistência dos produtos

O cadastro deixou de utilizar:

```python
products.append(item)
```

e passou a criar objetos SQLAlchemy:

```python
product = Product(
    name=item.name,
    price=item.price,
    stock=item.stock,
    category_id=item.category_id
)
```

Depois:

```python
db.add(product)
db.commit()
```

Os produtos passaram então a ser persistidos no PostgreSQL.

---

# 12. 📤 Consulta de produtos

O endpoint:

```text
GET /products
```

passou a consultar diretamente o banco utilizando SQLAlchemy:

```python
result = db.execute(
    select(Product)
)
```

Os objetos são obtidos através de:

```python
products = result.scalars().all()
```

---

# 13. 🔎 Consulta de produto por ID

A busca individual utiliza:

```python
result = db.execute(
    select(Product).where(Product.id == id)
)
```

Depois:

```python
product = result.scalar_one_or_none()
```

Caso o produto não exista:

```python
raise HTTPException(
    status_code=404,
    detail="Product not found."
)
```

---

# 14. ✏️ Atualização de preço

Foi criado um schema específico:

```python
class UpdatePrice(BaseModel):
    price: Decimal = Field(gt=0)
```

Isso garante que o preço seja maior que zero.

A atualização modifica somente o campo de preço:

```python
product.price = item.price
```

Depois:

```python
db.commit()
```

---

# 15. 🗑️ Exclusão de produtos

O produto é localizado através do SQLAlchemy:

```python
result = db.execute(
    select(Product).where(Product.id == id)
)
```

Depois:

```python
product = result.scalar_one_or_none()
```

Quando autorizado:

```python
db.delete(product)
db.commit()
```

A exclusão é protegida por autorização administrativa.

---

# 16. 🏷️ Categorias

O projeto passou a trabalhar com categorias de produtos.

Foi criado o model:

```text
Category
```

Um relacionamento de um-para-muitos foi estabelecido:

```text
Category
   │
   ├── Product
   ├── Product
   └── Product
```

No produto:

```python
category_id = mapped_column(
    ForeignKey("categories.id")
)
```

E no relacionamento ORM:

```python
category = relationship(
    back_populates="products"
)
```

A categoria possui:

```python
products = relationship(
    back_populates="category"
)
```

---

# 17. 📦 Controle de estoque

Os produtos possuem:

```python
stock: Mapped[int]
```

O estoque não pode ser negativo.

O schema utilizado para atualização é:

```python
class UpdateStock(BaseModel):
    stock: int = Field(ge=0)
```

Também foram implementadas verificações de estoque durante operações do carrinho e criação de pedidos.

---

# 18. 👤 Cadastro de usuários

Foi criado o model:

```text
User
```

com os principais campos:

```text
id
name
email
password_hash
role
```

O email possui restrição de unicidade:

```python
unique=True
```

Isso impede que dois usuários utilizem o mesmo email.

---

# 19. 🔐 Validação e hash de senha

A senha não é armazenada diretamente no banco.

Durante o cadastro, o Pydantic valida a senha.

Regras:

* mínimo de 8 caracteres;
* pelo menos uma letra maiúscula;
* pelo menos um número;
* pelo menos um caractere especial.

Exemplo:

```text
Lavinha123!
```

Fluxo:

```text
Senha
  ↓
Validação
  ↓
bcrypt
  ↓
password_hash
  ↓
PostgreSQL
```

Durante o login, a senha fornecida é comparada com o hash através de:

```python
bcrypt.checkpw()
```

A senha em texto puro nunca é armazenada no banco.

---

# 20. 📧 Validação de email

O cadastro utiliza:

```python
email: EmailStr
```

O Pydantic valida o formato do email antes que a aplicação continue o processamento.

Além disso, o banco garante a unicidade do endereço.

---

# 21. 🔑 Login e JWT

Foi implementado login utilizando JWT.

Endpoint:

```text
POST /users/login
```

Depois de validar as credenciais, a API gera um token.

O token contém informações como:

```text
sub → ID do usuário
exp → data de expiração
```

O token possui tempo de expiração configurado através das configurações da aplicação.

---

# 22. 🪪 Autenticação com Bearer Token

A autenticação utiliza Bearer Token.

O cliente envia:

```text
Authorization: Bearer TOKEN
```

A dependência:

```python
get_current_user()
```

é responsável por:

1. receber o token;
2. validar o JWT;
3. verificar sua expiração;
4. obter o ID do usuário;
5. consultar o usuário no banco;
6. retornar o usuário autenticado.

Também existe:

```python
get_current_admin()
```

para operações que exigem privilégios administrativos.

---

# 23. 👥 Roles e autorização

A aplicação possui dois tipos principais de usuário:

```text
user
admin
```

O tipo é definido pelo campo:

```text
role
```

### Usuário comum

Pode:

* consultar produtos;
* consultar categorias;
* utilizar o carrinho;
* realizar compras;
* consultar seus próprios pedidos.

### Administrador

Além das permissões de usuário comum, pode:

* criar produtos;
* atualizar produtos;
* excluir produtos;
* alterar estoque;
* criar categorias;
* atualizar categorias;
* excluir categorias;
* gerenciar pedidos;
* consultar usuários;
* alterar roles de usuários.

A autorização utiliza:

```python
Depends(get_current_admin)
```

Enquanto endpoints que exigem apenas autenticação utilizam:

```python
Depends(get_current_user)
```

A API diferencia:

```text
401 → não autenticado ou token inválido

403 → autenticado, mas sem permissão
```

---

# 24. 🛒 Carrinho

Foram criados os models:

```text
Cart
CartItem
```

Estrutura:

```text
Cart
├── id
└── user_id

CartItem
├── id
├── cart_id
├── product_id
├── quantity
└── added_price
```

Cada usuário possui um único carrinho:

```python
user_id = mapped_column(
    ForeignKey("users.id"),
    unique=True
)
```

---

# 25. 🛍️ Operações do carrinho

Principais endpoints:

| Método | Endpoint             | Função             |
| ------ | -------------------- | ------------------ |
| GET    | `/cart`              | Consultar carrinho |
| POST   | `/cart`              | Adicionar produto  |
| PATCH  | `/cart/{product_id}` | Alterar quantidade |
| DELETE | `/cart/{product_id}` | Remover produto    |

Todos os endpoints do carrinho exigem autenticação.

---

# 26. ➕ Regra para adicionar produtos

Ao adicionar um produto, a API verifica:

1. se o usuário está autenticado;
2. se o carrinho existe;
3. se o produto existe;
4. se existe estoque suficiente;
5. se o produto já está no carrinho.

Um mesmo produto **não pode aparecer duplicado no carrinho**.

Quando o produto já existe, sua quantidade deve ser atualizada através da operação específica de quantidade.

---

# 27. 🔢 Controle de quantidade

O endpoint:

```text
PATCH /cart/{product_id}
```

permite alterar a quantidade.

A quantidade deve ser maior que zero.

Além disso, o estoque é verificado novamente.

Isso impede que o usuário mantenha no carrinho uma quantidade superior ao estoque disponível.

---

# 28. 🗑️ Remoção do carrinho

O endpoint:

```text
DELETE /cart/{product_id}
```

remove o item pertencente ao carrinho do usuário autenticado.

Um usuário não consegue remover itens do carrinho de outro usuário.

---

# 29. 💰 Valores monetários com Decimal

Para evitar problemas de precisão relacionados ao uso de `float`, os valores monetários passaram a utilizar:

```python
Decimal
```

Na camada do banco:

```python
Numeric(10, 2)
```

Os principais campos monetários são:

```text
Product.price
CartItem.added_price
Order.total
OrderItem.price
```

Fluxo:

```text
API
 ↓
Decimal
 ↓
SQLAlchemy Numeric(10,2)
 ↓
PostgreSQL NUMERIC(10,2)
```

---

# 30. 💵 Preço, subtotal e total

Os itens do carrinho possuem informações como:

```text
product_id
name
price
added_price
quantity
subtotal
price_changed
```

O subtotal é calculado com base no preço atual do produto:

```python
subtotal = item.product.price * item.quantity
```

O total é calculado a partir dos subtotais.

O campo:

```text
added_price
```

mantém o preço registrado no momento em que o produto foi adicionado ao carrinho.

Isso permite detectar alterações posteriores de preço.

---

# 31. 📦 Criação de pedidos

Foram criados os models:

```text
Order
OrderItem
```

### Order

```text
id
user_id
status
total
```

### OrderItem

```text
id
order_id
product_id
quantity
price
```

O pedido é criado a partir do carrinho.

Durante a criação:

1. o carrinho do usuário é localizado;
2. verifica-se se existem itens;
3. o estoque atual é verificado novamente;
4. o preço atual dos produtos é utilizado;
5. o pedido é criado;
6. os itens do pedido são registrados;
7. o estoque é reduzido;
8. os itens do carrinho são removidos;
9. a transação é confirmada.

O preço armazenado em `OrderItem.price` representa o preço no momento da compra.

Dessa forma, alterações futuras no preço do produto não alteram o histórico do pedido.

---

# 32. 🧾 Consulta de pedidos

O usuário pode consultar seus próprios pedidos.

Endpoints:

```text
GET /orders
GET /orders/{order_id}
```

A API garante que o usuário só consiga acessar pedidos pertencentes a ele.

A resposta contém:

```text
id
status
items
total
```

Cada item apresenta:

```text
product_id
name
quantity
price
subtotal
```

---

# 33. 💳 Pagamento simulado

O projeto não utiliza um gateway de pagamento real.

Foi implementado um fluxo de pagamento simulado:

```text
POST /orders/{order_id}/pay
```

Um pedido só pode ser pago quando estiver:

```text
PENDENTE
```

Após o pagamento:

```text
PENDENTE
   ↓
PAGO
```

Nenhuma transação financeira real é realizada.

---

# 34. 🔄 Status dos pedidos

O fluxo de status implementado é:

```text
PENDENTE
   ↓
PAGO
   ↓
ENVIADO
   ↓
ENTREGUE
```

Também existe cancelamento:

```text
PENDENTE → CANCELADO

PAGO → CANCELADO
```

As transições válidas são:

```text
PENDENTE → PAGO
PENDENTE → CANCELADO

PAGO → ENVIADO
PAGO → CANCELADO

ENVIADO → ENTREGUE
```

Pedidos `ENTREGUE` ou `CANCELADO` não podem avançar para outro status.

Quando um pedido é cancelado, os produtos são devolvidos ao estoque.

---

# 35. 🔎 Busca, filtros e paginação

O endpoint:

```text
GET /products
```

possui filtros e paginação.

Parâmetros disponíveis:

```text
name
category
min_price
max_price
skip
limit
```

Exemplos:

```text
/products?name=harry
```

```text
/products?category=livros
```

```text
/products?min_price=30&max_price=100
```

Os filtros podem ser combinados:

```text
/products?name=harry&category=livros&min_price=30
```

A categoria pode ser pesquisada pelo nome, enquanto internamente o relacionamento utiliza:

```text
products.category_id
        ↓
categories.id
```

Também foi implementada paginação utilizando:

```text
skip
limit
```

com limite máximo de 100 registros por requisição.

---

# 36. 🔐 Área administrativa

Foi criada uma área administrativa protegida por:

```python
Depends(get_current_admin)
```

O router utiliza:

```text
/admin
```

## Administração de pedidos

Endpoints:

```text
GET   /admin/orders
GET   /admin/orders/{order_id}
PATCH /admin/orders/{order_id}/status
```

O administrador pode consultar todos os pedidos e alterar seus status respeitando as regras de transição.

## Administração de usuários

Endpoints:

```text
GET   /admin/users
GET   /admin/users/{user_id}
PATCH /admin/users/{user_id}/role
```

O administrador pode consultar usuários e alterar suas roles entre:

```text
user
admin
```

Existe também uma proteção para impedir que o administrador remova a própria permissão administrativa.

---

# 37. 🔍 Conceitos de SQLAlchemy

Durante o desenvolvimento foram utilizados conceitos importantes do SQLAlchemy.

### `db.add()`

Adiciona um objeto à sessão atual.

### `db.commit()`

Confirma a transação no banco.

### `db.rollback()`

Desfaz alterações ainda não confirmadas.

### `db.flush()`

Envia alterações para o banco sem finalizar a transação.

É útil quando precisamos do ID gerado pelo banco antes do `commit`.

### `db.refresh()`

Atualiza o objeto Python com os dados atuais do banco.

Resumo:

```text
flush    → envia
commit   → confirma
rollback → desfaz
refresh  → atualiza
```

---

# 38. 🗃️ Alembic

O projeto atualmente utiliza **Alembic** para controlar a evolução do schema do banco de dados.

A migration inicial foi gerada automaticamente a partir dos models:

```text
6fdb58e707fc_initial_migration.py
```

Ela cria as principais tabelas da aplicação:

```text
categories
users
products
carts
cart_items
orders
order_items
```

A migration é aplicada através de:

```powershell
docker compose exec api python -m alembic upgrade head
```

Isso permite reproduzir a estrutura do banco de maneira organizada e evita depender de alterações manuais no PostgreSQL.

Fluxo utilizado:

```text
Models
   ↓
Alembic autogenerate
   ↓
Migration
   ↓
alembic upgrade head
   ↓
PostgreSQL
```

---

# 39. 🐳 Docker

O projeto atualmente possui um ambiente Dockerizado utilizando Docker Compose.

A estrutura principal é:

```text
Docker Compose
│
├── API
│   └── FastAPI
│
└── PostgreSQL
```

Serviços:

```text
postgres
api
```

O PostgreSQL utiliza persistência através de volume Docker.

A API se conecta ao banco utilizando o hostname do serviço:

```text
postgres
```

Em vez de:

```text
localhost
```

quando a conexão acontece dentro do container.

---

# 40. 🐘 PostgreSQL no Docker

O banco utiliza:

```text
PostgreSQL 17
```

O serviço é executado através do container:

```text
postgres-dev
```

A API é executada através do container:

```text
loja-geek-api
```

A comunicação ocorre:

```text
loja-geek-api
       │
       ▼
postgres-dev
       │
       ▼
PostgreSQL
```

O banco possui um volume persistente para evitar perda dos dados quando os containers são reiniciados.

---

# 41. 🧪 Testes automatizados

Foi criada uma suíte de testes utilizando:

```text
pytest
```

Os testes utilizam um banco PostgreSQL separado do banco utilizado pela aplicação.

Foram testados fluxos envolvendo:

* cadastro de usuários;
* validação de email;
* validação de senha;
* login;
* JWT;
* autenticação;
* autorização;
* produtos;
* categorias;
* filtros;
* paginação;
* estoque;
* carrinho;
* quantidade;
* pedidos;
* pagamento;
* cancelamento;
* área administrativa;
* regras de status.

### Resultado atual

```text
66 passed
```

Todos os **66 testes automatizados estão passando**.

---

# 42. 📁 Organização atual do projeto

A estrutura atual está organizada aproximadamente da seguinte maneira:

```text
loja-geek/
│
├── .venv/
├── .env
├── .env.example
├── .gitignore
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
│
├── alembic.ini
├── alembic/
│   └── versions/
│       └── 6fdb58e707fc_initial_migration.py
│
├── main.py
├── database.py
├── models.py
├── schema.py
├── auth.py
│
├── routers/
│   ├── products.py
│   ├── categories.py
│   ├── users.py
│   ├── cart.py
│   ├── orders.py
│   └── admin.py
│
└── tests/
    ├── conftest.py
    └── ...
```

---

# 43. 🌐 Arquitetura atual

A aplicação atualmente segue aproximadamente:

```text
                         CLIENTE
                            │
                            ▼
                         FastAPI
                            │
              ┌─────────────┼─────────────┐
              │             │             │
           Routers         Auth         Schemas
              │             │             │
              │        JWT / bcrypt       │
              │                           │
              └─────────────┬─────────────┘
                            │
                        SQLAlchemy
                            │
                         Psycopg
                            │
                            ▼
                       PostgreSQL
                            │
                     Docker Container
```

As migrations são controladas pelo Alembic:

```text
Models
   ↓
Alembic
   ↓
Migrations
   ↓
PostgreSQL
```

---

# 44. 🔐 Segurança implementada

Até o momento foram implementados:

* hash de senha com bcrypt;
* validação de senha;
* validação de email;
* JWT;
* expiração de token;
* autenticação com Bearer Token;
* diferenciação entre usuário e administrador;
* proteção de endpoints administrativos;
* email único;
* `response_model`;
* variáveis sensíveis armazenadas em `.env`;
* `.env` protegido pelo `.gitignore`;
* diferenciação entre HTTP 401 e HTTP 403;
* proteção contra cadastro público com role administrativa.

A role do usuário não é definida pelo cadastro público.

Dessa forma, um usuário não pode simplesmente enviar:

```json
{
    "role": "admin"
}
```

para tentar criar uma conta administrativa.

---

# 45. 🧠 Regras de negócio principais

O projeto possui diversas regras de negócio além do CRUD básico.

### Produtos

* preço deve ser maior que zero;
* estoque não pode ser negativo;
* categoria deve existir;
* exclusão é protegida por autorização.

### Usuários

* email deve possuir formato válido;
* email deve ser único;
* senha possui regras de complexidade;
* senha é armazenada somente como hash;
* roles são controladas.

### Carrinho

* usuário precisa estar autenticado;
* produto precisa existir;
* estoque precisa ser suficiente;
* produto não pode aparecer duplicado;
* quantidade deve ser maior que zero.

### Pedidos

* pedido precisa possuir itens;
* estoque é verificado novamente na criação;
* estoque é reduzido durante a compra;
* preço da compra é armazenado no `OrderItem`;
* apenas o dono pode consultar seus pedidos;
* status segue transições definidas;
* cancelamento pode devolver produtos ao estoque.

---

# 46. 📋 Próximas etapas

O núcleo funcional do backend já está implementado.

As próximas etapas serão voltadas principalmente para **qualidade, refinamento e preparação para produção**.

## 🧹 1. Refatoração final

Realizar uma revisão geral do projeto:

* organização dos routers;
* schemas;
* nomes de variáveis;
* funções;
* responses;
* tratamento de erros;
* regras duplicadas;
* consultas SQLAlchemy;
* organização dos arquivos;
* comentários;
* documentação;
* padronização do código.

A nomenclatura principal do projeto já foi padronizada para inglês.

---

## 🧪 2. Revisão dos testes

Apesar dos 66 testes estarem passando, ainda será possível melhorar a suíte com:

* cobertura de casos extremos;
* cenários de erro adicionais;
* testes de integração;
* melhoria das fixtures;
* análise de cobertura.

---

## 🚀 3. Preparação para produção

Depois da revisão do backend:

* revisar variáveis de ambiente;
* revisar segurança;
* configurar banco de produção;
* executar migrations;
* configurar logs;
* configurar servidor;
* revisar Docker;
* preparar deploy.

---

## 🎨 4. Frontend

Depois da conclusão do backend, será desenvolvido o frontend da loja.

O frontend deverá incluir:

* catálogo;
* busca;
* filtros;
* categorias;
* login;
* cadastro;
* carrinho;
* checkout;
* pedidos;
* área do usuário;
* área administrativa.

---

# 47. 📊 Estado atual do projeto

O projeto evoluiu de:

```text
CRUD simples em memória
```

para:

```text
                         FASTAPI
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
       Products          Categories        Users
          │                 │                 │
       Stock                │            JWT + bcrypt
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                          Cart
                            │
                            ▼
                          Order
                            │
                            ▼
                    Pagamento simulado
                            │
                            ▼
                       Área Admin
                            │
                            ▼
                       PostgreSQL
                            │
                            ▼
                         Docker
```

### Funcionalidades implementadas

* [x] CRUD de produtos
* [x] Categorias
* [x] Relacionamento entre categorias e produtos
* [x] Controle de estoque
* [x] Usuários
* [x] Validação de email
* [x] Validação de senha
* [x] bcrypt
* [x] JWT
* [x] Autenticação
* [x] Autorização
* [x] Roles
* [x] Carrinho
* [x] Controle de quantidade
* [x] Controle de estoque no carrinho
* [x] Pedidos
* [x] Histórico de pedidos
* [x] Pagamento simulado
* [x] Cancelamento
* [x] Fluxo de status
* [x] Área administrativa
* [x] Gerenciamento de usuários
* [x] Busca
* [x] Filtros
* [x] Paginação
* [x] Decimal/Numeric para valores monetários
* [x] Testes automatizados
* [x] Alembic
* [x] Docker
* [x] Docker Compose
* [x] PostgreSQL em container

---

# 48. 📚 O que este projeto ensinou

O desenvolvimento permitiu sair de um CRUD básico e estudar conceitos presentes em aplicações reais.

### Python e API

* Python;
* FastAPI;
* Pydantic;
* HTTP;
* REST;
* CRUD;
* OpenAPI;
* Swagger;
* ReDoc.

### Banco de dados

* PostgreSQL;
* SQLAlchemy;
* Psycopg;
* Foreign Keys;
* relacionamentos ORM;
* Sessions;
* Transactions;
* `commit`;
* `rollback`;
* `flush`;
* `refresh`;
* migrations;
* Alembic.

### Segurança

* validação de dados;
* validação de email;
* validação de senha;
* hash de senha;
* bcrypt;
* JWT;
* autenticação;
* autorização;
* roles;
* Bearer Token.

### Regras de negócio

* controle de estoque;
* carrinho de compras;
* controle de quantidade;
* pedidos;
* histórico de pedidos;
* pagamento simulado;
* cancelamento;
* fluxo de status;
* filtros;
* paginação;
* valores monetários com Decimal.

### Infraestrutura

* variáveis de ambiente;
* Docker;
* Docker Compose;
* containers;
* volumes;
* PostgreSQL em container;
* migrations em ambiente Docker.

### Qualidade

* pytest;
* testes de integração;
* fixtures;
* validação de regras de negócio;
* organização de projeto.

---

# 49. 🎯 Conclusão

O projeto começou como uma forma de aprender os fundamentos de CRUD com Python e FastAPI.

Ao longo do desenvolvimento, ele foi evoluindo gradualmente para uma aplicação muito mais próxima de um backend real:

```text
CRUD
 ↓
API REST
 ↓
Banco de dados
 ↓
ORM
 ↓
Relacionamentos
 ↓
Autenticação
 ↓
Autorização
 ↓
Regras de negócio
 ↓
Carrinho
 ↓
Pedidos
 ↓
Administração
 ↓
Testes
 ↓
Migrations
 ↓
Docker
```

O objetivo não foi apenas implementar funcionalidades, mas entender **por que cada camada existe, como elas se relacionam e quais problemas cada tecnologia resolve**.

O resultado é uma API de e-commerce funcional, testada e containerizada, construída progressivamente como projeto de estudo e prática de desenvolvimento backend.

---

# 📌 Próximo passo

Com o backend funcional, testado, versionado através do Alembic e executando em Docker, o próximo ciclo do projeto será:

```text
🧹 Refatoração final
        ↓
🔐 Revisão de segurança
        ↓
🚀 Preparação para produção / Deploy
        ↓
🎨 Desenvolvimento do Frontend
```

A documentação interativa da API pode ser acessada durante o desenvolvimento em:

```text
http://localhost:8000/docs
```

E a documentação alternativa:

```text
http://localhost:8000/redoc
```

O FastAPI disponibiliza essas interfaces automaticamente a partir do schema OpenAPI da aplicação.
