import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from decimal import Decimal

class Item(BaseModel):
    name: str
    price: Decimal = Field(gt=0)
    estoque: int = Field(ge=0)
    category_id: int

class AtualizarPreco(BaseModel):
    price: Decimal = Field(gt=0)

class ProdutoResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    estoque: int
    category_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class CategoriaCreate(BaseModel):
    name: str

class AtualizarCategoria(BaseModel):
    name: str

class CategoriaResponse(BaseModel):
    id: int
    name: str
        
    model_config = ConfigDict(from_attributes=True)
    
class CategoriaComProdutosResponse(BaseModel):
    id: int
    name: str
    produtos: list[ProdutoResponse]
    
    model_config = ConfigDict(from_attributes=True)
    
class ProdutoComCategoriaResponse(BaseModel):
    id: int
    name: str
    price: Decimal = Field(gt=0)
    estoque: int = Field(ge=0)
    category_id: int
    categoria: CategoriaResponse

    model_config = ConfigDict(from_attributes=True)
    
class AtualizarEstoque(BaseModel):
    estoque: int = Field(ge=0)
    
class UsuarioCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    
    @field_validator("password")
    @classmethod
    def validar_senha(cls, senha):
        if not re.search(r"[A-Z]", senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiuscula."
            )

        if not re.search(r"\d", senha):
            raise ValueError(
                "A senha deve conter pelo menos um número."
            )

        if not re.search(r"[^A-Za-z0-9]", senha):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )

        return senha

class UsuarioLogin(BaseModel):
    email: str
    password: str
    
class AtualizarUsuario(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(
        default=None,
        min_length=8
    )

    @field_validator("password")
    @classmethod
    def validar_senha(cls, senha):
        if senha is None:
            return senha

        if not re.search(r"[A-Z]", senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiuscula."
            )

        if not re.search(r"\d", senha):
            raise ValueError(
                "A senha deve conter pelo menos um número."
            )

        if not re.search(r"[^A-Za-z0-9]", senha):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )

        return senha
    
class UsuarioResponse(BaseModel):
    id: int
    name: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)
    
class ItemCarrinhoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class ItemCarrinhoResponse(BaseModel):
    produto_id: int
    nome: str
    preco: Decimal
    quantidade: int
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class CarrinhoResponse(BaseModel):
    id: int
    itens: list[ItemCarrinhoResponse]
    total: Decimal

class PedidoItemResponse(BaseModel):
    produto_id: int
    nome: str
    quantidade: int
    preco: Decimal
    subtotal: Decimal


class PedidoResponse(BaseModel):
    id: int
    status: str
    itens: list[PedidoItemResponse]
    total: Decimal

class AtualizarStatusPedido(BaseModel):
    status: str