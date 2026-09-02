from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy  import String, Float, ForeignKey

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = "produtos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
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