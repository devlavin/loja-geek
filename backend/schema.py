import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from decimal import Decimal
from typing import Literal

class Item(BaseModel):
    name: str
    price: Decimal = Field(gt=0)
    description: str | None = None
    stock: int = Field(ge=0)
    category_id: int
    image_url: str | None = None

class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    image_url: str | None = None
    
class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str | None = None
    stock: int
    category_id: int
    image_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
class CategoryCreate(BaseModel):
    name: str

class UpdateCategory(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
        
    model_config = ConfigDict(from_attributes=True)
    
class CategoryWithProductsResponse(BaseModel):
    id: int
    name: str
    products: list[ProductResponse]
    
    model_config = ConfigDict(from_attributes=True)
    
class ProductWithCategoryResponse(BaseModel):
    id: int
    name: str
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)
    
class UpdateStock(BaseModel):
    stock: int = Field(ge=0)
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiuscula."
            )

        if not re.search(r"\d", password):
            raise ValueError(
                "A senha deve conter pelo menos um número."
            )

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )

        return password

class UserLogin(BaseModel):
    email: str
    password: str
    
class UpdateUser(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(
        default=None,
        min_length=8
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if password is None:
            return password

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiuscula."
            )

        if not re.search(r"\d", password):
            raise ValueError(
                "A senha deve conter pelo menos um número."
            )

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )

        return password

class UpdateRole(BaseModel):
    role: Literal["user", "admin"]
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)
    
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    product_id: int
    name: str
    image_url: str | None
    price: Decimal
    added_price: Decimal
    price_changed: bool
    quantity: int
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    id: int | None
    items: list[CartItemResponse]
    total: Decimal

class OrderItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: Decimal
    subtotal: Decimal


class OrderResponse(BaseModel):
    id: int
    status: str
    items: list[OrderItemResponse]
    total: Decimal

class UpdateStatusOrder(BaseModel):
    status: Literal["PENDENTE", "PAGO", "ENVIADO", "ENTREGUE", "CANCELADO"]