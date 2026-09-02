from pydantic import BaseModel, ConfigDict, Field

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    estoque: int = Field(ge=0)
    category_id: int

class AtualizarPreco(BaseModel):
    price: float

class ProdutoResponse(BaseModel):
    id: int
    name: str
    price: float
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
    price: float = Field(gt=0)
    estoque: int = Field(ge=0)
    category_id: int
    categoria: CategoriaResponse

    model_config = ConfigDict(from_attributes=True)
    
class AtualizarEstoque(BaseModel):
    estoque: int = Field(ge=0)
    
class UsuarioCreate(BaseModel):
    name: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str
class UsuarioResponse(BaseModel):
    id: int
    name: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)