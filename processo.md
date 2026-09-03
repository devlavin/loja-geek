# 🐍 Projeto CRUD de Produtos — FastAPI + PostgreSQL

## 📌 Sobre o projeto

Este projeto começou como um CRUD simples de produtos desenvolvido em Python com FastAPI, inicialmente utilizando armazenamento em memória.

O objetivo foi compreender, de forma progressiva, como construir uma API REST, validar dados, trabalhar com banco de dados, autenticação, autorização e regras de negócio.

Após validar a lógica do CRUD em memória, o projeto foi evoluído para utilizar PostgreSQL com SQLAlchemy, tornando os dados persistentes e aproximando a aplicação de uma arquitetura utilizada em aplicações reais.

Atualmente, o projeto evoluiu de um simples CRUD de produtos para uma **API de uma loja virtual**, com usuários, autenticação, categorias, estoque, carrinho, pedidos, pagamento simulado e área administrativa.

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

* como criar uma API;
* como criar endpoints;
* como utilizar métodos HTTP;
* como o FastAPI processa requisições;
* como retornar respostas.

---

# 2. 📦 Criação do modelo de dados

Utilizei Pydantic para definir e validar os dados dos produtos:

```python
class Item(BaseModel):
    id: int
    name: str
    price: float
```

Cada produto possuía inicialmente:

* `id`
* `name`
* `price`

O Pydantic ficou responsável pela validação dos dados recebidos pela API.

---

# 3. 💾 Criação do CRUD inicialmente em memória

Antes de utilizar um banco de dados, criei uma lista para armazenar os produtos:

```python
produtos = []
```

Isso permitiu desenvolver e testar a lógica do CRUD sem depender inicialmente de um banco.

Foram criadas as operações:

| Método | Endpoint         | Função             |
| ------ | ---------------- | ------------------ |
| POST   | `/produtos`      | Cadastrar produtos |
| GET    | `/produtos`      | Listar produtos    |
| GET    | `/produtos/{id}` | Buscar produto     |
| PATCH  | `/produtos/{id}` | Atualizar preço    |
| DELETE | `/produtos/{id}` | Excluir produto    |

Essa etapa foi importante para entender primeiro a lógica da aplicação antes de introduzir persistência.

---

# 4. 📚 Cadastro de vários produtos

Inicialmente o endpoint recebia apenas um produto.

Depois alterei para aceitar vários produtos de uma vez:

```python
@app.post("/produtos")
def cadastrarProd(itens: list[Item]):
```

Utilizei um `for` para percorrer os produtos:

```python
for item in itens:
    produtos.append(item)
```

Isso permitiu enviar vários produtos em uma única requisição.

---

# 5. 🔎 Busca de produto por ID

Foi criado o endpoint:

```text
GET /produtos/{id}
```

A rota procura o produto pelo ID informado.

Também implementei tratamento de erro:

```python
raise HTTPException(
    status_code=404,
    detail="Produto não encontrado."
)
```

Assim, quando um produto não existe, a API retorna HTTP 404.

---

# 6. 🗄️ Introdução do PostgreSQL

Depois que o CRUD em memória estava funcionando, decidi substituir a lista pelo PostgreSQL.

Foi criado o banco:

```text
fastapi_produtos
```

Também foi configurado um ambiente virtual:

```text
.venv
```

E instaladas as principais dependências:

* FastAPI
* SQLAlchemy
* Psycopg
* python-dotenv
* bcrypt
* PyJWT

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
fastapi_produtos
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

Inicialmente foi criado o model `Produto`.

Com a evolução do projeto, novos models foram adicionados:

* `Produto`
* `Categoria`
* `Usuario`
* `Carrinho`
* `ItemCarrinho`
* `Pedido`
* `PedidoItem`

---

# 9. 🏗️ Criação automática das tabelas

Foi utilizado:

```python
Base.metadata.create_all(bind=engine)
```

Com isso, o SQLAlchemy consegue criar tabelas que ainda não existem no banco com base nos models.

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
produtos.append(item)
```

e passou a criar objetos SQLAlchemy:

```python
produto = Produto(
    name=item.name,
    price=item.price,
    estoque=item.estoque,
    category_id=item.category_id
)
```

Depois:

```python
db.add(produto)
db.commit()
```

Assim, os produtos passaram a ser armazenados permanentemente no PostgreSQL.

Durante o desenvolvimento também foram cadastrados produtos de teste, incluindo livros da saga Jogos Vorazes 😂📚.

---

# 12. 📤 Migração do GET

O endpoint:

```text
GET /produtos
```

passou a consultar o banco:

```python
resultado = db.execute(select(Produto))
```

E os registros foram convertidos para uma lista:

```python
produtos = resultado.scalars().all()
```

---

# 13. 🔎 Migração do GET por ID

Para buscar um produto específico:

```python
resultado = db.execute(
    select(Produto).where(Produto.id == id)
)
```

Depois:

```python
produto = resultado.scalar_one_or_none()
```

Caso o produto não exista:

```python
raise HTTPException(
    status_code=404,
    detail="Produto não encontrado."
)
```

---

# 14. ✏️ Migração do PATCH

Foi criado um schema específico para atualização de preço:

```python
class AtualizarPreco(BaseModel):
    price: Decimal = Field(gt=0)
```

A API busca o produto pelo ID e altera somente o preço:

```python
produto.price = item.price
```

Depois confirma a alteração:

```python
db.commit()
```

Dessa forma, o PATCH possui uma responsabilidade específica e não permite alterar outros campos acidentalmente.

---

# 15. 🗑️ Migração do DELETE

O DELETE também passou a trabalhar diretamente com o banco.

Primeiro o produto é localizado:

```python
resultado = db.execute(
    select(Produto).where(Produto.id == id)
)
```

Depois:

```python
produto = resultado.scalar_one_or_none()
```

Se existir:

```python
db.delete(produto)
db.commit()
```

O registro é removido do PostgreSQL.

---

# 16. 🏷️ Criação de categorias

O projeto evoluiu para trabalhar com categorias de produtos.

Foi criado o model:

```text
Categoria
```

E estabelecida uma relação:

```text
Categoria
    │
    └── vários Produtos
```

No produto foi adicionada:

```python
category_id
```

utilizando uma Foreign Key:

```python
ForeignKey("categorias.id")
```

Também foi criada a relação ORM:

```python
categoria = relationship(
    back_populates="produtos"
)
```

Enquanto a categoria possui:

```python
produtos = relationship(
    back_populates="categoria"
)
```

Isso permite navegar entre categoria e produtos utilizando o SQLAlchemy.

---

# 17. 📦 Controle de estoque

Os produtos passaram a possuir:

```python
estoque: Mapped[int]
```

Também foi criado um endpoint específico para atualização:

```text
PATCH /produtos/{id}/estoque
```

Foi criado o schema:

```python
class AtualizarEstoque(BaseModel):
    estoque: int = Field(ge=0)
```

Assim, o estoque não pode receber valores negativos.

O estoque também passou a ser considerado nas operações do carrinho e na criação de pedidos.

---

# 18. 🔐 Cadastro de usuários

Foi criado o model:

```text
Usuario
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

# 19. 🔒 Hash e validação de senha com bcrypt

A senha não é armazenada diretamente no banco.

Durante o cadastro, primeiro a senha passa pelas validações do Pydantic.

A senha precisa possuir:

* pelo menos 8 caracteres;
* pelo menos uma letra maiúscula;
* pelo menos um número;
* pelo menos um caractere especial.

Exemplo de senha válida:

```text
Lavinha123!
```

Depois da validação, a senha passa pelo bcrypt:

```python
senha_hash = bcrypt.hashpw(
    usuario.password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")
```

O banco armazena apenas o hash:

```text
senha original
      ↓
validação
      ↓
   bcrypt
      ↓
password_hash
```

Durante o login, a senha informada é comparada com o hash utilizando:

```python
bcrypt.checkpw()
```

A senha em texto puro nunca é armazenada no banco.

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
POST /usuarios/login
```

Após validar email e senha, a API gera um token:

```python
token = criar_token(usuario_db.id)
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

* visualizar produtos;
* visualizar categorias;
* utilizar o carrinho;
* realizar compras;
* visualizar seus próprios pedidos.

### Administrador

Pode realizar todas as operações do usuário comum e também:

* cadastrar produtos;
* alterar produtos;
* excluir produtos;
* alterar estoque;
* cadastrar categorias;
* alterar categorias;
* excluir categorias;
* gerenciar pedidos;
* visualizar usuários;
* alterar permissões de usuários.

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

# 24. 🛒 Criação do carrinho

O projeto agora possui um sistema de carrinho.

Foram criados dois models:

```text
Carrinho
├── id
└── usuario_id

ItemCarrinho
├── id
├── carrinho_id
├── produto_id
├── quantidade
└── preco_adicionado
```

Cada usuário possui um único carrinho através de:

```python
usuario_id = mapped_column(
    ForeignKey("usuarios.id"),
    unique=True
)
```

A relação ficou:

```text
Usuário
   ↓
Carrinho
   ↓
Itens do carrinho
   ↓
Produtos
```

O campo `preco_adicionado` guarda o preço do produto no momento em que ele foi colocado no carrinho.

Isso permite detectar alterações de preço enquanto o produto permanece no carrinho.

---

# 25. 🛍️ Operações do carrinho

Foram criados os principais endpoints:

| Método | Endpoint                 | Função              |
| ------ | ------------------------ | ------------------- |
| GET    | `/carrinho`              | Visualizar carrinho |
| POST   | `/carrinho`              | Adicionar produto   |
| PATCH  | `/carrinho/{produto_id}` | Alterar quantidade  |
| DELETE | `/carrinho/{produto_id}` | Remover produto     |

Todos exigem um usuário autenticado.

---

# 26. ➕ Regra para adicionar produtos

Ao adicionar um produto, a API verifica:

1. se o usuário está autenticado;
2. se o carrinho existe;
3. se o produto existe;
4. se existe estoque suficiente;
5. se o produto já está no carrinho.

Um mesmo produto **não pode aparecer duplicado no carrinho**.

A quantidade é controlada pelo endpoint de alteração de quantidade.

---

# 27. 🔢 Alteração de quantidade

O endpoint:

```text
PATCH /carrinho/{produto_id}
```

permite alterar a quantidade de um produto.

A quantidade precisa ser maior que zero:

```python
quantidade > 0
```

Também é feita uma nova verificação do estoque.

Assim, o usuário não consegue colocar no carrinho uma quantidade maior que o estoque disponível.

---

# 28. 🗑️ Remoção de produtos do carrinho

O endpoint:

```text
DELETE /carrinho/{produto_id}
```

localiza o item pertencente ao carrinho do usuário e o remove.

A operação não interfere no carrinho de outros usuários.

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
Produto.price
ItemCarrinho.preco_adicionado
Pedido.total
PedidoItem.preco
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

Foi testado o cálculo de subtotais e totais dos pedidos com valores decimais, confirmando que os cálculos permanecem corretos.

---

# 30. 💵 Preço, subtotal e total do carrinho

Cada item do carrinho possui:

```text
produto_id
nome
preco
quantidade
subtotal
```

O subtotal é calculado:

```python
subtotal = item.produto.price * item.quantidade
```

E o total do carrinho:

```python
total = sum(item["subtotal"] for item in itens)
```

O preço utilizado para o cálculo vem do banco de dados, e não de um valor enviado pelo frontend.

Além disso, o sistema mantém o preço no momento em que o item foi adicionado ao carrinho através de:

```text
preco_adicionado
```

Dessa forma, é possível detectar alterações posteriores no preço.

---

# 31. 📦 Criação de pedidos

O projeto passou a possuir os models:

```text
Pedido
PedidoItem
```

A estrutura permite armazenar:

### Pedido

```text
id
usuario_id
status
total
```

### PedidoItem

```text
id
pedido_id
produto_id
quantidade
preco
```

O pedido é criado a partir do carrinho.

Durante a criação:

1. o carrinho do usuário é localizado;
2. é verificado se existem itens;
3. o estoque atual é verificado novamente;
4. o preço atual do produto é utilizado;
5. o pedido é criado;
6. os itens são registrados;
7. o estoque é diminuído;
8. os itens do carrinho são removidos;
9. a transação é confirmada.

O preço armazenado em `PedidoItem.preco` representa o preço no momento da compra.

Isso permite que o histórico do pedido continue correto mesmo que o preço do produto seja alterado posteriormente.

---

# 32. 🧾 Visualização de pedidos

O usuário possui acesso aos seus próprios pedidos.

Foram implementados:

```text
GET /pedidos
GET /pedidos/{pedido_id}
```

O sistema garante que o usuário só consiga acessar pedidos pertencentes a ele.

A resposta contém:

```text
id
status
itens
total
```

Cada item apresenta:

```text
produto_id
nome
quantidade
preco
subtotal
```

---

# 33. 💳 Pagamento simulado

Não foi utilizado um gateway de pagamento real.

Foi implementado um pagamento simulado através de:

```text
POST /pedidos/{pedido_id}/pagar
```

O pedido só pode ser pago quando estiver:

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

# 34. 🔄 Status dos pedidos

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

Pedidos `ENTREGUE` ou `CANCELADO` não podem avançar para outro status.

Quando um pedido é cancelado, os produtos são devolvidos ao estoque.

---

# 35. 🔎 Busca, filtros e paginação

O endpoint:

```text
GET /produtos
```

foi expandido para permitir filtros.

É possível utilizar:

```text
nome
categoria
min_price
max_price
skip
limit
```

Exemplos:

```text
/produtos?nome=harry
```

```text
/produtos?categoria=livros
```

```text
/produtos?min_price=30&max_price=100
```

Os filtros podem ser combinados:

```text
/produtos?nome=harry&categoria=livros&min_price=30
```

A categoria é pesquisada pelo **nome**, e não pelo ID.

Isso evita que o usuário precise conhecer detalhes internos do banco.

Internamente, o relacionamento continua utilizando:

```text
Produto.category_id
      ↓
Categoria.id
```

Mas a API pública permite:

```text
categoria=livros
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

### Administração de pedidos

Foram implementados:

```text
GET   /admin/pedidos
GET   /admin/pedidos/{pedido_id}
PATCH /admin/pedidos/{pedido_id}/status
```

O administrador consegue visualizar todos os pedidos, visualizar um pedido específico e atualizar o status respeitando as transições válidas.

### Administração de usuários

Também foram implementados:

```text
GET   /admin/usuarios
GET   /admin/usuarios/{usuario_id}
PATCH /admin/usuarios/{usuario_id}/role
```

O administrador pode visualizar usuários e alterar suas permissões entre:

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
    ├── produtos.py
    ├── categorias.py
    ├── usuarios.py
    ├── carrinho.py
    ├── pedidos.py
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

* hash de senha com bcrypt;
* validação de senha;
* validação de email;
* JWT para autenticação;
* expiração de token;
* autenticação com Bearer Token;
* diferenciação entre usuário e administrador;
* proteção de endpoints administrativos;
* email único;
* respostas com `response_model`;
* variáveis sensíveis armazenadas em `.env`;
* `.env` protegido pelo `.gitignore`;
* separação entre erros HTTP 401 e 403.

A senha de usuário também não é aceita como `role` no cadastro público, evitando que alguém tente se cadastrar diretamente como administrador.

---

# 41. 📋 Próximas etapas

O núcleo funcional da loja já está implementado.

Os próximos passos serão voltados para **qualidade, manutenção, infraestrutura e produção**.

## 🧪 1. Testes automatizados

Adicionar testes utilizando `pytest` para:

* cadastro;
* validação de email;
* validação de senha;
* login;
* JWT;
* autorização;
* produtos;
* categorias;
* filtros;
* carrinho;
* estoque;
* pedidos;
* pagamento;
* cancelamento;
* área administrativa;
* regras de status.

Os testes deverão utilizar um ambiente/banco de testes separado para não modificar os dados de desenvolvimento.

---

## 🗃️ 2. Alembic

Adicionar Alembic para controlar alterações no banco através de migrations.

Isso substituirá a necessidade de realizar manualmente alterações estruturais no banco conforme o projeto evolui.

Exemplo:

```text
migration 001 → estrutura inicial
migration 002 → estoque
migration 003 → usuários
migration 004 → roles
migration 005 → pedidos
migration 006 → Numeric para valores monetários
```

---

## 🧹 3. Refatoração final

Depois dos testes, será feita uma única revisão geral do projeto.

Serão avaliados:

* organização dos routers;
* schemas;
* nomes de variáveis;
* funções;
* respostas;
* tratamento de erros;
* regras duplicadas;
* consultas SQLAlchemy;
* organização dos arquivos;
* padronização de nomes.

Também será tomada a decisão definitiva sobre utilizar português ou inglês nos nomes do projeto.

A intenção é evitar refatorações constantes durante o desenvolvimento.

---

## 🐳 4. Docker

Criar a infraestrutura utilizando:

```text
Docker
├── API FastAPI
└── PostgreSQL
```

Utilizando Docker Compose para facilitar o ambiente de desenvolvimento.

---

## 🚀 5. Preparação para produção

Depois do backend estar concluído:

* configurar ambiente de produção;
* revisar variáveis de ambiente;
* configurar banco;
* revisar segurança;
* executar migrations;
* configurar logs;
* preparar servidor;
* preparar deploy.

---

## 🎨 6. Frontend

Após finalizar e testar o backend, será desenvolvido o frontend da loja.

O frontend será responsável por:

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
      Produtos          Categorias        Usuários
          │                 │                 │
       Estoque              │            JWT + bcrypt
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                         Carrinho
                            │
                            ▼
                          Pedido
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

* CRUD de produtos;
* categorias;
* relacionamento entre categorias e produtos;
* controle de estoque;
* usuários;
* validação de email;
* validação de senha;
* bcrypt;
* JWT;
* autenticação;
* autorização;
* roles;
* carrinho;
* controle de quantidade;
* controle de estoque no carrinho;
* pedidos;
* histórico de pedidos;
* pagamento simulado;
* cancelamento;
* fluxo de status;
* área administrativa;
* gerenciamento de usuários;
* busca;
* filtros;
* paginação;
* valores monetários com Decimal/Numeric;
* Git e GitHub.

---

# 43. 📚 O que este projeto ensinou até aqui

O desenvolvimento permitiu sair de um CRUD básico e estudar conceitos presentes em aplicações reais:

* Python;
* FastAPI;
* Pydantic;
* HTTP;
* REST;
* CRUD;
* PostgreSQL;
* SQLAlchemy;
* Psycopg;
* Foreign Keys;
* relacionamentos ORM;
* Sessions;
* Transactions;
* `commit`, `rollback`, `flush` e `refresh`;
* validação de dados;
* validação de email;
* validação de senha;
* hash de senhas;
* bcrypt;
* JWT;
* autenticação;
* autorização;
* roles;
* dependências do FastAPI;
* controle de estoque;
* regras de negócio;
* carrinho de compras;
* pedidos;
* pagamento simulado;
* controle de status;
* filtros;
* paginação;
* Decimal;
* Numeric;
* organização de projeto;
* variáveis de ambiente;
* Git e GitHub.

O projeto começou como uma forma de aprender CRUD e foi transformado gradualmente em uma **API de e-commerce completa**, com foco em entender não apenas como fazer cada funcionalidade, mas também por que cada decisão de arquitetura existe.

---

# 📌 Próximo passo

Amanhã, o próximo módulo será:

```text
🧪 PYTEST
```

A ideia será criar um ambiente de testes separado e começar a testar a API por fluxos completos, garantindo que o que já construímos continue funcionando antes de partir para Alembic, refatoração, Docker e deploy.
