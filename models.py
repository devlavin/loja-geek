from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy  import String, ForeignKey, Numeric
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = "produtos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )
    estoque: Mapped[int] = mapped_column(default=0)
    
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id")
    )
    categoria: Mapped["Categoria"] = relationship(
        back_populates="produtos"
    )
    
class Categoria(Base):
    __tablename__ = "categorias"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    produtos: Mapped[list["Produto"]] = relationship(
        back_populates="categoria"
    )

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    role: Mapped[str] = mapped_column(
        String(20),
        default="user"
    )
    
class Carrinho(Base):
    __tablename__ = "carrinhos"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        unique=True
    )

    itens: Mapped[list["ItemCarrinho"]] = relationship(
        back_populates="carrinho"
    )
    
class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id: Mapped[int] = mapped_column(primary_key=True)

    carrinho_id: Mapped[int] = mapped_column(
        ForeignKey("carrinhos.id")
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id")
    )

    quantidade: Mapped[int] = mapped_column(
        default=1
    )

    preco_adicionado: Mapped[Decimal] = mapped_column(
    Numeric(10, 2)
    )

    carrinho: Mapped["Carrinho"] = relationship(
        back_populates="itens"
    )

    produto: Mapped["Produto"] = relationship()
    
class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDENTE"
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    itens: Mapped[list["PedidoItem"]] = relationship(
        back_populates="pedido"
    )


class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id: Mapped[int] = mapped_column(primary_key=True)

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id")
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id")
    )

    quantidade: Mapped[int] = mapped_column()

    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    pedido: Mapped["Pedido"] = relationship(
        back_populates="itens"
    )

    produto: Mapped["Produto"] = relationship()