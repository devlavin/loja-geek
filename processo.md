# 🐍 Projeto CRUD de products — FastAPI + PostgreSQL

## 📌 Sobre o projeto

Este projeto começou como um CRUD simples de products desenvolvido em Python com FastAPI, inicialmente utilizando armazenamento em memória.

O objetivo foi compreender, de forma progressiva, como construir uma API REST, validar dados, trabalhar com banco de dados, autenticação, autorização e regras de negócio.

Após validar a lógica do CRUD em memória, o projeto foi evoluído para utilizar PostgreSQL com SQLAlchemy, tornando os dados persistentes e aproximando a aplicação de uma arquitetura utilizada em aplicações reais.

Atualmente, o projeto evoluiu de um simples CRUD de products para uma **API de uma loja virtual**, com usuários, autenticação, categorys, stock, cart, orders, pagamento simulado e área administrativa.

---

# 1. 🚀 Criação da API

Comecei criando uma API utilizando FastAPI.

A primeira rota criada foi:

```python
@app.get("/exemplo")
def Exemplo_1():
    return "Hello World"
```

O objetivo inicial foi entender:

- como create uma API;
- como create endpoints;
- como utilizar métodos HTTP;
- como o FastAPI processa requisições;
- como retornar responses.

---

# 2. 📦 Criação do modelo de dados

Utilizei Pydantic para definir e validar os dados dos products:

```python
class Item(BaseModel):
    id: int
    name: str
    price: float
```

Cada product possuía inicialmente:

- `id`
- `name`
- `price`

O Pydantic ficou responsável pela validação dos dados recebidos pela API.

---

# 3. 💾 Criação do CRUD inicialmente em memória

Antes de utilizar um banco de dados, criei uma lista para armazenar os products:

```python
products = []
```

Isso permitiu desenvolver e testar a lógica do CRUD sem depender inicialmente de um banco.

Foram criadas as operações:

| Método | Endpoint         | Função          |
| ------ | ---------------- | --------------- |
| POST   | `/products`      | create products |
| GET    | `/products`      | list products   |
| GET    | `/products/{id}` | Buscar product  |
| PATCH  | `/products/{id}` | update preço    |
| DELETE | `/products/{id}` | Excluir product |

Essa etapa foi importante para entender primeiro a lógica da aplicação antes de introduzir persistência.

---

# 4. 📚 Cadastro de vários products

Inicialmente o endpoint recebia apenas um product.

Depois alterei para aceitar vários products de uma vez:

```python
@app.post("/products")
def createProd(items: list[Item]):
```

Utilizei um `for` para percorrer os products:

```python
for item in items:
    products.append(item)
```

Isso permitiu enviar vários products em uma única requisição.

---

# 5. 🔎 Busca de product por ID

Foi criado o endpoint:

```text
GET /products/{id}
```

A rota procura o product pelo ID informado.

Também implementei tratamento de erro:

```python
raise HTTPException(
    status_code=404,
    detail="product não encontrado."
)
```

Assim, quando um product não existe, a API retorna HTTP 404.

---

# 6. 🗄️ Introdução do PostgreSQL

Depois que o CRUD em memória estava funcionando, decidi substituir a lista pelo PostgreSQL.

Foi criado o banco:

```text
fastapi_products
```

Também foi configurado um ambiente virtual:

```text
.venv
```

E instaladas as principais dependências:

- FastAPI
- SQLAlchemy
- Psycopg
- python-dotenv
- bcrypt
- PyJWT

O `psycopg` foi utilizado como driver para comunicação entre Python/SQLAlchemy e PostgreSQL.

---

# 7. 🔌 Configuração do SQLAlchemy

Foi criado o arquivo:

```text
database.py
```

Nele foi configurado o engine:

```python
engine = create_engine(DATABASE_URL)
```

A conexão utiliza:

```text
Python
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL
   ↓
fastapi_products
```

Também foi criada uma `SessionLocal` para trabalhar com sessões do banco.

As informações sensíveis de conexão foram colocadas em variáveis de ambiente através do `.env`.

---

# 8. 🏗️ Criação dos Models

Foi criado o arquivo:

```text
models.py
```

A Base do SQLAlchemy foi definida utilizando:

```python
class Base(DeclarativeBase):
    pass
```

Inicialmente foi criado o model `product`.

Com a evolução do projeto, novos models foram adicionados:

- `product`
- `category`
- `user`
- `cart`
- `Itemcart`
- `order`
- `orderItem`

---

# 9. 🏗️ Criação automática das tabelas

Foi utilizado:

```python
Base.metadata.create_all(bind=engine)
```

Com isso, o SQLAlchemy consegue create tabelas que ainda não existem no banco com base nos models.

A estrutura do banco passou a representar as entidades da aplicação.

> Observação: `create_all()` cria tabelas novas, mas não funciona como um sistema completo de migrações para alterações em tabelas existentes. Por isso, alterações posteriores foram realizadas manualmente no PostgreSQL. No futuro, o projeto deverá utilizar Alembic para migrations.

---

# 10. 🔄 Criação da Session

Foi criada a função:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Ela permite que o FastAPI forneça uma sessão do banco para cada requisição e depois feche essa sessão.

Nas rotas:

```python
db: Session = Depends(get_db)
```

O `Depends()` permite que o FastAPI injete automaticamente a sessão.

---

# 11. 📥 Migração do POST para PostgreSQL

O cadastro deixou de utilizar:

```python
products.append(item)
```

e passou a create objetos SQLAlchemy:

```python
product = product(
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

Assim, os products passaram a ser armazenados permanentemente no PostgreSQL.

Durante o desenvolvimento também foram cadastrados products de teste, incluindo livros da saga Jogos Vorazes 😂📚.

---

# 12. 📤 Migração do GET

O endpoint:

```text
GET /products
```

passou a consultar o banco:

```python
resultado = db.execute(select(product))
```

E os registros foram convertidos para uma lista:

```python
products = resultado.scalars().all()
```

---

# 13. 🔎 Migração do GET por ID

Para buscar um product específico:

```python
resultado = db.execute(
    select(product).where(product.id == id)
)
```

Depois:

```python
product = resultado.scalar_one_or_none()
```

Caso o product não exista:

```python
raise HTTPException(
    status_code=404,
    detail="product não encontrado."
)
```

---

# 14. ✏️ Migração do PATCH

Foi criado um schema específico para atualização de preço:

```python
class updatePreco(BaseModel):
    price: Decimal = Field(gt=0)
```

A API busca o product pelo ID e altera somente o preço:

```python
product.price = item.price
```

Depois confirma a alteração:

```python
db.commit()
```

Dessa forma, o PATCH possui uma responsabilidade específica e não permite alterar outros campos acidentalmente.

---

# 15. 🗑️ Migração do DELETE

O DELETE também passou a trabalhar diretamente com o banco.

Primeiro o product é localizado:

```python
resultado = db.execute(
    select(product).where(product.id == id)
)
```

Depois:

```python
product = resultado.scalar_one_or_none()
```

Se existir:

```python
db.delete(product)
db.commit()
```

O registro é removido do PostgreSQL.

---

# 16. 🏷️ Criação de categorys

O projeto evoluiu para trabalhar com categorys de products.

Foi criado o model:

```text
category
```

E estabelecida uma relação:

```text
category
    │
    └── vários products
```

No product foi adicionada:

```python
category_id
```

utilizando uma Foreign Key:

```python
ForeignKey("categorys.id")
```

Também foi criada a relação ORM:

```python
category = relationship(
    back_populates="products"
)
```

Enquanto a category possui:

```python
products = relationship(
    back_populates="category"
)
```

Isso permite navegar entre category e products utilizando o SQLAlchemy.

---

# 17. 📦 Controle de stock

Os products passaram a possuir:

```python
stock: Mapped[int]
```

Também foi criado um endpoint específico para atualização:

```text
PATCH /products/{id}/stock
```

Foi criado o schema:

```python
class updatestock(BaseModel):
    stock: int = Field(ge=0)
```

Assim, o stock não pode receber valores negativos.

O stock também passou a ser considerado nas operações do cart e na criação de orders.

---

# 18. 🔐 Cadastro de usuários

Foi criado o model:

```text
user
```

com os principais campos:

```text
id
name
email
password_hash
role
```

O email foi configurado como único:

```python
unique=True
```

Isso impede o cadastro de dois usuários utilizando o mesmo email.

---

# 19. 🔒 Hash e validação de password com bcrypt

A password não é armazenada diretamente no banco.

Durante o cadastro, primeiro a password passa pelas validações do Pydantic.

A password precisa possuir:

- pelo menos 8 caracteres;
- pelo menos uma letra maiúscula;
- pelo menos um número;
- pelo menos um caractere especial.

Exemplo de password válida:

```text
Lavinha123!
```

Depois da validação, a password passa pelo bcrypt:

```python
password_hash = bcrypt.hashpw(
    user.password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")
```

O banco armazena apenas o hash:

```text
password original
      ↓
validação
      ↓
   bcrypt
      ↓
password_hash
```

Durante o login, a password informada é comparada com o hash utilizando:

```python
bcrypt.checkpw()
```

A password em texto puro nunca é armazenada no banco.

---

# 20. 📧 Validação de email

O cadastro e o login passaram a utilizar validação de email através do Pydantic:

```python
email: EmailStr
```

Assim, a API rejeita valores que não possuem formato válido de email antes de continuar o processamento.

Além da validação do formato, o banco continua garantindo que o email seja único.

---

# 21. 🔑 Login e JWT

Foi implementado login utilizando JWT.

Endpoint:

```text
POST /users/login
```

Após validar email e password, a API gera um token:

```python
token = create_token(user_db.id)
```

O token contém informações como:

```text
sub → ID do usuário
exp → data de expiração
```

O token possui tempo de expiração configurado.

---

# 22. 🪪 Autenticação com Bearer Token

Foi utilizado `HTTPBearer` para autenticação.

O cliente envia:

```text
Authorization: Bearer TOKEN
```

A função:

```python
get_current_user()
```

é responsável por:

1. receber o token;
2. validar o JWT;
3. verificar a expiração;
4. obter o ID do usuário;
5. procurar o usuário no banco;
6. retornar o usuário autenticado.

Foi criado também:

```python
get_current_admin()
```

que utiliza `get_current_user()` e verifica a função do usuário.

---

# 23. 👤 Usuários e permissões

O projeto passou a utilizar dois tipos de usuário:

```text
user
admin
```

A diferença é baseada no campo:

```text
role
```

### Usuário comum

Pode:

- get products;
- get categorys;
- utilizar o cart;
- realizar compras;
- get seus próprios orders.

### Administrador

Pode realizar todas as operações do usuário comum e também:

- create products;
- alterar products;
- excluir products;
- alterar stock;
- create categorys;
- alterar categorys;
- excluir categorys;
- gerenciar orders;
- get usuários;
- alterar permissões de usuários.

A autorização utiliza:

```python
Depends(get_current_admin)
```

Enquanto operações que exigem apenas login utilizam:

```python
Depends(get_current_user)
```

Também foi aplicada a separação entre:

```text
401 → não autenticado / token inválido
403 → autenticado, mas sem permissão
```

---

# 24. 🛒 Criação do cart

O projeto agora possui um sistema de cart.

Foram criados dois models:

```text
cart
├── id
└── user_id

Itemcart
├── id
├── cart_id
├── product_id
├── quantity
└── added_price
```

Cada usuário possui um único cart através de:

```python
user_id = mapped_column(
    ForeignKey("users.id"),
    unique=True
)
```

A relação ficou:

```text
Usuário
   ↓
cart
   ↓
items do cart
   ↓
products
```

O campo `added_price` guarda o preço do product no momento em que ele foi colocado no cart.

Isso permite detectar alterações de preço enquanto o product permanece no cart.

---

# 25. 🛍️ Operações do cart

Foram criados os principais endpoints:

| Método | Endpoint             | Função            |
| ------ | -------------------- | ----------------- |
| GET    | `/cart`              | get cart          |
| POST   | `/cart`              | Adicionar product |
| PATCH  | `/cart/{product_id}` | Alterar quantity  |
| DELETE | `/cart/{product_id}` | Remover product   |

Todos exigem um usuário autenticado.

---

# 26. ➕ Regra para adicionar products

Ao adicionar um product, a API verifica:

1. se o usuário está autenticado;
2. se o cart existe;
3. se o product existe;
4. se existe stock suficiente;
5. se o product já está no cart.

Um mesmo product **não pode aparecer duplicado no cart**.

A quantity é controlada pelo endpoint de alteração de quantity.

---

# 27. 🔢 Alteração de quantity

O endpoint:

```text
PATCH /cart/{product_id}
```

permite alterar a quantity de um product.

A quantity precisa ser maior que zero:

```python
quantity > 0
```

Também é feita uma nova verificação do stock.

Assim, o usuário não consegue colocar no cart uma quantity maior que o stock disponível.

---

# 28. 🗑️ Remoção de products do cart

O endpoint:

```text
DELETE /cart/{product_id}
```

localiza o item pertencente ao cart do usuário e o remove.

A operação não interfere no cart de outros usuários.

---

# 29. 💰 Valores monetários com Decimal

Inicialmente os valores monetários utilizavam `float`.

Para evitar problemas de precisão com dinheiro, os valores foram alterados para `Decimal` na aplicação e `NUMERIC(10,2)` no PostgreSQL.

No SQLAlchemy, os campos monetários utilizam:

```python
Numeric(10, 2)
```

Os principais campos são:

```text
product.price
Itemcart.added_price
order.total
orderItem.preco
```

No Pydantic, os valores passaram a utilizar:

```python
Decimal
```

O fluxo ficou:

```text
API
 ↓
Decimal
 ↓
SQLAlchemy Numeric(10,2)
 ↓
PostgreSQL numeric(10,2)
```

Foi testado o cálculo de subtotais e totais dos orders com valores decimais, confirmando que os cálculos permanecem corretos.

---

# 30. 💵 Preço, subtotal e total do cart

Cada item do cart possui:

```text
product_id
name
preco
quantity
subtotal
```

O subtotal é calculado:

```python
subtotal = item.product.price * item.quantity
```

E o total do cart:

```python
total = sum(item["subtotal"] for item in items)
```

O preço utilizado para o cálculo vem do banco de dados, e não de um valor enviado pelo frontend.

Além disso, o sistema mantém o preço no momento em que o item foi adicionado ao cart através de:

```text
added_price
```

Dessa forma, é possível detectar alterações posteriores no preço.

---

# 31. 📦 Criação de orders

O projeto passou a possuir os models:

```text
order
orderItem
```

A estrutura permite armazenar:

### order

```text
id
user_id
status
total
```

### orderItem

```text
id
order_id
product_id
quantity
preco
```

O order é criado a partir do cart.

Durante a criação:

1. o cart do usuário é localizado;
2. é verificado se existem items;
3. o stock atual é verificado novamente;
4. o preço atual do product é utilizado;
5. o order é criado;
6. os items são registrados;
7. o stock é diminuído;
8. os items do cart são removidos;
9. a transação é confirmada.

O preço armazenado em `orderItem.preco` representa o preço no momento da compra.

Isso permite que o histórico do order continue correto mesmo que o preço do product seja alterado posteriormente.

---

# 32. 🧾 Visualização de orders

O usuário possui acesso aos seus próprios orders.

Foram implementados:

```text
GET /orders
GET /orders/{order_id}
```

O sistema garante que o usuário só consiga acessar orders pertencentes a ele.

A response contém:

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
preco
subtotal
```

---

# 33. 💳 Pagamento simulado

Não foi utilizado um gateway de pagamento real.

Foi implementado um pagamento simulado através de:

```text
POST /orders/{order_id}/pay
```

O order só pode ser pago quando estiver:

```text
PENDENTE
```

Após o pagamento:

```text
PENDENTE
   ↓
PAGO
```

O pagamento não movimenta dinheiro real.

---

# 34. 🔄 Status dos orders

Foi estabelecido um fluxo de status:

```text
PENDENTE
   ↓
PAGO
   ↓
ENVIADO
   ↓
ENTREGUE
```

Também existe a possibilidade de cancelamento:

```text
PENDENTE → CANCELADO
PAGO     → CANCELADO
```

O administrador não pode realizar transições arbitrárias.

As transições válidas são:

```text
PENDENTE → PAGO
PENDENTE → CANCELADO

PAGO → ENVIADO
PAGO → CANCELADO

ENVIADO → ENTREGUE
```

orders `ENTREGUE` ou `CANCELADO` não podem avançar para outro status.

Quando um order é cancelado, os products são devolvidos ao stock.

---

# 35. 🔎 Busca, filtros e paginação

O endpoint:

```text
GET /products
```

foi expandido para permitir filtros.

É possível utilizar:

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

A category é pesquisada pelo **name**, e não pelo ID.

Isso evita que o usuário precise conhecer detalhes internos do banco.

Internamente, o relacionamento continua utilizando:

```text
product.category_id
      ↓
category.id
```

Mas a API pública permite:

```text
category=livros
```

em vez de exigir:

```text
category_id=1
```

Também foi implementada paginação através de:

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

### Administração de orders

Foram implementados:

```text
GET   /admin/orders
GET   /admin/orders/{order_id}
PATCH /admin/orders/{order_id}/status
```

O administrador consegue get todos os orders, get um order específico e update o status respeitando as transições válidas.

### Administração de usuários

Também foram implementados:

```text
GET   /admin/users
GET   /admin/users/{user_id}
PATCH /admin/users/{user_id}/role
```

O administrador pode get usuários e alterar suas permissões entre:

```text
user
admin
```

Também existe uma proteção para impedir que o administrador remova a própria permissão de administrador.

---

# 37. 🧠 Conceitos de SQLAlchemy aprendidos

Durante o desenvolvimento foram utilizados conceitos importantes:

### `db.add()`

Adiciona um objeto à sessão atual.

### `db.commit()`

Confirma a transação no banco.

### `db.rollback()`

Desfaz alterações ainda não confirmadas.

### `db.flush()`

Envia as alterações para o banco sem finalizar a transação.

É útil, por exemplo, quando precisamos do ID gerado pelo banco antes de executar o `commit`.

### `db.refresh()`

Atualiza o objeto Python com os dados atuais do banco.

Um resumo para memorizar:

```text
flush    → envia
commit   → confirma
rollback → desfaz
refresh  → atualiza
```

---

# 38. 🧱 Organização atual do projeto

A estrutura atual está:

```text
python/
│
├── .venv/
├── .env
├── .env.example
├── .gitignore
│
├── main.py
├── database.py
├── models.py
├── schema.py
├── auth.py
│
└── routers/
    ├── products.py
    ├── categorys.py
    ├── users.py
    ├── cart.py
    ├── orders.py
    └── admin.py
```

---

# 39. 🌐 Arquitetura atual

A aplicação atualmente segue aproximadamente:

```text
                    CLIENTE
                       │
                       ▼
                    FastAPI
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Routers          Auth          Schemas
        │              │              │
        │         JWT / bcrypt        │
        │                             │
        └──────────────┬──────────────┘
                       │
                   SQLAlchemy
                       │
                    Psycopg
                       │
                  PostgreSQL
```

---

# 40. 🔐 Segurança implementada

Até o momento, foram implementados:

- hash de password com bcrypt;
- validação de password;
- validação de email;
- JWT para autenticação;
- expiração de token;
- autenticação com Bearer Token;
- diferenciação entre usuário e administrador;
- proteção de endpoints administrativos;
- email único;
- responses com `response_model`;
- variáveis sensíveis armazenadas em `.env`;
- `.env` protegido pelo `.gitignore`;
- separação entre erros HTTP 401 e 403.

A password de usuário também não é aceita como `role` no cadastro público, evitando que alguém tente se create diretamente como administrador.

---

# 41. 📋 Próximas etapas

O núcleo funcional da loja já está implementado.

Os próximos passos serão voltados para **qualidade, manutenção, infraestrutura e produção**.

## 🧪 1. Testes automatizados — CONCLUÍDO ✅

Foi implementada uma suíte de testes utilizando `pytest` para validar os principais fluxos da API.

O ambiente de testes utiliza um banco PostgreSQL separado:

```text
fastapi_products_test
```

Foram testados fluxos envolvendo:

- cadastro de usuários;
- validação de email;
- validação de password;
- login;
- JWT;
- autenticação;
- autorização;
- products;
- categorys;
- filtros;
- paginação;
- stock;
- cart;
- controle de quantity;
- orders;
- pagamento;
- cancelamento;
- área administrativa;
- regras de status.

Resultado atual:

```text
36 passed
```

Todos os 36 testes automatizados estão passando.

Com isso, a etapa de testes automatizados foi concluída e o projeto está pronto para avançar para Alembic.

---

## 🗃️ 2. Alembic

Adicionar Alembic para controlar alterações no banco através de migrations.

Isso substituirá a necessidade de realizar manualmente alterações estruturais no banco conforme o projeto evolui.

Exemplo:

```text
migration 001 → estrutura inicial
migration 002 → stock
migration 003 → usuários
migration 004 → roles
migration 005 → orders
migration 006 → Numeric para valores monetários
```

---

## 🧹 3. Refatoração final

Depois dos testes, será feita uma única revisão geral do projeto.

Serão avaliados:

- organização dos routers;
- schemas;
- names de variáveis;
- funções;
- responses;
- tratamento de erros;
- regras duplicadas;
- consultas SQLAlchemy;
- organização dos arquivos;
- padronização de names.

Também será tomada a decisão definitiva sobre utilizar português ou inglês nos names do projeto.

A intenção é evitar refatorações constantes durante o desenvolvimento.

---

## 🐳 4. Docker

create a infraestrutura utilizando:

```text
Docker
├── API FastAPI
└── PostgreSQL
```

Utilizando Docker Compose para facilitar o ambiente de desenvolvimento.

---

## 🚀 5. Preparação para produção

Depois do backend estar concluído:

- configurar ambiente de produção;
- revisar variáveis de ambiente;
- configurar banco;
- revisar segurança;
- executar migrations;
- configurar logs;
- preparar servidor;
- preparar deploy.

---

## 🎨 6. Frontend

Após finalizar e testar o backend, será desenvolvido o frontend da loja.

O frontend será responsável por:

- catálogo;
- busca;
- filtros;
- categorys;
- login;
- cadastro;
- cart;
- checkout;
- orders;
- área do usuário;
- área administrativa.

---

# 42. ✅ Estado atual do projeto

O projeto já evoluiu de:

```text
CRUD simples em memória
```

para:

```text
                         FASTAPI
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
      products          categorys        Usuários
          │                 │                 │
       stock              │            JWT + bcrypt
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                         cart
                            │
                            ▼
                          order
                            │
                            ▼
                    Pagamento simulado
                            │
                            ▼
                      Área Admin
                            │
                            ▼
                       PostgreSQL
```

O backend já possui:

- CRUD de products;
- categorys;
- relacionamento entre categorys e products;
- controle de stock;
- usuários;
- validação de email;
- validação de password;
- bcrypt;
- JWT;
- autenticação;
- autorização;
- roles;
- cart;
- controle de quantity;
- controle de stock no cart;
- orders;
- histórico de orders;
- pagamento simulado;
- cancelamento;
- fluxo de status;
- área administrativa;
- gerenciamento de usuários;
- busca;
- filtros;
- paginação;
- valores monetários com Decimal/Numeric;
- Git e GitHub.

---

# 43. 📚 O que este projeto ensinou até aqui

O desenvolvimento permitiu sair de um CRUD básico e estudar conceitos presentes em aplicações reais:

- Python;
- FastAPI;
- Pydantic;
- HTTP;
- REST;
- CRUD;
- PostgreSQL;
- SQLAlchemy;
- Psycopg;
- Foreign Keys;
- relacionamentos ORM;
- Sessions;
- Transactions;
- `commit`, `rollback`, `flush` e `refresh`;
- validação de dados;
- validação de email;
- validação de password;
- hash de passwords;
- bcrypt;
- JWT;
- autenticação;
- autorização;
- roles;
- dependências do FastAPI;
- controle de stock;
- regras de negócio;
- cart de compras;
- orders;
- pagamento simulado;
- controle de status;
- filtros;
- paginação;
- Decimal;
- Numeric;
- organização de projeto;
- variáveis de ambiente;
- Git e GitHub.

O projeto começou como uma forma de aprender CRUD e foi transformado gradualmente em uma **API de e-commerce completa**, com foco em entender não apenas como fazer cada funcionalidade, mas também por que cada decisão de arquitetura existe.

---

# 📌 Próximo passo

O próximo módulo será:

```text
🗃️ ALEMBIC
```

A ideia será adicionar migrations ao projeto para controlar a evolução da estrutura do banco de dados de forma organizada e reproduzível.

Depois de Alembic, seguiremos para:

```text
🧹 Refatoração final
        ↓
🐳 Docker
        ↓
🚀 Preparação para produção / Deploy
        ↓
🎨 Frontend
```
