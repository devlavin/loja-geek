from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy  import String, Float

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = "produtos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)