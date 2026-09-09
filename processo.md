# 🛒 Processo de Desenvolvimento — Geek Store

## 1. Início do projeto

O projeto começou como um CRUD simples de produtos utilizando **Python e FastAPI**.

Inicialmente, os produtos eram armazenados em memória. O objetivo era praticar os conceitos básicos de uma API REST, como rotas, métodos HTTP, requisições e respostas.

---

## 2. Persistência com PostgreSQL

Depois da primeira versão, o projeto evoluiu para utilizar **PostgreSQL** como banco de dados.

O **SQLAlchemy** foi utilizado como ORM para facilitar a comunicação entre a aplicação e o banco.

Nesse momento foram criados os principais modelos da aplicação:

* Usuários
* Produtos
* Categorias
* Carrinho
* Itens do carrinho
* Pedidos
* Itens dos pedidos

Também foram estabelecidos os relacionamentos entre essas entidades.

---

## 3. Validações

Com a aplicação crescendo, foram adicionadas validações utilizando **Pydantic**.

Algumas regras implementadas:

* Preço deve ser maior que zero
* Estoque não pode ser negativo
* Categorias precisam existir antes de serem associadas aos produtos
* Dados recebidos pela API precisam seguir os schemas definidos
* Quantidade de produtos precisa respeitar o estoque disponível

---

## 4. Autenticação e autorização

Foi implementado um sistema de autenticação utilizando **JWT**.

Após o login, o usuário recebe um token que deve ser enviado nas requisições protegidas.

Também foi implementada autorização por roles:

```text
user
admin
```

As operações administrativas passaram a ser protegidas, impedindo que usuários comuns realizem ações exclusivas do administrador.

As senhas dos usuários são armazenadas utilizando **bcrypt** para geração de hash.

---

## 5. Produtos e categorias

O CRUD inicial foi expandido para trabalhar com banco de dados e categorias.

Foram adicionados:

* Cadastro de produtos
* Consulta de produtos
* Atualização de produtos
* Exclusão de produtos
* Cadastro e consulta de categorias
* Relacionamento entre produtos e categorias
* Busca por nome
* Filtros
* Paginação
* Controle de estoque

Também foram adicionadas descrições e imagens dos produtos através de URL.

---

## 6. Carrinho

Foi desenvolvido o sistema de carrinho de compras.

O carrinho permite:

* Adicionar produtos
* Alterar quantidade
* Remover produtos
* Consultar os itens
* Calcular o total

Foram implementadas regras para verificar o estoque disponível.

Também foi definido que a adição de um produto já existente no carrinho deve aumentar sua quantidade em vez de criar uma duplicação do item.

---

## 7. Pedidos

A aplicação passou a transformar o carrinho em pedidos.

O fluxo inclui:

* Criação do pedido
* Itens do pedido
* Histórico de pedidos
* Consulta dos detalhes
* Pagamento simulado
* Cancelamento
* Atualização do estoque
* Controle do status do pedido

Os pedidos possuem diferentes estados para representar o andamento da compra.

---

## 8. Testes automatizados

Foi criada uma suíte de testes utilizando **Pytest**.

Os testes foram utilizados para verificar as principais funcionalidades e regras da API, incluindo:

* Usuários
* Autenticação
* Produtos
* Categorias
* Estoque
* Carrinho
* Pedidos
* Pagamento
* Permissões administrativas

A suíte chegou a **66 testes passando**.

---

## 9. Docker

O projeto foi posteriormente preparado para execução utilizando **Docker e Docker Compose**.

A utilização de containers facilitou a configuração do ambiente de desenvolvimento e a execução dos serviços da aplicação.

O PostgreSQL também passou a ser executado através do ambiente Docker.

---

## 10. Desenvolvimento do frontend

Após a estrutura principal do backend estar funcionando, começou o desenvolvimento do frontend utilizando:

* React
* TypeScript
* Vite
* React Router

O frontend passou a consumir os endpoints da API para apresentar a interface da loja.

Foram desenvolvidas funcionalidades como:

* Catálogo
* Login
* Carrinho
* Pedidos
* Perfil do usuário
* Navegação entre páginas

---

## 11. Painel administrativo

Foi desenvolvido o início do painel administrativo para usuários com role `admin`.

O painel possui áreas para gerenciamento de:

* Produtos
* Categorias
* Usuários
* Pedidos

O acesso ao painel é controlado de acordo com a permissão do usuário.

Também foi adicionada uma navegação específica para o painel administrativo.

---

## 12. Imagens dos produtos

Na etapa mais recente, foi adicionada a possibilidade de armazenar uma **URL de imagem** para cada produto.

O backend foi atualizado para receber e retornar o campo `image_url`.

O frontend também foi adaptado para exibir as imagens:

* No catálogo
* Nos cards dos produtos
* No carrinho

As descrições dos produtos também passaram a ser utilizadas na aplicação.

---

## 13. Estado atual

Atualmente, a Geek Store possui uma estrutura full stack composta por:

```text
Frontend
React + TypeScript + Vite
        ↓
Backend
FastAPI + Pydantic
        ↓
Persistência
SQLAlchemy + PostgreSQL
```

Além disso, o projeto conta com:

* Autenticação JWT
* Roles `user` e `admin`
* CRUD de produtos e categorias
* Controle de estoque
* Carrinho
* Pedidos
* Pagamento simulado
* Testes automatizados
* Alembic
* Docker
* Frontend integrado à API
* Painel administrativo
* Imagens e descrições dos produtos

---

## 14. Próximas etapas

As próximas etapas planejadas são:

* Refinar a interface do frontend
* Melhorar o tratamento de erros
* Revisar questões de segurança
* Finalizar funcionalidades do painel administrativo
* Melhorar a experiência do usuário
* Preparar o projeto para deploy

---

## 🎯 Objetivo do projeto

A Geek Store está sendo desenvolvida como um projeto de estudo e portfólio para consolidar conhecimentos em **Python, FastAPI, PostgreSQL, SQLAlchemy, desenvolvimento de APIs REST, autenticação, testes, React e TypeScript**.

O principal objetivo é demonstrar a evolução do projeto desde um CRUD simples até uma aplicação full stack com funcionalidades e regras de negócio mais próximas de um sistema real.
