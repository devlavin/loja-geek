from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from auth import get_current_admin
from models import Product, Category, User
from schema import (
    Item,
    UpdateProduct,
    UpdateStock,
    ProductResponse,
    ProductWithCategoryResponse,
)


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("")
def create_product(
    items: list[Item],
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        for item in items:

            result = db.execute(
                select(Category).where(
                    Category.id == item.category_id
                )
            )

            category_db = result.scalar_one_or_none()

            if category_db is None:
                raise HTTPException(
                    status_code=404,
                    detail="Categoria não encontrada."
                )

            new_product = Product(
                name=item.name,
                description=item.description,
                price=item.price,
                stock=item.stock,
                category_id=item.category_id,
                image_url=item.image_url
            )

            db.add(new_product)

        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar produto."
        )

    quantity = len(items)

    if quantity == 1:
        return "Produto cadastrado com sucesso."

    return f"{quantity} produtos cadastrados com sucesso."


@router.get(
    "",
    response_model=list[ProductResponse]
)
def list_products(
    name: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = select(Product)

    if name:
        query = query.where(
            Product.name.ilike(f"%{name}%")
        )

    if category:
        query = query.join(Product.category).where(
            Category.name.ilike(f"%{category}%")
        )

    if min_price is not None:
        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.where(
            Product.price <= max_price
        )

    query = query.offset(skip).limit(limit)

    result = db.execute(query)

    return result.scalars().all()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    item: UpdateProduct,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    if item.name is not None:
        product.name = item.name

    if item.description is not None:
        product.description = item.description

    if item.price is not None:
        product.price = item.price

    if item.stock is not None:
        product.stock = item.stock

    if item.category_id is not None:
        result = db.execute(
            select(Category).where(
                Category.id == item.category_id
            )
        )

        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada."
            )

        product.category_id = item.category_id

    if item.image_url is not None:
        product.image_url = item.image_url

    db.commit()
    db.refresh(product)

    return product

@router.patch(
    "/{product_id}/stock",
    response_model=ProductResponse
)
def update_stock(
    product_id: int,
    item: UpdateStock,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    product.stock = item.stock

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    db.delete(product)
    db.commit()

    return "Produto excluído com sucesso."
